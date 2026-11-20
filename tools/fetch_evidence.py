#!/usr/bin/env python3
"""外部データの証拠を取る。依存は標準ライブラリと openssl だけ（ots があれば使う）。

    python3 tools/fetch_evidence.py <SOURCE.toml のあるディレクトリ>

やること:
  1. url と license_url の応答（本文とヘッダ）を EVIDENCE/raw/ に保存する。
     他人の著作物なのでコミットしない（.gitignore 済み）。手元で保管し、ハッシュだけ公開する。
  2. 同じ URL を Internet Archive の Save Page Now に送り、第三者による保存の URL を記録する。
     保存された生の内容（id_ 付き URL）を取り直し、手元の写しとハッシュが一致するかも記録する。
  3. [catalog] があれば、提供者のカタログ（CKAN / DataCite）のライセンス表記と照合する。
  4. データ本体と 1 の保存物の sha256 を EVIDENCE/MANIFEST.sha256 に書き、
     RFC 3161 タイムスタンプ（.tsr）を付ける。ots コマンドがあれば OpenTimestamps も付ける。
  5. 結果を EVIDENCE/evidence.json に書く。

ここで証明できるのは「このバイト列が時刻 T より前に存在した」と「第三者が T ごろにこの URL を保存した」まで。
提供者が権利者であることは証明できない（DATA_POLICY.md の「機械では確認できないこと」）。
"""

from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zlib
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_data_policy import (  # noqa: E402
    EVIDENCE_DIR, MANIFEST, ROOT, SOURCE_NAME, load_policy, payload_files, repo_files,
    sha256, verify_tsr,
)

UA = "thought-experiments-evidence/1.0 (+https://github.com/ryo-morimoto/thought-experiments)"


def get(url: str, timeout: int = 60, data: bytes | None = None, headers: dict | None = None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    return urllib.request.urlopen(req, timeout=timeout)


def save_raw(url: str, name: str, raw_dir: Path) -> None:
    with get(url) as r:
        body = r.read()
        head = f"{r.status} {r.reason}\nURL: {r.url}\n" + "".join(f"{k}: {v}\n" for k, v in r.headers.items())
    (raw_dir / f"{name}.body").write_bytes(body)
    (raw_dir / f"{name}.headers").write_text(head, encoding="utf-8")


def save_page_now(url: str) -> dict:
    try:
        with get("https://web.archive.org/save/" + url, timeout=180) as r:
            loc = r.headers.get("Content-Location")
            snap = urllib.parse.urljoin("https://web.archive.org", loc) if loc else r.url
            return {"snapshot": snap}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"snapshot": None, "error": str(e)}


def archived_digest(snapshot: str) -> dict:
    """Internet Archive が保存した生の内容（id_ 付き URL）を取得し、sha256 を返す。"""
    m = re.match(r"(https://web\.archive\.org/web/\d+)/(.+)", snapshot)
    if not m:
        return {"archived_sha256": None, "archive_error": f"想定外の保存 URL: {snapshot}"}
    raw = f"{m.group(1)}id_/{m.group(2)}"
    try:
        with get(raw, timeout=120) as r:
            body, enc = r.read(), (r.headers.get("Content-Encoding") or "").lower()
        # 手元の取得は圧縮なし。保存側が gzip で返すことがあるので、展開してから比べる
        if enc == "gzip" or body[:2] == b"\x1f\x8b":
            body = gzip.decompress(body)
        elif enc == "deflate":
            body = zlib.decompress(body)
        return {"archived_raw": raw, "archived_sha256": hashlib.sha256(body).hexdigest()}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"archived_raw": raw, "archived_sha256": None, "archive_error": str(e)}


def family(lic: str) -> str:
    """'CC-BY-4.0' -> 'cc-by'（バージョンを落とした系統名）。"""
    return re.sub(r"-\d+(\.\d+)*$", "", lic.lower())


