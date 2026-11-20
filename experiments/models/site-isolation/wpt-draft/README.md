# Draft WPT: COEP credentialless + CORP internal check, varying request-includes-credentials

Status: draft only. Not submitted and not run.

File (paths mirror the WPT tree):

- `html/cross-origin-embedder-policy/credentialless/service-worker-coep-none-proxy-credentials.https.window.js`

## Behavior under test

In a document whose COEP is `credentialless`, an opaque (no-cors, cross-origin) response
that has no `Cross-Origin-Resource-Policy` header:

- is a network error when the response's *request-includes-credentials* is true, and
- is an opaque response when it is false.

## Spec basis

Fetch, "cross-origin resource policy internal check"
(https://fetch.spec.whatwg.org/#cross-origin-resource-policy-internal-check):

> If policy is null, then switch on embedderPolicyValue:
> "credentialless": Set policy to `same-origin` if: response's request-includes-credentials is true, or forNavigation is true.

Fetch, "Cross-Origin-Embedder-Policy allows credentials"
(https://fetch.spec.whatwg.org/#cross-origin-embedder-policy-allows-credentials):

> 1. Assert: request's origin is not "client".
> 2. If request's mode is not "no-cors", then return true.
> 3. If request's client is null, then return true.
> 4. If request's client's policy container's embedder policy's value is not "credentialless", then return true.
> 5. If request's origin is same origin with request's current URL's origin and request's redirect-taint is "same-origin", then return true.
> 6. Return false.

HTTP-network-or-cache fetch:

> If Cross-Origin-Embedder-Policy allows credentials with request returns false, then set includeCredentials to false.
> ...
> Set response's request-includes-credentials to includeCredentials.

HTTP fetch (where the CORP check is called):

> If either request's response tainting or response's type is "opaque", and the cross-origin resource policy check with request's origin, request's client, request's destination, and internalResponse returns blocked, then return a network error.
>
> The cross-origin resource policy check runs for responses coming from the network and responses coming from the service worker. ... request's client and the service worker can have different embedder policies.

HTML, embedder policy value "credentialless"
(https://html.spec.whatwg.org/multipage/browsers.html#embedder-policy-value):

> When this value is used, fetching cross-origin no-CORS resources omits credentials. In exchange, an explicit `Cross-Origin-Resource-Policy` header is not required. Other requests sent with credentials require the server's explicit permission through the CORS protocol or the `Cross-Origin-Resource-Policy` header.

### When can "credentialed + no CORP" reach a credentialless document?

The credentials mode is **not** rewritten. `fetch(url, {mode: "no-cors", credentials: "include"})`
keeps credentials mode "include", but includeCredentials is forced to false. The same holds for `<img>`
and other no-cors element fetches. `<img crossorigin="use-credentials">` is a CORS request, so it is
outside this check. So for a no-cors request whose *client* is the credentialless document,
request-includes-credentials is true only when its current URL is same-origin with
redirect-taint "same-origin". In that case the internal check passes anyway, because
`same-origin` matches. **A credentialless document's own network fetch cannot produce the
blocked case.**

The blocked case needs a response produced under a *different client* whose embedder
policy allows credentials, and then checked against the document's policy. The spec
names one such path: a **service worker** (its own client, COEP `unsafe-none`) fetches
the cross-origin no-cors resource with credentials and passes it to `respondWith()`.
HTTP fetch for the document then runs the CORP check with the document's client
(`credentialless`), and the check sees request-includes-credentials = true. Navigations
(forNavigation = true) are the other trigger, but they are a different condition and
already have tests (`iframe-coep-credentialless.https.window.js`).

## Test design

There is one COEP:unsafe-none service worker, scoped to `/common/dispatcher/executor.html`. It
proxies `/proxied?credentials=<mode>` to `fetch(cross_origin + "/common/blank.html", {mode: "no-cors", credentials: <mode>})`.
`/common/blank.html` has no `.headers` file, and wpt.live serves it without CORP.

| # | Document COEP | SW fetch credentials | Expected in document |
|---|---|---|---|
| 1 | credentialless | include | rejects with TypeError |
| 2 | credentialless | omit | resolves, `type === "opaque"` |
| 3 | unsafe-none (control) | include | resolves, `type === "opaque"` |
| 4 | credentialless, direct fetch without SW respondWith | include requested | resolves opaque, because credentials are stripped |

Subtests 1 and 2 differ only in request-includes-credentials. Subtest 3 shows that COEP
is the cause. Subtest 4 shows that the direct path cannot trigger the block.

## Why existing tests do not cover this as a minimal pair

- `credentialless/service-worker-coep-none-proxy.https.window.js` asserts case 1 (credentialed
  through an unsafe-none SW leads to "Document: Fetch error"). **This is the existing direct coverage of the
  blocking half.** It has no uncredentialed counterpart with the same SW, and no COEP:none control.
- `credentialless/service-worker-coep-credentialless-proxy.https.window.js` shows success, but
  it changes the *SW's* COEP and not the credentials mode. This conflates two variables.
- `credentialless/no-cors-omit.https.window.js` covers the direct `credentials: "omit"` success.
- `credentialless/fetch.https.window.js` and `image.https.window.js` assert which cookies are sent,
  not whether the CORP check passes or blocks.
- `fetch/cross-origin-resource-policy/*` tests CORP header values, not COEP credentialless.
- `html/document-isolation-policy/service-worker-coep-*-proxy.https.tentative.window.js` mirrors
  the above for Document-Isolation-Policy.

Possible upstream form: add subtests 2 and 3 to the existing
`service-worker-coep-none-proxy.https.window.js` rather than adding a new file.

## How to run

From a WPT checkout, copy the file into the same path, then:

```
./wpt serve   # then open https://web-platform.test:8443/html/cross-origin-embedder-policy/credentialless/service-worker-coep-none-proxy-credentials.https.window.html
./wpt run chrome html/cross-origin-embedder-policy/credentialless/service-worker-coep-none-proxy-credentials.https.window.js
./wpt run firefox html/cross-origin-embedder-policy/credentialless/service-worker-coep-none-proxy-credentials.https.window.js
```

## Open questions

1. Is request-includes-credentials preserved when the SW returns the Response through
   `respondWith()`? The spec passes the internal response through, so it should be. Engines
   may track this differently, for example on the network-layer response.
2. If a response is cached in CacheStorage by an unsafe-none SW and then served to a
   credentialless document, the bit comes from the original fetch. `cache-storage.https.window.js`
   may cover this. Check it before extending.
3. `coep_none` sends `Cross-Origin-Embedder-Policy: none`, which is not a valid token. It parses as
   the default `unsafe-none`. This matches the existing tests' convention, but `unsafe-none` would be clearer.
4. Subtest 4 runs in a document controlled by the SW (the fetch falls through to the network). Should it
   move to an uncontrolled document so that it is independent of SW fallback?
5. The tests run sequentially and share one SW registration. Check timeout headroom (`timeout=long`)
   on slow bots.
