from requests import Session, RequestException


class TimeOutSession(Session):

    def __init__(self, timeout):
        self.timeout = timeout

        super(TimeOutSession, self).__init__()

    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', self.timeout)

        return super(TimeOutSession, self).request(*args, **kwargs)

    def json(self, method, url, **kwargs):
        try:
            response = self.request(method, url, **kwargs)
        except RequestException as error:
            return None, error

        if response.status_code == 204:
            return True, None

        elif response.ok:
            return True, response.json()

        return False, response
