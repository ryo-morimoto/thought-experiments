# WPT-style reproduction tests for held-out bugs: results

Run on 2026-11-21. WPT clone commit 31362d1, run with `./wpt run --headless` inside podman (`python:3.12-bookworm`). Driver scripts are in `driver/` and wptreport JSON is in `logs/`. Each assertion comes from a WHATWG algorithm. None of the assertions was taken from the bug's fix.

## Results

| # | Bug | Web-observable? | Test | Chrome 158 | Firefox 160.0.1 | Pre-fix build: result | Pre-fix detects the bug? |
|---|---|---|---|---|---|---|---|
| 1 | CVE-2025-3071 | yes (opener can read the DOM of a cross-origin popup) | `cve-2025-3071-aboutblank-back-origin.sub.https.html` | PASS | PASS | Chrome 134.0.6998.165: PASS | **No** |
| 43 | CVE-2026-8950 (fetch) | yes (server echoes the `Origin` header) | `cve-2026-8950-origin-after-xsite-redirect.sub.https.html` | PASS | PASS | Firefox 150.0: PASS | **No** |
| 43 | CVE-2026-8950 (form POST) | yes | `cve-2026-8950-form-post-origin-after-xsite-redirect.sub.https.html` | PASS | PASS | Firefox 150.0: PASS | **No** |
| 39 | CVE-2024-6611 | yes (server echoes the `Cookie` header) | `cve-2024-6611-samesite-cookie-xsite-iframe.sub.https.html` | PASS | PASS | Firefox 127.0.2: PASS | **No** (may be a vacuous pass, see below) |
| 2 | CVE-2024-9966 | yes in principle (whether CSP is enforced) | not written | - | - | - | - |
| 9 | CVE-2026-84355 | yes in principle (`navigation.entries()` / navigate event) | not written | - | - | - | - |
| 10 | CVE-2026-87516 | yes in principle (`history.length`) | not written | - | - | - | - |
| 38 | CVE-2024-5687 | **no**: a URL typed into the browser UI, Firefox Android | skipped | - | - | - | - |

As controls, every test also passed on the builds where its bug did not apply (Chrome 134 for the Firefox tests, Firefox 150 and 127 for the Chrome test).

**Result: none of the tests detected its bug on the pre-fix build.**

## Assertions and spec basis

- **#43**: the `Origin` header is `"null"`. The basis is Fetch "compute the redirect-taint", "serializing a request origin" and "append a request `Origin` header". The request has origin A, goes to cross-site B, and B answers with a 307 to A. The URL list is then [B, A], and A is not same site with B, so the redirect-taint is "cross-site".
  - First draft: A → B. This draft was wrong. With that URL list the taint stays "same-origin", because the request's origin is the same as the URL being redirected from, so the spec requires the real origin. Every build sent the real origin, so the draft failed on Chrome and Firefox alike. Reading the algorithm step by step caught the error.
  - Both the fetch variant and the form-POST variant pass on Firefox 150. Possible reasons:
    1. The inverted condition sits on a code path the tests do not reach, such as a top-level navigation, a different redirect status, or a same-site hop.
    2. The bug was fixed earlier than the table says.
- **#1**: after `about:blank` and then `back()`, reading the popup's DOM must throw `SecurityError`. The basis is HTML "determine the origin" and "apply the history step": the cross-origin entry gets its own origin back. The test does not know the internal trigger, document sequence number reuse, so Chrome 134 passing probably means the trigger was not hit. It does not show that the oracle is wrong.
- **#39**: no `ss_strict`/`ss_lax` cookie is sent on a navigation of a cross-site iframe. The basis is "determine the same-site mode" with the `Cookie` header. The first version timed out on every build because the popup was blocked. It now opens the popup with `test_driver.bless`. The test does not check that `ss_none` arrived. So a pass may only mean that no cookie was set or sent, for example because of third-party cookie blocking. That makes this result unconfirmed rather than a clean miss.

## Not done, and why

- **#2, #9, #10**: the effect can be seen in a web page, but the trigger depends on browser internals: a policy container kept on an error-page history entry, an origin worked out from the committed URL versus the real one, and the rule that replaces history entries for error pages. I could not build a reliable black-box setup for any of them within the time limit.
- **#38**: the only way in is a URL typed into the browser's own UI, which page content cannot do.
- **Pre-fix runs not done**: no pre-fix run for #2 (Chrome 129), and no pre-fix run of a Chromium 152 build for #9 and #10.
- **Two setup problems, now fixed**:
  - Running wpt on the host first recreated `_venv3`, which wiped the installed browsers. The container run then needed the gobject-introspection dev packages for PyGObject.
  - Python's `zipfile` dropped the exec bit on Chrome 134's `chrome_crashpad_handler`, so the first Chrome 134 run created no session.
