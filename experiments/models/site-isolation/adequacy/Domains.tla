------------------------------ MODULE Domains ---------------------------------
(* adequacy/RESULTS.md: larger origin domains for ../SpecIsolation.tla.      *)
(* Origins are records [scheme, host, site] as in SpecIsolation; the apex    *)
(* host of a site has the site's name (as OA's "a.test").                    *)
EXTENDS Naturals, FiniteSets, Sequences
Og(s, h, st) == [scheme |-> s, host |-> h, site |-> st]
\* All schemes x hosts of the given sites.
Dom(sites, subs) ==
  {Og(s, IF sub = "" THEN st ELSE sub \o "." \o st, st) :
     s \in {"https", "http"}, st \in sites, sub \in subs}
\* D18: 3 sites x 3 hosts (apex, www1, www2) x 2 schemes.
D18 == Dom({"a.test", "b.test", "c.test"}, {"", "www1", "www2"})
\* D12: the domain this note argues realizes every relational type of up to
\* 3 origins: site a 3 hosts, site b 2 hosts, site c 1 host, x 2 schemes.
D12 == Dom({"a.test"}, {"", "www1", "www2"}) \cup Dom({"b.test"}, {"", "www1"})
       \cup Dom({"c.test"}, {""})
\* D32: 4 sites x 4 hosts x 2 schemes (every type of up to 4 origins).
D32 == Dom({"a.test", "b.test", "c.test", "d.test"}, {"", "www1", "www2", "www3"})
===============================================================================
