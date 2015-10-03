# Fix for Python 2.7.6 with ssl handshake error: (no need for Python 3.x)
# See: https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
