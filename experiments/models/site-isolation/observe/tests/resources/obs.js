// Observation reporting for experiments/models/site-isolation/observe.
// Each observation becomes a passing subtest named "OBS <row> :: <value>".
// Failures of the scenario itself become a failing "OBS-ERROR <row>" subtest,
// so nothing is asserted about the value.
setup({explicit_done: true});

const OBS_SEEN = {};
function obs(row, value) {
  // Subtest names must be unique within a file; repeated rows get a suffix.
  OBS_SEEN[row] = (OBS_SEEN[row] || 0) + 1;
  const tag = OBS_SEEN[row] > 1 ? `${row}#${OBS_SEEN[row]}` : row;
  test(() => {}, `OBS ${tag} :: ${value}`);
}
function obsError(row, e) {
  test(() => { throw e; }, `OBS-ERROR ${row}`);
}
// Run each [row, async () => value] in order.
async function runObs(list) {
  for (const [row, fn] of list) {
    try {
      obs(row, await fn());
    } catch (e) {
      obsError(row, e);
    }
  }
}
// fetch() outcome: response.type, or "error" on TypeError.
async function fetchOutcome(url, init, fetchFn = fetch, TypeErrorCtor = TypeError) {
  try {
    const r = await fetchFn(url, init);
    return r.type;
  } catch (e) {
    return (e instanceof TypeErrorCtor || e.name === "TypeError") ? "error" : "exc:" + e.name;
  }
}
// <img>/<script> load outcome: "load" or "error".
function elementOutcome(tag, url, crossOrigin) {
  return new Promise(resolve => {
    const el = document.createElement(tag);
    if (crossOrigin) el.crossOrigin = crossOrigin;
    el.src = url;
    el.onload = () => { el.remove(); resolve("load"); };
    el.onerror = () => { el.remove(); resolve("error"); };
    document.body.appendChild(el);
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
