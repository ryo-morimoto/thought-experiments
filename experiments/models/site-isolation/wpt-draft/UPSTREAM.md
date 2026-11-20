# 上流への報告の下書き（未送信）

思考実験 [experiments/2026-11-20-browser-semantics-soundness.md](../../../2026-11-20-browser-semantics-soundness.md) の過程で見つけた Firefox の振る舞いについて、送るかどうかをユーザーが決めるための下書き。どれもまだ送っていない。

## 判断の要約

- 仕様の読みの違いではない。応答の request-includes-credentials は既定で true で、service worker の respondWith が応答をどう写しても、仕様どおりなら遮断になる。Chrome 158 も遮断する。
- 機能の欠如でもない。Firefox は credentialless を 119 から既定で有効にしている（MDN の browser-compat-data）。文書から直接の取得の小試験も通る。require-corp なら service worker の応答にも CORP の検査をしている（wpt.fyi で 13/13）。
- したがって Firefox の実装の欠陥（credentialless かつ service worker が渡した応答の経路）と考えられる。Gecko のソースは確かめていない。
- 既存の報告: Bugzilla 1760782（wpt-sync が自動で起こした、TIMEOUT としか書かれていない未整理のバグ）。1560488（ServiceWorkerGlobalScope.serviceWorker が無いことの報告）。原因まで書いた報告は見つからなかった。
- 仕様への issue は要らない（仕様の文は一意）。

## 下書き 1: Bugzilla（新しいバグ、または 1760782 へのコメント）

Component 案: Core :: DOM: Service Workers（または DOM: Security）

> **COEP: credentialless does not block a credentialed, CORP-less no-cors response supplied by a COEP: unsafe-none service worker**
>
> Steps: a document with `Cross-Origin-Embedder-Policy: credentialless` is controlled by a service worker whose COEP is unsafe-none. The SW fetches a cross-origin no-cors resource without `Cross-Origin-Resource-Policy` using `credentials: "include"` and returns it with `respondWith()`. The document's `fetch(url, {mode: "no-cors"})` resolves with an opaque response.
>
> Expected: a network error. Fetch's HTTP fetch runs the CORP check on service-worker responses using the client's embedder policy ("request's client and the service worker can have different embedder policies"); the internal check sets policy to `same-origin` for `credentialless` when the response's request-includes-credentials is true, which it is (set by the SW's own HTTP-network-or-cache fetch, and true by default).
>
> Actual (Firefox 160.0.1): opaque response. Chrome 158 returns a network error. With `credentials: "omit"` both return opaque; a COEP: unsafe-none control document gets opaque in both.
>
> This is likely the real failure behind the TIMEOUT in bug 1760782: `service-worker-coep-none-proxy.https.window.js` uses `serviceWorker.state` inside the service worker, which Firefox does not implement (bug 1560488), so the test hangs before reaching this assertion. With that line replaced by `registration.active.state`, the test reaches the assertion and fails ("Document: Fetch success" instead of "Document: Fetch error").
>
> Reduced test (minimal pair plus control): attached `service-worker-coep-none-proxy-credentials.https.window.js`.

## 下書き 2: web-platform-tests の PR

> **credentialless SW proxy tests: avoid `ServiceWorkerGlobalScope.serviceWorker`**
>
> `service-worker-coep-none-proxy.https.window.js` and `service-worker-coep-credentialless-proxy.https.window.js` send `serviceWorker.state` from inside the service worker. Firefox does not implement `ServiceWorkerGlobalScope.serviceWorker`, so both tests time out in setup and never reach their assertions. Use `registration.active.state` instead. With this change, Firefox 160 reaches the assertions (the none-proxy test then fails on a real behavior difference, tracked in Bugzilla).
>
> Optionally add the minimal-pair subtests from the attached draft (same SW, only the credentials mode differs).

## 送る前に要るもの

- Bugzilla と GitHub のアカウント（ユーザー本人のもの）。
- 下書きの試験を、既存のファイルへの小試験の追加にするか、新しいファイルにするかの判断（WPT の慣習では追加が好まれそう）。
