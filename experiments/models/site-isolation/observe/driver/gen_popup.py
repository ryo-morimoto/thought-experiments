"""Write the four PopupSevered observation tests (one per opener COOP header).

usage: python3 -I gen_popup.py <observe/tests dir>
Rows follow wpt-cases.tsv: for each opener, cross-origin, same-origin, same-site,
each with popup COOP unsafe-none, same-origin, same-origin-allow-popups.
"""
import os
import sys

OPENERS = [  # file stem, opener COOP header (None = no header), first row number
    ("popup-sap", "same-origin-allow-popups", 27),
    ("popup-so", "same-origin", 36),
    ("popup-un", "unsafe-none", 45),
    ("popup-unspec", None, 54),
]
ORIGINS = ["CROSS_ORIGIN", "SAME_ORIGIN", "SAME_SITE"]
COOPS = ["unsafe-none", "same-origin", "same-origin-allow-popups"]

PAGE = """<!DOCTYPE html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>OBS PopupSevered, opener COOP {label}</title>
<script src="/resources/testharness.js"></script>
<script src="/resources/testharnessreport.js"></script>
<script src="/common/dispatcher/dispatcher.js"></script>
<script src="/common/get-host-info.sub.js"></script>
<script src="/common/utils.js"></script>
<script src="/html/cross-origin-opener-policy/resources/common.js"></script>
<script src="/html/cross-origin-opener-policy/resources/popup-test.js"></script>
<script src="resources/obs.js"></script>
<body>
<script>
// Same popup URLs (getExecutorPath) and settle time (500 ms) as popup_test() in
// html/cross-origin-opener-policy/resources/popup-test.js. Value: TRUE when the
// popup is closed from the opener side and its opener is null, FALSE when it is
// open with a non-null opener, else the raw pair.
async function popupObs(origin, headers) {{
  const popup_token = token();
  const reply_token = token();
  const popup = window.open(getExecutorPath(popup_token, origin.origin, headers));
  send(popup_token, `send('${{reply_token}}', 'Popup loaded');`);
  if (await receive(reply_token) !== 'Popup loaded') throw new Error('no load');
  await sleep(500);
  const closed = popup.closed;
  const hasOpener = await getPopupHasOpener(popup_token);
  send(popup_token, `close()`);
  await sleep(100);
  if (closed && hasOpener === "false") return "TRUE";
  if (!closed && hasOpener === "true") return "FALSE";
  return `closed=${{closed}},opener=${{hasOpener}}`;
}}
runObs([
{rows}
]).then(done);
</script>
"""


def main():
    out = sys.argv[1]
    for stem, coop, first in OPENERS:
        rows = []
        n = first
        for origin in ORIGINS:
            for pc in COOPS:
                rows.append('  ["w%03d", () => popupObs(%s, {coop: "%s"})],' % (n, origin, pc))
                n += 1
        label = coop or "absent"
        with open(os.path.join(out, stem + ".https.html"), "w", encoding="utf-8") as f:
            f.write(PAGE.format(label=label, rows="\n".join(rows)))
        if coop:
            with open(os.path.join(out, stem + ".https.html.headers"), "w", encoding="utf-8") as f:
                f.write("Cross-Origin-Opener-Policy: %s\n" % coop)


main()
