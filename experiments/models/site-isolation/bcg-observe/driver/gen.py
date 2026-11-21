import os, sys
out = sys.argv[1]
T = """<!DOCTYPE html>
<meta charset=utf-8>
<meta name="timeout" content="long">
<title>BCG swap probe: {n}</title>
<script src="/resources/testharness.js"></script>
<script src="/resources/testharnessreport.js"></script>
<script src="/common/utils.js"></script>
<script src="/common/dispatcher/dispatcher.js"></script>
<script src="/common/get-host-info.sub.js"></script>
<script src="/html/browsers/browsing-the-web/remote-context-helper/resources/remote-context-helper.js"></script>
<script src="resources/bcg-probe.js"></script>
<script>
bcgProbe({c});
</script>
"""
cases = {
 "c1-noopener-crosssite": "{label: 'c1 noopener cross-site', openerPresent: false, dest: 'HTTPS_NOTSAMESITE_ORIGIN'}",
 "c2-noopener-samesite": "{label: 'c2 noopener same-site cross-origin', openerPresent: false, dest: 'HTTPS_REMOTE_ORIGIN'}",
 "c3-noopener-sameorigin": "{label: 'c3 noopener same-origin', openerPresent: false, dest: 'HTTPS_ORIGIN'}",
 "c4-opener-crosssite": "{label: 'c4 opener cross-site', openerPresent: true, dest: 'HTTPS_NOTSAMESITE_ORIGIN'}",
 "c5-noopener-crosssite-nostore": "{label: 'c5 noopener cross-site, A no-store', openerPresent: false, dest: 'HTTPS_NOTSAMESITE_ORIGIN', noStore: true}",
 "c6-noopener-samesite-nostore": "{label: 'c6 noopener same-site, A no-store', openerPresent: false, dest: 'HTTPS_REMOTE_ORIGIN', noStore: true}",
}
for n, c in cases.items():
    open(os.path.join(out, n + ".https.html"), "w").write(T.format(n=n, c=c))
print("\n".join(sorted(cases)))
