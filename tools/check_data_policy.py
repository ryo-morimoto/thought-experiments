#!/usr/bin/env python3
"""DATA_POLICY.md のルールを検査する。依存は標準ライブラリと openssl だけ（Python 3.11+）。

全ファイルのライセンス宣言（網羅性）は REUSE（`reuse lint`）が受け持つ。
このスクリプトは REUSE がやらないこと、つまり出所・ライセンス義務・証拠を検査する。

使い方:
    python3 tools/check_data_policy.py                 # 検査のみ。違反があれば終了コード 1
    python3 tools/check_data_policy.py --fix           # REUSE.toml と NOTICE.md を再生成してから検査
    python3 tools/check_data_policy.py --report r.json # 結果を JSON でも書き出す（CI の attestation 用）
"""

from __future__ import annotations

import datetime as dt
import fnmatch
import hashlib
import json
import shutil
import subprocess
import sys
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

import embedded_data

ROOT = Path(__file__).resolve().parent.parent
POLICY_FILE = ROOT / "data-policy.toml"
NOTICE_FILE = ROOT / "NOTICE.md"
SOURCE_NAME = "SOURCE.toml"
REUSE_NAME = "REUSE.toml"
EVIDENCE_DIR = "EVIDENCE"
MANIFEST = f"{EVIDENCE_DIR}/MANIFEST.sha256"
ORIGINS = {"external", "derived", "original"}
CACHE_DIR = ROOT / ".cache"

REQUIRED = {
    "external": ["id", "title", "publisher", "publisher_type", "url", "license", "license_url",
                 "terms", "content_kind", "modified", "concluded"],
    "derived": ["id", "title", "derived_from", "license"],
    "original": ["id", "title"],
}


# ---------- 共通（fetch_evidence.py からも使う） ----------

def load_policy() -> dict:
    return tomllib.loads(POLICY_FILE.read_text(encoding="utf-8"))


def repo_files() -> list[PurePosixPath]:
    """追跡中と、未追跡だが .gitignore されていないファイル。"""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout.decode()
    return sorted({PurePosixPath(p) for p in out.split("\0") if p and (ROOT / p).is_file()})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def payload_files(src_dir: PurePosixPath, files: list[PurePosixPath],
                  source_dirs: set[PurePosixPath]) -> list[PurePosixPath]:
    """src_dir が直接管轄するデータ本体（宣言・REUSE.toml・証拠・下位の宣言の管轄を除く）。"""
    out = []
    for f in files:
        if src_dir not in f.parents or governing_source(f, source_dirs) != src_dir:
            continue
        rel = f.relative_to(src_dir)
        if str(rel) in (SOURCE_NAME, REUSE_NAME) or rel.parts[0] == EVIDENCE_DIR:
            continue
        out.append(f)
    return out


def governing_source(path: PurePosixPath, source_dirs: set[PurePosixPath]):
    for parent in path.parents:
        if parent in source_dirs:
            return parent
    return None


def is_own(path: PurePosixPath, policy: dict) -> bool:
    """自作物とみなすファイルか（data-policy.toml の [own]）。"""
    own = policy.get("own", {})
    if path.suffix.lower().lstrip(".") in own.get("extensions", []):
        return True
    return any(fnmatch.fnmatch(str(path), p) for p in own.get("paths", []))


