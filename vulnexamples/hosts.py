from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host('', 'vulnexamples.urls', name='default'),
    host('a1', 'a1_injection.urls', name='a1_injection'),
    host('a2', 'a2_broken_auth.urls', name='a2_broken_auth'),
    host('a7', 'a7_xss.urls', name='a7_xss'),
    host('a8', 'a8_insecure_deserialization.urls', name='a8_insecure_deserialization'),
)
