from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host('', 'index.urls', name='default'),
    host('a1', 'a1_injection.urls', name='a1_injection'),
    host('a2', 'a2_broken_auth.urls', name='a2_broken_auth'),
    host('a3', 'a3_sensitive_data_exposure.urls', name='a3_sensitive_data_exposure'),
    host('a4', 'a4_xxe.urls', name='a4_xxe'),
    host('a5', 'a5_broken_access_control.urls', name='a5_broken_access_control'),
    host('a6', 'a6_security_misconfiguration.urls', name='a6_security_misconfiguration'),
    host('a7', 'a7_xss.urls', name='a7_xss'),
    host('a8', 'a8_insecure_deserialization.urls', name='a8_insecure_deserialization'),
)