def pinned_file(spec: dict) -> Path:
    """URL から取得し、記録した sha256 と一致することを確かめたファイル（.cache/ に置く）。"""
    dest = CACHE_DIR / spec["url"].rsplit("/", 1)[-1]
    if not dest.exists() or sha256(dest) != spec["sha256"]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(spec["url"], headers={"User-Agent": "thought-experiments-check/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.write_bytes(r.read())
    if sha256(dest) != spec["sha256"]:
        raise RuntimeError(f"{spec['url']} の sha256 が data-policy.toml の記録と一致しない（差し替えの疑い）")
    return dest


def verify_tsr(manifest: Path, tsr: Path, policy: dict) -> str | None:
    """RFC 3161 トークンを検証する。問題があればエラーメッセージを返す。"""
    if not shutil.which("openssl"):
        return "openssl がないのでタイムスタンプを検証できない"
    tsa = policy.get("tsa", {})
    try:
        cafile, untrusted = pinned_file(tsa["cafile"]), pinned_file(tsa["untrusted"])
    except (OSError, RuntimeError) as e:
        return f"タイムスタンプ局の証明書を用意できない: {e}"
    cmd = ["openssl", "ts", "-verify", "-data", str(manifest), "-in", str(tsr),
           "-CAfile", str(cafile), "-untrusted", str(untrusted)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "Verification: OK" not in r.stdout:
        return "タイムスタンプの検証に失敗: " + (r.stderr or r.stdout).strip().splitlines()[-1]
    return None


# ---------- 個別の宣言の検査 ----------

def check_source(rel: PurePosixPath, src: dict, licenses: dict, policy: dict) -> list[str]:
    errs: list[str] = []
    if rel.parent == PurePosixPath("."):
        errs.append(f"{rel}: ルートに SOURCE.toml は置けない（全ファイルを一括で宣言できてしまう）")
    origin = src.get("origin")
    if origin not in ORIGINS:
        return errs + [f"{rel}: origin は {sorted(ORIGINS)} のいずれか（現在: {origin!r}）"]

    for key in REQUIRED[origin]:
        if key not in src or src[key] in ("", []):
            errs.append(f"{rel}: {key} がない")

    lic = src.get("license")
    if lic is not None and lic not in licenses:
        errs.append(f"{rel}: ライセンス {lic!r} は data-policy.toml で許可されていない")

    if origin != "external":
        return errs

    types = policy.get("publisher_types", {})
    if src.get("publisher_type") and src["publisher_type"] not in types:
        errs.append(f"{rel}: 提供者の種別 {src['publisher_type']!r} は data-policy.toml の publisher_types にない")
    errs += check_terms(rel, src, policy)
    errs += check_art13(rel, src, policy)
    for key in ("url", "license_url"):
        if key in src and not str(src[key]).startswith("https://"):
            errs.append(f"{rel}: {key} は https:// で始まる公開 URL にする")
    if lic in licenses and licenses[lic].get("attribution") and not src.get("attribution"):
        errs.append(f"{rel}: {lic} はクレジット表示が必要なので attribution を書く")
    if "modified" in src and not isinstance(src["modified"], bool):
        errs.append(f"{rel}: modified は true / false にする")
    if src.get("modified") is True and not src.get("modifications"):
        errs.append(f"{rel}: modified = true なら modifications に加工内容（と加工した主体）を書く")

    c = src.get("concluded")
    if isinstance(c, dict):
        for key in ("license", "by", "at", "basis", "third_party"):
            if not c.get(key):
                errs.append(f"{rel}: concluded.{key} がない")
        if c.get("license") and c.get("license") != lic:
            errs.append(f"{rel}: 宣言値 {lic!r} と確認値 {c.get('license')!r} が食い違う")
        tp = c.get("third_party")
        if tp is not None and tp != "none-indicated" and not isinstance(tp, list):
            errs.append(f"{rel}: concluded.third_party は \"none-indicated\" か、第三者の権利がある部分のリストにする")
        if isinstance(tp, list) and tp:
            errs.append(f"{rel}: 第三者の権利がある部分 {tp} を含むデータは使わない（その部分を除いてから取り込む）")
        if "at" in c and not isinstance(c["at"], dt.date):
            errs.append(f"{rel}: concluded.at は日付（例: 2026-11-20）にする")
    elif c is not None:
        errs.append(f"{rel}: concluded は表（[concluded]）にする")
    return errs


def check_terms(rel: PurePosixPath, src: dict, policy: dict) -> list[str]:
    """利用規約（data-policy.toml の [terms]）の登録と、規約の性質に対する方針を検査する。"""
    tid = src.get("terms")
    if not tid:
        return []
    t = policy.get("terms", {}).get(tid)
    if t is None:
        return [f"{rel}: 規約 {tid!r} が data-policy.toml の [terms] にない。本文を読んで登録する"]
    errs = []
    tp = policy.get("terms_policy", {})
    if t.get("base_license") not in ("*", src.get("license")):
        errs.append(f"{rel}: 規約 {tid} のライセンスは {t.get('base_license')!r} で、宣言 {src.get('license')!r} と一致しない")
    if t.get("url") and t["url"] != src.get("license_url"):
        errs.append(f"{rel}: license_url は規約 {tid} の url（{t['url']}）にする")
    if t.get("indemnity") and not tp.get("allow_indemnity", False):
        errs.append(f"{rel}: 規約 {tid}（{t.get('title')}）には求償条項がある。"
                    "提供者側の誤表示のリスクが利用者に移るため使わない（terms_policy.allow_indemnity）")
    if t.get("non_copyrightable") == "applies" and not tp.get("allow_non_copyrightable_applies", True):
        errs.append(f"{rel}: 規約 {tid} は著作物でないデータにも条件を課すため使わない"
                    "（terms_policy.allow_non_copyrightable_applies）")
    return errs


ART13_LICENSE = "LicenseRef-jp-copyright-art13"


def check_art13(rel: PurePosixPath, src: dict, policy: dict) -> list[str]:
    """著作権法13条（権利の目的とならない著作物）として扱うデータの条件。"""
    if src.get("license") != ART13_LICENSE:
        return []
    cfg = policy.get("art13", {})
    errs = []
    if src.get("terms") != "jp-copyright-art13":
        errs.append(f"{rel}: 13条の区分では terms = \"jp-copyright-art13\" にする")
    if src.get("art13_item") not in cfg.get("items", []):
        errs.append(f"{rel}: 13条のどの号に当たるかを art13_item に書く（{cfg.get('items')}）")
    if src.get("publisher_type") not in cfg.get("publisher_types", []):
        errs.append(f"{rel}: 13条の作成主体は国・地方公共団体の機関・独立行政法人等。"
                    f"publisher_type {src.get('publisher_type')!r} は当たらない")
    host = urllib.parse.urlsplit(str(src.get("url", ""))).hostname
    if host not in cfg.get("hosts", {}):
        errs.append(f"{rel}: 取得元 {host!r} は [art13.hosts] にない。公的機関が直接運営するサイトから取得し、"
                    "サイト規約を確認してから登録する（民間の例規集は編集物・独自規約があるため不可）")
    return errs


def check_third_party(src_dir: PurePosixPath, src: dict, payload: list[PurePosixPath],
                      policy: dict) -> list[str]:
    """著作物の部分を含み、規約が第三者の権利の処理を利用者に任せるデータには、提供者の明示の証拠を求める。"""
    rel = src_dir / SOURCE_NAME
    tp = policy.get("third_party", {})
    kinds = src.get("content_kind", [])
    errs = []
    if not isinstance(kinds, list) or any(k not in tp.get("kinds", []) for k in kinds):
        return [f"{rel}: content_kind は {tp.get('kinds')} から選んだリストにする"]
    creative = sorted(set(kinds) & set(tp.get("creative_kinds", [])))
    exts = set(tp.get("creative_extensions", []))
    found = sorted({f.suffix.lower().lstrip(".") for f in payload} & exts)
    if found and not creative:
        errs.append(f"{rel}: データに {found} のファイルがある。著作物の部分（image・document など）を content_kind に書く")
    if not (creative or found):
        return errs
    terms = policy.get("terms", {}).get(src.get("terms"), {})
    if terms.get("third_party_clearance", "user") != "user":
        return errs
    ev = src.get("concluded", {}).get("third_party_evidence")
    if not (isinstance(ev, dict) and str(ev.get("url", "")).startswith("https://") and ev.get("quote")):
        errs.append(f"{rel}: 著作物の部分 {creative or found} を含み、規約 {src.get('terms')} は第三者の権利の処理を"
                    "利用者に任せている。提供者が権利処理済・自作と明示している証拠を "
                    "[concluded] third_party_evidence = {url = \"https://…\", quote = \"原文\"} に書く。なければ使わない")
    return errs


def check_evidence(src_dir: PurePosixPath, src: dict, payload: list[PurePosixPath],
                   policy: dict) -> list[str]:
    """外部データの証拠: マニフェストとデータの一致、タイムスタンプ、カタログ照合。"""
    rel = src_dir / SOURCE_NAME
    base = ROOT / src_dir
    manifest, tsr = base / MANIFEST, base / (MANIFEST + ".tsr")
    hint = f"python3 tools/fetch_evidence.py {src_dir} を実行する"
    if not manifest.exists() or not tsr.exists():
        return [f"{rel}: 証拠（{MANIFEST} と .tsr）がない。{hint}"]

    errs: list[str] = []
    recorded: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            recorded[name.strip()] = digest
    for f in payload:
        name = str(f.relative_to(src_dir))
        if name not in recorded:
            errs.append(f"{f}: 証拠マニフェストに載っていない。{hint}")
        elif recorded[name] != sha256(ROOT / f):
            errs.append(f"{f}: 証拠を取った後に中身が変わっている。{hint}")
    for name in recorded:
        if not name.startswith(EVIDENCE_DIR + "/") and not (base / name).exists():
            if src.get("committed", True):
                errs.append(f"{rel}: マニフェストにある {name} がリポジトリにない")
    if (msg := verify_tsr(manifest, tsr, policy)):
        errs.append(f"{rel}: {msg}")

    ev_file = base / EVIDENCE_DIR / "evidence.json"
    ev = json.loads(ev_file.read_text(encoding="utf-8")) if ev_file.exists() else {}
    # 取得元の証拠: 第三者（Internet Archive）が保存した内容が、手元の写しと一致するか
    if not src.get("archive_note"):
        for name in ("url", "license_url"):
            a = ev.get("archives", {}).get(name, {})
            if not a.get("snapshot"):
                errs.append(f"{rel}: {name} の Internet Archive 保存がない。{hint}"
                            "（保存できない事情があれば archive_note に書く）")
            elif a.get("archived_sha256") != recorded.get(f"{EVIDENCE_DIR}/raw/{name}.body"):
                errs.append(f"{rel}: {name} の Internet Archive の保存内容が手元の写しと一致しない"
                            "（動的なページなどで一致しない事情があれば archive_note に書く）")
    # 第三者の権利を示す語（© やゼンリンなど）がデータにあれば、確認した結果を書かせる
    marks = ev.get("third_party_markers") or []
    if marks and not src.get("concluded", {}).get("third_party_note"):
        errs.append(f"{rel}: データに第三者の権利を示す語 {marks} がある。"
                    "確認した結果を [concluded] third_party_note に書く")
    cat = ev.get("catalog")
    if cat and cat.get("result") == "mismatch" and not src.get("catalog", {}).get("accept_mismatch"):
        errs.append(f"{rel}: カタログのライセンス {cat.get('licenses')} が宣言と一致しない"
                    "（承知で使うなら [catalog] accept_mismatch に理由を書く）")
    return errs


def check_lineage(sources: dict[str, tuple[PurePosixPath, dict]], licenses: dict) -> list[str]:
    errs: list[str] = []
    for rel, src in sources.values():
        if src.get("origin") != "derived":
            continue
        parents = src.get("derived_from", [])
        if not isinstance(parents, list):
            errs.append(f"{rel}: derived_from は id のリストにする")
            continue
        mine = licenses.get(src.get("license"), {})
        sa = set()
        for pid in parents:
            if pid not in sources:
                errs.append(f"{rel}: derived_from の {pid!r} に対応する SOURCE.toml がない")
                continue
            plic = sources[pid][1].get("license")
            pinfo = licenses.get(plic, {})
            if pinfo.get("share_alike"):
                sa.add(plic)
            # CC BY 3(a)(4) などの代わりの、より厳しい規則: 表示義務を落とすライセンスにしない
            if pinfo.get("attribution") and mine and not mine.get("attribution"):
                errs.append(f"{rel}: 元データ {pid}（{plic}）は表示義務があるので、"
                            f"表示義務のない {src.get('license')} にはできない")
            # ODbL 4.6 の代わりの、より厳しい規則: 派生物は必ずリポジトリに含めて提供する
            if pinfo.get("offer_derived") and src.get("committed", True) is False:
                errs.append(f"{rel}: 元データ {pid}（{plic}）は派生データの提供義務があるので committed = false にできない")
        if len(sa) > 1:
            errs.append(f"{rel}: 継承ライセンスが混在している {sorted(sa)}。組み合わせられない")
        elif sa and src.get("license") not in sa:
            (need,) = sa
            errs.append(f"{rel}: 元データが {need}（継承）なので license = \"{need}\" にする")
    return errs


# ---------- 生成物 ----------

def toml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def render_reuse(src: dict, sources: dict, policy: dict) -> str:
    me = policy["self"]
    if src.get("origin") == "external":
        holder = src.get("publisher", "")
    elif src.get("origin") == "derived":
        ups = [sources[p][1].get("publisher") for p in src.get("derived_from", []) if p in sources]
        holder = "; ".join([me["copyright"], *[u for u in ups if u]])
    else:
        holder = me["copyright"]
    lic = src.get("license") or me["license"]
    return "\n".join([
        "# 自動生成: python3 tools/check_data_policy.py --fix。手で編集しない（元は SOURCE.toml）。",
        "version = 1",
        "",
        "[[annotations]]",
        'path = "**"',
        f"SPDX-FileCopyrightText = {toml_str(holder)}",
        f"SPDX-License-Identifier = {toml_str(lic)}",
        "",
        "[[annotations]]",
        f'path = ["{SOURCE_NAME}", "{EVIDENCE_DIR}/**"]',
        f"SPDX-FileCopyrightText = {toml_str(me['copyright'])}",
        f"SPDX-License-Identifier = {toml_str(me['license'])}",
        "",
    ])


def render_root_reuse(policy: dict) -> str:
    """自作物だけに CC0 を宣言する。データディレクトリでは、その中の REUSE.toml が優先される。"""
    own, me = policy.get("own", {}), policy["self"]
    paths = [f"**/*.{e}" for e in own.get("extensions", [])]
    paths += [p for p in own.get("paths", []) if not p.startswith("LICENSES/")]
    return "\n".join([
        "# 自動生成: python3 tools/check_data_policy.py --fix。手で編集しない（元は data-policy.toml の [own]）。",
        "# 自作物だけに宣言する。それ以外を一括で宣言すると、出所の分からないファイルにも自作物のラベルが付いてしまう。",
        "version = 1",
        "",
        "# aggregate: ファイル内の SPDX スニペット（埋め込んだ外部データ）の宣言と合わせて扱う",
        "[[annotations]]",
        'precedence = "aggregate"',
        "path = [" + ", ".join(toml_str(p) for p in paths) + "]",
        f"SPDX-FileCopyrightText = {toml_str(me['copyright'])}",
        f"SPDX-License-Identifier = {toml_str(me['license'])}",
        "",
    ])


def render_notice(sources: dict[str, tuple[PurePosixPath, dict]]) -> str:
    lines = [
        "# NOTICE",
        "",
        "このリポジトリが利用している外部データとそのクレジット表示です。",
        "このファイルは `tools/check_data_policy.py --fix` が `SOURCE.toml` から生成します。手で編集しないでください。",
        "ライセンス本文は `LICENSES/`、ファイルごとのライセンスは各ディレクトリの `REUSE.toml` にあります。",
        "",
    ]
    external = [(rel, s) for rel, s in sources.values() if s.get("origin") == "external"]
    if not external:
        lines.append("現在、外部データは使っていません。")
    for rel, s in sorted(external, key=lambda x: x[1]["id"]):
        lines += [
            f"## {s.get('title', s['id'])}",
            "",
            f"- 提供者: {s.get('publisher', '')}",
            f"- 取得元: {s.get('url', '')}",
            f"- ライセンス: {s.get('license', '')}（{s.get('license_url', '')}）",
        ]
        if s.get("attribution"):
            lines.append(f"- クレジット: {s['attribution']}")
        if s.get("modified"):
            lines.append(f"- 加工内容: {s.get('modifications', '')}")
        lines += [f"- 宣言: `{rel}`", ""]
    return "\n".join(lines).rstrip() + "\n"


def sync(path: Path, content: str, fix: bool, label: str, errs: list[str]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return
    if fix:
        path.write_text(content, encoding="utf-8")
        print(f"{label} を再生成しました")
    else:
        errs.append(f"{label} が SOURCE.toml と一致しない。--fix で再生成する")


# ---------- main ----------

def main() -> int:
    args = sys.argv[1:]
    fix = "--fix" in args
    report = args[args.index("--report") + 1] if "--report" in args else None

    policy = load_policy()
    licenses: dict = policy.get("licenses", {})
    ignore_sources = list(policy.get("ignore_sources", []))

    files = repo_files()
    errs: list[str] = []

    sources: dict[str, tuple[PurePosixPath, dict]] = {}
    source_dirs: set[PurePosixPath] = set()
    for f in files:
        if f.name != SOURCE_NAME or any(fnmatch.fnmatch(str(f), p) for p in ignore_sources):
            continue
        source_dirs.add(f.parent)
        try:
            src = tomllib.loads((ROOT / f).read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            errs.append(f"{f}: TOML として読めない: {e}")
            continue
        errs += check_source(f, src, licenses, policy)
        sid = src.get("id")
        if sid in sources:
            errs.append(f"{f}: id {sid!r} が {sources[sid][0]} と重複している")
        elif sid:
            sources[sid] = (f, src)

    for f in files:
        if governing_source(f, source_dirs) is None and not is_own(f, policy):
            errs.append(f"{f}: 自作物の拡張子・パス（data-policy.toml の [own]）でなく、"
                        "SOURCE.toml の管轄下にもない。データなら出所を宣言する")

    errs += check_lineage(sources, licenses)

    # ファイルの形をしていないデータ（自作物のファイルに埋め込まれた表や数値）
    emb = policy.get("embedded", {})
    for f in files:
        if governing_source(f, source_dirs) is None and is_own(f, policy) \
                and not any(fnmatch.fnmatch(str(f), p) for p in emb.get("skip", [])):
            errs += embedded_data.scan(str(f), (ROOT / f).read_bytes(), sources, licenses, emb)

    for rel, src in sources.values():
        d = rel.parent
        sync(ROOT / d / REUSE_NAME, render_reuse(src, sources, policy), fix, str(d / REUSE_NAME), errs)
        if src.get("origin") == "external":
            payload = payload_files(d, files, source_dirs)
            errs += check_third_party(d, src, payload, policy)
            errs += check_evidence(d, src, payload, policy)

    sync(ROOT / REUSE_NAME, render_root_reuse(policy), fix, REUSE_NAME, errs)
    sync(NOTICE_FILE, render_notice(sources), fix, "NOTICE.md", errs)

    if report:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        Path(report).write_text(json.dumps({
            "commit": head.stdout.strip(),
            "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "ok": not errs,
            "errors": errs,
            "sources": {sid: {"path": str(rel), "origin": s.get("origin"), "license": s.get("license")}
                        for sid, (rel, s) in sorted(sources.items())},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errs:
        print("データ利用ポリシー違反（DATA_POLICY.md を参照）:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"データ利用ポリシー: OK（宣言 {len(sources)} 件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
