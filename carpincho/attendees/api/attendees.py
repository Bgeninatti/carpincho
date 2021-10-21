from bs4 import BeautifulSoup

from carpincho.db.models import Attendee


class AttendeeProvider:

    _url = 'https://eventos.python.org.ar/admin/manager/attendee/{attendee_id}/change/'

    def __init__(self, client):
        self._client = client

    def fetch_since(self, attendee_id: int, limit: int = 10):
        for i in range(limit):
            try:
                yield self.fetch_one(attendee_id + i)
            except ValueError:
                continue

    def fetch_one(self, attendee_id):
        print(f"Fetching attendee: attendee_id={attendee_id}")
        url = self._url.format(attendee_id=attendee_id)
        response = self._client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if not self.is_pyconar_2021(soup):
            return
        return Attendee.from_html(soup, attendee_id=attendee_id)

    @staticmethod
    def is_pyconar_2021(soup):
        event_select = soup.find('select', id='id_event')
        if event_select is None:
            raise ValueError("Attendee not found")
        return event_select.find('option', selected=True).text == 'PyConAr 2021'
