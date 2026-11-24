# Dominance condition checked on every inventory path: results

For tree node B4. Written by a subagent; one rater. No spec text and no per-path verdicts are in
this repository.

## What was checked

The dominance condition: bytes enter a document (secure context, COEP `require-corp` or
`credentialless`) only after the base CORP check of HTTP fetch has run under that document's
policy (for nested navigations, also the navigation CORP check and the embedder-policy
adherence check), or the reuse key holds the consumer's policy, or the check runs on every use.

## Method

- Inputs: the 139 rows kept in `../boundary/paths.tsv`: fetch calls, re-entries, reuse sites,
  and other-spec exits that carry responses. Specs: HTML 0e292f4 and Fetch d7fc0fd (see
  `../extract/commits.txt`).
- For each row, the steps were read for three things:
  - where the bytes enter;
  - whether the CORP check (or CORS / same-origin mode, or the navigation checks) runs before
    that with the consumer as the request's client;
  - otherwise, what the reuse key holds and whether a check runs on each use.
- Rows with the same structure were judged together. An earlier held analysis (2026-11-22) was
  reused where the structure matched.
- A reuse read from a store whose key has no policy gets the verdict of the worst producer that
  can write to that store.
- Steps that only continue an entry already judged (for example, loading the document) count as
  holds. The entry row carries the verdict.
- Verdicts:
  - **holds**;
  - **not guaranteed by text**: the steps allow the entry without the check under the
    consumer's policy;
  - **undecidable**: prose latitude, an other-spec exit, or something left unresolved.

## Counts

| group | rows | holds | not guaranteed | undecidable |
|---|---|---|---|---|
| fetch calls | 49 | 41 | 4 | 4 |
| fetch-internal re-entries | 5 | 5 | 0 | 0 |
| reuse sites (stores and fields) | 80 | 60 | 20 | 0 |
| other-spec exits | 5 | 4 | 0 | 1 |
| **total** | **139** | **110** | **24** | **5** |

The 24 not-guaranteed rows fall into 4 structures. Most rows that hold do so for one of these
reasons:
- CORS or same-origin mode governs;
- the CORP check runs inside HTTP fetch after the cache and after the service worker;
- the store is per Document with the same producer and consumer;
- no bytes reach a document (pings, downloads, deferred fetches, icons).

## Undecidable categories

- Prose latitude in an element's fetching model: a "may use other means" permission that is
  not tied to Fetch's check.
- An other-spec exit where the bytes come from an object defined in another specification
  (File API, Media Source).

Outside the inventory, these were noted but not counted:
- moving elements between documents (DOM adoption, a primitive the inventory does not follow);
- response-supplied navigations that are not inventory rows.

## Where the per-path verdicts are

The user chose not to publish per-path verdicts. They are held outside the repository, with the
spec anchors for each row.

## Done condition

B4 ("dominance checked per path"): met for the 139 inventory rows. Each row has a verdict and
citations. The limits: one rater, approximate line anchors, and the prefetch verdict depends on
a reading of the WICG text made on 2026-11-22.
