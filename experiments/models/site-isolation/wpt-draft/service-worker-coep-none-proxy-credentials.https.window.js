// META: timeout=long
// META: script=/common/get-host-info.sub.js
// META: script=/common/utils.js
// META: script=/common/dispatcher/dispatcher.js
// META: script=./resources/common.js
// META: script=/service-workers/service-worker/resources/test-helpers.sub.js

// Fetch "cross-origin resource policy internal check":
//   If policy is null, switch on embedderPolicyValue:
//     "credentialless": Set policy to `same-origin` if response's
//     request-includes-credentials is true, or forNavigation is true.
// https://fetch.spec.whatwg.org/#cross-origin-resource-policy-internal-check
//
// From a COEP:credentialless document, a cross-origin no-cors request never
// includes credentials ("Cross-Origin-Embedder-Policy allows credentials"
// returns false), so request-includes-credentials can only be true for such a
// response when it was produced by a different client: here, a COEP:unsafe-none
// ServiceWorker that fetches it and hands it back via respondWith(). The
// document's HTTP fetch then runs the CORP check against the *document's*
// embedder policy (https://fetch.spec.whatwg.org/#concept-http-fetch).
//
// The only variable between subtests 1 and 2 is the credentials mode of the
// ServiceWorker's fetch, i.e. response's request-includes-credentials.
// The response (/common/blank.html) has no Cross-Origin-Resource-Policy header.

const cross_origin = get_host_info().HTTPS_REMOTE_ORIGIN;

// Register one COEP:unsafe-none ServiceWorker controlling executor documents.
// It proxies "/proxied?credentials=<mode>" to a cross-origin no-cors fetch
// using <mode>.
let sw_registration;
promise_test(async test => {
  const reply = token();
  const sw_token = token();
  const sw_url = executor_service_worker_path + coep_none + `&uuid=${sw_token}`;
  sw_registration =
    await service_worker_unregister_and_register(test, sw_url, executor_path);
  add_completion_callback(() => sw_registration.unregister());
  await wait_for_state(test, sw_registration.installing, 'activated');

  send(sw_token, `
    fetchHandler = event => {
      const url = new URL(event.request.url);
      if (url.pathname !== "/proxied")
        return;
      const credentials = url.searchParams.get("credentials");
      const reply = url.searchParams.get("reply");
      event.respondWith((async () => {
        try {
          const response = await fetch("${cross_origin}/common/blank.html", {
            mode: "no-cors",
            credentials,
          });
          send(reply, "sw:" + response.type);
          return response;
        } catch (e) {
          send(reply, "sw:error");
          return new Response("", {status: 400});
        }
      })());
    };
    await clients.claim();
    send("${reply}", registration.active.state);
  `);
  assert_equals(await receive(reply), "activated");
}, "Setup: COEP:unsafe-none ServiceWorker proxying cross-origin no-cors");

// Opens a document with |coep_headers| controlled by the ServiceWorker, makes
// it fetch "/proxied" (no-cors), and returns [sw_result, document_result].
const proxiedFetch = async (coep_headers, credentials) => {
  const sw_reply = token();
  const doc_reply = token();
  const [doc_token] = environments["document"](coep_headers);
  send(doc_token, `
    try {
      const r = await fetch(
        "/proxied?credentials=${credentials}&reply=${sw_reply}",
        {mode: "no-cors"});
      send("${doc_reply}", "doc:" + r.type);
    } catch (e) {
      send("${doc_reply}", "doc:" + e.name);
    }
  `);
  return [await receive(sw_reply), await receive(doc_reply)];
};

promise_test(async () => {
  const [sw, doc] = await proxiedFetch(coep_credentialless, "include");
  assert_equals(sw, "sw:opaque", "ServiceWorker (COEP:unsafe-none) fetch");
  assert_equals(doc, "doc:TypeError",
    "request-includes-credentials=true, no CORP => blocked in document");
}, "COEP:credentialless document, credentialed no-cors response without " +
   "CORP is a network error");

promise_test(async () => {
  const [sw, doc] = await proxiedFetch(coep_credentialless, "omit");
  assert_equals(sw, "sw:opaque", "ServiceWorker (COEP:unsafe-none) fetch");
  assert_equals(doc, "doc:opaque",
    "request-includes-credentials=false, no CORP => allowed in document");
}, "COEP:credentialless document, uncredentialed no-cors response without " +
   "CORP is an opaque response");

// Control: same credentialed response, document without COEP.
promise_test(async () => {
  const [sw, doc] = await proxiedFetch(coep_none, "include");
  assert_equals(sw, "sw:opaque", "ServiceWorker (COEP:unsafe-none) fetch");
  assert_equals(doc, "doc:opaque", "COEP:unsafe-none => CORP not required");
}, "Control: COEP:unsafe-none document, credentialed no-cors response " +
   "without CORP is an opaque response");

// Direct path (no ServiceWorker involvement in the response): the document
// asks for credentials:"include", but "Cross-Origin-Embedder-Policy allows
// credentials" forces includeCredentials=false, so the response is allowed.
// Uses a URL outside the ServiceWorker's "/proxied" filter (falls through to
// network).
promise_test(async () => {
  const doc_reply = token();
  const [doc_token] = environments["document"](coep_credentialless);
  send(doc_token, `
    try {
      const r = await fetch("${cross_origin}/common/blank.html?${token()}",
                            {mode: "no-cors", credentials: "include"});
      send("${doc_reply}", "doc:" + r.type);
    } catch (e) {
      send("${doc_reply}", "doc:" + e.name);
    }
  `);
  assert_equals(await receive(doc_reply), "doc:opaque");
}, "COEP:credentialless document, direct no-cors credentials:'include' " +
   "fetch is sent without credentials and is not blocked by CORP");
