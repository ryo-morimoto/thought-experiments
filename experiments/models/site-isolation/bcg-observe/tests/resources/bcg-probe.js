// Probe for the optional browsing context group (BCG) swap in HTML
// "obtain a browsing context to use for a navigation response".
//
// Sequence: W opens on origin A -> W navigates top-level to DEST (B) ->
// B opens popup P (origin A, named) -> B does history.back() to A.
// Then A looks up P by name and P inspects its opener.
//
// Without a swap at A->B, A, B and P share one BCG, so A finds P by name and
// P's opener (the BC of W) now shows A (same-origin with P, readable).
// With a swap at A->B, B (and therefore P) live in a new BCG; A (back in the
// old BC) cannot find P by name.
//
// Requires: testharness, /common/utils.js, /common/dispatcher/dispatcher.js,
// /common/get-host-info.sub.js, remote-context-helper.js.

function bcgProbe({label, openerPresent, dest, noStore}) {
  const results = {};
  promise_test(async t => {
    const step = (name, p) => Promise.race([p, new Promise((_, rej) =>
        t.step_timeout(() => rej(new Error('STEP-TIMEOUT ' + name + ' ' +
                                            JSON.stringify(results))), 25000))]);
    const rcHelper = new RemoteContextHelper();
    const probeName = 'probe_' + token();
    const aHeaders = noStore ? [['Cache-Control', 'no-store']] : [];
    const W = await step('openW', rcHelper.addWindow(
        {origin: 'HTTPS_ORIGIN', headers: aHeaders},
        openerPresent ? {} : {features: 'noopener'}));
    results.before = await step('before', W.executeScript(() => {
      window.name = 'wname';
      window.__marker = 1;
      sessionStorage.setItem('k', 'v');
      return {name: window.name, hlen: history.length,
              hasOpener: window.opener !== null};
    }));
    const B = await step('navB', W.navigateToNew({origin: dest}));
    results.atB = await step('atB', B.executeScript(() => ({
      name: window.name, hlen: history.length,
      hasOpener: window.opener !== null, origin: location.origin})));
    const P = await step('openP', B.addWindow({origin: 'HTTPS_ORIGIN'}, {target: probeName}));
    await step('markP', P.executeScript(() => { window.__probe = true; }));
    await step('back', B.historyBack());
    results.after = await step('after', W.executeScript((pn) => {
      const r = {name: window.name, hlen: history.length,
                 ss: sessionStorage.getItem('k'),
                 bfcacheRestored: window.__marker === 1};
      const w = window.open('', pn);
      let found = false;
      try { found = !!(w && w.__probe === true); } catch (e) { found = 'err:' + e.name; }
      r.foundByName = found;
      if (w && found !== true) { try { w.close(); } catch (e) {} }
      return r;
    }, [probeName]));
    results.fromP = await step('fromP', P.executeScript(() => {
      const r = {openerNull: window.opener === null};
      try { r.openerClosed = window.opener.closed; } catch (e) { r.openerClosed = 'err:' + e.name; }
      try { r.openerHref = window.opener.location.href.replace(/\?.*/, '?…'); }
      catch (e) { r.openerHref = 'err:' + e.name; }
      return r;
    }));
    try { await step('closeP', P.executeScript(() => window.close())); } catch (e) {}
    try { await step('closeW', W.executeScript(() => window.close())); } catch (e) {}
    assert_true(results.after.foundByName === true,
                'SWAP-OBSERVED ' + JSON.stringify(results));
  }, `${label}: same BCG after A->B->back (PASS = no swap, FAIL = swap)`);

  promise_test(async t => {
    assert_unreached('OBS ' + JSON.stringify(results));
  }, `${label}: observations (always FAIL; message carries data)`);
}
