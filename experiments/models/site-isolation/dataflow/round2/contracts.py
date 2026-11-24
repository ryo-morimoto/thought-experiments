"""Stated contracts and the author's reading of the residual items (round 2).

Each entry is an assumption the analysis states instead of counting a hole.
Labels only; no spec text. `mw` = may write a model-read concept:
'n' (no, by the reading in `why`), '?' (cannot tell), 'c' (only through the
named contract, which the properties assume).
"""

CONTRACTS = {
    'C1': 'A call into another spec is a function of its arguments and writes no HTML/Fetch '
          'struct field, except as listed in inputs.tsv (Infra position variables, URL setters, '
          'Streams set-up, Fetch Metadata headers).',
    'C2': 'Script run by events, promises or callbacks reaches HTML/Fetch state only through IDL '
          'entry points, which are outside this closure.',
    'C3': 'No WebDriver BiDi remote end intercepts (BiDi network interception can rewrite '
          'requests and supply responses).',
    'C4': 'Per-type hooks ("X steps" defined per element type or by another spec) write no '
          'model-read concept.',
    'C5': 'User-agent state outside HTML/Fetch structs (event loop and task queues, JS execution '
          'context stack, DOM tree, focus, rendering, CSS, downloads) is not read by the model.',
    'C6': 'The network and the HTTP cache are inputs (any response); the model quantifies responses.',
    'C7': 'Prose-bound names (lambdas, existential bindings, named arguments of another spec) '
          'are bound as the prose says; the author read each one.',
}

# (algorithm, step) -> (contract or 'reading', value-writing y/n, mw, why)
STEPS = {
    # prose-only steps on relevant paths
    ('HTTP-network-or-cache fetch', '15.1'): ('reading', 'n', 'n', 'editorial note, no effect'),
    ('HTTP-network-or-cache fetch', '16.2'): ('reading', 'n', 'n', 'editorial note, no effect'),
    ('HTTP-network-or-cache fetch', '16.4'): ('C6', 'y', 'n', 'stores a proxy-authentication entry'),
    ('StructuredDeserialize', '22.13'): ('C5', 'y', 'n', 'attaches data to a deserialized value'),
    ('create a document to display a user agent page or PDF viewer inline', '6'):
        ('reading', 'y', 'n', 'document content or rendering; policies are set in earlier steps'),
    ('focus update steps', '4.1.2'): ('C5', 'y', 'n', 'focus state'),
    ('get the suggested filename', '14'): ('C5', 'y', 'n', 'download filename'),
    ('load a multipart/x-mixed-replace document', '1'):
        ('reading', 'y', 'n', 'parses the body into parts; part documents reuse the copied navigation params '
                              '(step 3) or go through navigate (step 5); checked in html.src'),
    ('parse a sizes attribute', '3.5'): ('C5', 'y', 'n', 'media condition evaluation (CSS)'),
    ('parse a srcset attribute', '4'): ('reading', 'y', 'n', 'parser position'),
    ('parse a srcset attribute', '8.2'): ('reading', 'y', 'n', 'parser position'),
    ('potentially reset the focus', '12'): ('C5', 'y', 'n', 'focus navigation starting point'),
    ('respond to base URL changes', '2'): ('C5', 'y', 'n', 'CSS link pseudo-class state'),
    ('rules for parsing floating-point number values', '13'): ('reading', 'n', 'n', 'label with sub-steps'),
    ('run a classic script', '8.1.2'): ('reading', 'n', 'n', 'rethrow (control)'),
    ('scroll to the fragment', '3.7'): ('C5', 'y', 'n', 'focus navigation starting point'),
    ('stops parsing', '13'): ('reading', 'n', 'n', 'states readiness; no field'),
    ('terminate a worklet global scope', '5'): ('C5', 'y', 'n', 'destroys an event loop'),
    ('update document for history step application', '9.4'): ('C2', 'n', 'c', 'scripts may run'),
    # unresolved links: constants or inline editorial notes
    ('create navigation params by fetching', '3'): ('reading', 'n', 'n', 'inline issue note'),
    ('evaluate a javascript: URL', '15'): ('reading', 'n', 'n', 'inline issue note'),
    ('navigate to a javascript: URL', '11'): ('reading', 'n', 'n', 'inline issue note'),
    ('hyperlink referrer policy', '1'): ('reading', 'n', 'n', 'concept term'),
    ('potentially reset the focus', '6'): ('reading', 'n', 'n', 'enum value'),
    ('build not restored reasons for document state', '4.2'): ('reading', 'n', 'n', 'attribute name'),
    ('unload', '5'): ('reading', 'n', 'n', 'inline note'),
    ('parse a sizes attribute', '3.2'): ('reading', 'n', 'n', 'CSS grammar term'),
    # callbacks the name rules do not bind
    ('process early hint headers', '5'): ('reading', 'y', 'n', 'returned callback given a document; commits preloads'),
    ('process the `Speculation-Rules` header', '3.4.2.2'): ('reading', 'y', 'n', 'speculation rules body'),
    ('fully read', '2'): ('reading', 'y', 'n', 'body bytes to success steps'),
    ('HTTP fetch', '3.2.2'): ('reading', 'y', 'n', 'request body chunk callback'),
    ('fetch', '11.2'): ('reading', 'y', 'n', 'bound by the callback-argument rule in round 2'),
    ('consume a preloaded resource', '8'): ('reading', 'y', 'n', 'bound by the callback-argument rule in round 2'),
    # collection ops and other write verbs
    ('load a media document', '4'): ('C5', 'y', 'n', 'DOM tree'),
    ('destroy', '5'): ('C5', 'y', 'n', 'task queues'),
    ('set', '1'): ('reading', 'y', 'n', 'removes duplicate headers from the header list argument'),
    ('HTTP fetch', '3.2.2.3'): ('C1', 'y', 'n', 'stream chunk (Streams)'),
    ('create a new realm', '3'): ('C5', 'y', 'n', 'JS execution context stack'),
    ('HTTP-network-or-cache fetch', '8.20'): ('reading', 'y', 'n', 'request header list per HTTP (not read by the model)'),
    ('HTTP-network-or-cache fetch', '11.5.2'): ('C6', 'y', 'n', 'HTTP cache store'),
}

