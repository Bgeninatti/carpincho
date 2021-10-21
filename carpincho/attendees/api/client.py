import requests


class EventolClient:

    _login_url = 'https://eventos.python.org.ar/admin/login/'

    def __init__(self, username, password):
        self._client = requests.session()
        self._login(username, password)

    def _login(self, username, password):
        self._client.get(self._login_url)
        csrftoken = self._client.cookies['csrftoken']
        login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken)
        self._client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        self._client.headers['Cookie'] = f"csrftoken={csrftoken}"
        self._client.post(self._login_url, data=login_data)

    def _set_headers(self):
        csrftoken = self._client.cookies['csrftoken']
        sessionid = self._client.cookies['sessionid']
        self._client.headers['Cookie'] = f"csrftoken={csrftoken}; sessionid={sessionid}"
        self._client.headers['Host'] = 'eventos.python.org.ar'
        self._client.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
        self._client.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self._client.headers['Accept-Language'] = 'es,en-US;q=0.7,en;q=0.3'
        self._client.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self._client.headers['Referer'] = 'https://eventos.python.org.ar/admin/'
        self._client.headers['Connection'] = 'keep-alive'
        self._client.headers['Upgrade-Insecure-Requests'] = '1'
        self._client.headers['Sec-Fetch-Dest'] = 'document'
        self._client.headers['Sec-Fetch-Mode'] = 'navigate'
        self._client.headers['Sec-Fetch-Site'] = 'same-origin'
        self._client.headers['Sec-Fetch-User'] = '?1'
        self._client.headers['Sec-GPC'] = '1'
        self._client.headers['Pragma'] = 'no-cache'
        self._client.headers['Cache-Control'] = 'no-cache'
        self._client.headers['TE'] = 'trailers'

    def get(self, url):
        self._set_headers()
        return self._client.get(url)
