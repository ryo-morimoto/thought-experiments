# 下書きの試験を実ブラウザで動かした結果

思考実験 [experiments/2026-11-20-browser-semantics-soundness.md](../../../2026-11-20-browser-semantics-soundness.md) のために、subagent が 2026-11-21 にコンテナの中で動かした（ユーザーの判断: 下書きを `wpt serve` で動かす）。筆者は wptreport 形式のログを要約スクリプトで読み直して確かめた。ログ自体はコミットしていない。

## 環境

- イメージ: `docker.io/library/python:3.12-bookworm`（ブラウザの共有ライブラリのために Debian の chromium と firefox-esr を apt で入れた）
- WPT: `31362d12238db2b16efda9643953d6e4630caf7b`（浅い clone、master）
- Chrome for Testing 158.0.8127.36（chromedriver 同版）、`--binary-arg=--no-sandbox`、表示なし
- Firefox 160.0.1、geckodriver、`--headless`
- 実行: `./wpt run --yes --headless --log-wptreport=... <product> <tests>`

## 修正したこと

最初の下書きと、既存の `service-worker-coep-none-proxy.https.window.js` は、Firefox で準備の段が止まった。service worker の中で `serviceWorker.state` を読んでいるが、Firefox は `ServiceWorkerGlobalScope.serviceWorker` を実装していない（`ReferenceError: serviceWorker is not defined`）。下書きは `registration.active.state` に直した。下の結果は、この直した版（既存の試験も同じ箇所だけ直した写し）で取った。

## 結果

| 小試験 | Chrome 158 | Firefox 160 |
| --- | --- | --- |
| 準備: COEP unsafe-none の service worker | PASS | PASS |
| 1. credentialless の文書、資格情報つき、CORP 無し → 失敗 | PASS | FAIL（`doc:TypeError` を期待、`doc:opaque` だった） |
| 2. credentialless の文書、資格情報なし、CORP 無し → opaque | PASS | PASS |
| 3. 対照: unsafe-none の文書、資格情報つき → opaque | PASS | PASS |
| 4. 文書から直接 `credentials:"include"` → opaque | PASS | PASS |
| 既存の `service-worker-coep-none-proxy`（同じ箇所を直した写し） | PASS | FAIL（「Fetch error」を期待、「Fetch success」だった） |

Chrome は、下書きが前提にした仕様の読み（service worker が資格情報つきで取った応答は、credentialless の文書では CORP の検査で遮断される）どおりに動いた。Firefox は遮断しなかった。既存の試験も同じように失敗するので、下書きの誤りではなく Firefox の振る舞い。service worker の `respondWith()` を通るときに「要求が資格情報を含んだ」という印を保っていないか、文書の方針で CORP の検査をしていない、のどちらかと考えられる（未確認）。wpt.fyi 上の既存の試験の Firefox の結果は、確かめていない。