# residual havoc gap rows whose target no rule places
GAP = {
    ('serialize a response URL for reporting', '3'): ('C1', 'URL setter (username)'),
    ('serialize a response URL for reporting', '4'): ('C1', 'URL setter (password)'),
    ('sanitize a URL to send in a report', '2'): ('C1', 'URL setter (username)'),
    ('sanitize a URL to send in a report', '3'): ('C1', 'URL setter (password)'),
    ('HTTP-network-or-cache fetch', '15.3.3'): ('C1', 'URL setter (username)'),
    ('HTTP-network-or-cache fetch', '15.3.4'): ('C1', 'URL setter (password)'),
    ('fetch response handover', '9.3'): ('C1', 'Streams set-up'),
    ('HTTP fetch', '3.2.3'): ('C1', 'Streams set-up'),
    ('HTTP-network fetch', '14'): ('C1', 'Streams set-up'),
    ('HTTP-network-or-cache fetch', '8.13'): ('C1', 'Fetch Metadata appends request headers'),
    ('HTTP-network-or-cache fetch', '11.5.2'): ('C6', 'HTTP cache store'),
    ('navigate to a fragment', '18'): ('C5', 'queues a task (steps analysed in place)'),
    ('URL and history update steps', '14'): ('C5', 'queues a task (steps analysed in place)'),
    ('load a media document', '4'): ('C5', 'DOM tree'),
    ('destroy', '5'): ('C5', 'task queues'),
    ('create a new realm', '3'): ('C5', 'JS execution context stack'),
    ('prepare to run script', '1'): ('C5', 'JS execution context stack'),
    ('clean up after running script', '2'): ('C5', 'JS execution context stack'),
    ('spin the event loop', '4'): ('C5', 'JS execution context stack'),
    ('spin the event loop', '6.2.1'): ('C5', 'event loop task'),
}

# relevant locals that no rule binds
UNBOUND = {
    'HTTP-network fetch::body': ('C6', 'n', 'bound inside "making an HTTP request" (network)'),
    'append a request `Origin` header::scheme': ('C7', 'n', 'prose binding; affects the Origin header only'),
    'get a structured field value::input_string': ('C7', 'n', 'named argument of RFC 9651, not a var'),
    'get a structured field value::header_type': ('C7', 'n', 'named argument of RFC 9651, not a var'),
    'StructuredSerializeInternal::subValue': ('C7', 'n', 'prose lambda parameter'),
    'StructuredDeserialize::subSerialized': ('C7', 'n', 'prose lambda parameter'),
    'steps to fire beforeunload::event': ('C7', 'n', 'prose binding (event created in prose)'),
    'update the navigation API entries for reactivation::matchingOldNHE': ('C7', 'n', 'existential binding'),
    'abort the ongoing navigation::reason': ('C7', 'n', 'optional parameter defaulted in prose'),
    'run a module script::reason': ('C7', 'n', 'promise rejection reason (prose)'),
}