def check_catalog(cat: dict, declared: str) -> dict:
    kind, url = cat.get("type"), cat.get("url", "")
    try:
        if kind == "ckan":
            with get(url) as r:
                res = json.load(r)["result"]
            found = [res.get("license_id")] + [x.get("license_id") for x in res.get("resources", [])]
        elif kind == "datacite":
            with get("https://api.datacite.org/dois/" + urllib.parse.quote(url, safe="")) as r:
                rights = json.load(r)["data"]["attributes"].get("rightsList", [])
            found = [x.get("rightsIdentifier") for x in rights]
        else:
            return {"type": kind, "result": "error", "error": "type は ckan か datacite"}
    except (urllib.error.URLError, KeyError, ValueError) as e:
        return {"type": kind, "url": url, "result": "error", "error": str(e)}
    ids = sorted({x for x in found if x})
    low = {x.lower() for x in ids}
    if declared.lower() in low:
        result = "match"
    elif family(declared) in low:
        result = "partial"   # 例: e-Gov の 'cc-by'。系統は一致するがバージョンが分からない
    elif not ids:
        result = "unknown"
    else:
        result = "mismatch"
    return {"type": kind, "url": url, "licenses": ids, "result": result}


def timestamp(manifest: Path, policy: dict) -> None:
    tsq = manifest.with_suffix(".tsq")
    subprocess.run(["openssl", "ts", "-query", "-data", str(manifest), "-sha256", "-cert",
                    "-out", str(tsq)], check=True, capture_output=True)
    with get(policy["tsa"]["url"], data=tsq.read_bytes(),
             headers={"Content-Type": "application/timestamp-query"}) as r:
        Path(str(manifest) + ".tsr").write_bytes(r.read())
    tsq.unlink()


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    d = PurePosixPath(Path(sys.argv[1]).resolve().relative_to(ROOT).as_posix())
    src = tomllib.loads((ROOT / d / SOURCE_NAME).read_text(encoding="utf-8"))
    if src.get("origin") != "external":
        print("origin = external のディレクトリだけが対象です", file=sys.stderr)
        return 2
    policy = load_policy()
    base = ROOT / d
    raw_dir = base / EVIDENCE_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    targets = {"url": src["url"], "license_url": src["license_url"]}
    for name, url in targets.items():
        print(f"取得: {url}")
        save_raw(url, name, raw_dir)

    files = repo_files()
    source_dirs = {f.parent for f in files if f.name == SOURCE_NAME}
    lines = [f"{sha256(ROOT / f)}  {f.relative_to(d)}" for f in payload_files(d, files, source_dirs)]
    lines += [f"{sha256(p)}  {p.relative_to(base).as_posix()}" for p in sorted(raw_dir.iterdir())]
    manifest = base / MANIFEST
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("RFC 3161 タイムスタンプを取得")
    timestamp(manifest, policy)
    if (msg := verify_tsr(manifest, Path(str(manifest) + ".tsr"), policy)):
        print(msg, file=sys.stderr)
        return 1
    ots = bool(shutil.which("ots")) and subprocess.run(["ots", "stamp", str(manifest)]).returncode == 0

    archives = {}
    for name, url in targets.items():
        print(f"Save Page Now: {url}")
        a = {"url": url, **save_page_now(url)}
        if a.get("snapshot"):
            a.update(archived_digest(a["snapshot"]))
            local = sha256(raw_dir / f"{name}.body")
            a["matches_local"] = a.get("archived_sha256") == local
        archives[name] = a

    ev = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "tsa": policy["tsa"]["url"],
        "opentimestamps": ots,
        "archives": archives,
    }
    if "catalog" in src:
        ev["catalog"] = check_catalog(src["catalog"], src.get("license", ""))
        print(f"カタログ照合: {ev['catalog'].get('result')} {ev['catalog'].get('licenses', '')}")
    (base / EVIDENCE_DIR / "evidence.json").write_text(
        json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name, a in archives.items():
        if not a.get("snapshot"):
            print(f"警告: {name} を Internet Archive に保存できなかった（{a.get('error')}）。後で再実行する",
                  file=sys.stderr)
        elif not a.get("matches_local"):
            print(f"警告: {name} の Internet Archive の保存内容が手元の写しと一致しない"
                  f"（{a.get('archive_error') or '内容が異なる'}）。動的なページなら事情を archive_note に書く",
                  file=sys.stderr)
    if not ots:
        print("注意: ots コマンドがないので OpenTimestamps は付けていない", file=sys.stderr)
    print(f"証拠を {d / EVIDENCE_DIR} に書きました。EVIDENCE/raw/ はコミットせず手元で保管してください")
    return 0


if __name__ == "__main__":
    sys.exit(main())
