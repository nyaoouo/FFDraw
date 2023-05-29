import requests

PROXY_TEST_INV = 0
PROXY_TEST_PROCESS = 1
PROXY_TEST_SUCCESS = 2
PROXY_TEST_FAIL = 3
PROXY_TEST_TARGET_HTTP = 'http://www.github.com'
PROXY_TEST_TARGET_HTTPS = 'https://www.github.com'


def test_connection(target, proxy=None):
    try:
        requests.get(target, proxies={
            'http': proxy,
            'https': proxy
        }, timeout=5).raise_for_status()
    except:
        return PROXY_TEST_FAIL
    else:
        return PROXY_TEST_SUCCESS
