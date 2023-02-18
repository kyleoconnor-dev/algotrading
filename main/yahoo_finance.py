import datetime
from typing import Union

import aiohttp


class HTTPResponseError(Exception):
    def __init__(self, status):
        self.message = f'HTTPError: {status}'
        super().__init__(self.message)


class YahooFinance:
    QUERY_CHART_URL = "https://query1.finance.yahoo.com/v7/finance/chart/"
    START_SECONDS = 7223400
    DAILY_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }
    INTERVALS = ("1d", "1wk", "1mo", "1m")

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    def _build_chart_url(
            self, ticker: str, start_date: Union[str, None] = None,
            end_date: Union[str, None] = None, interval: str = '1d'
    ):
        if end_date is None:
            end_seconds = int(datetime.datetime.now().timestamp())

        else:
            end_dt = datetime.datetime.strptime(
                end_date, '%Y-%m-%d %H:%M:%S'
            ).timestamp()
            end_seconds = int(end_dt)

        if start_date is None:
            start_seconds = self.START_SECONDS
        else:
            start_dt = datetime.datetime.strptime(
                start_date, '%Y-%m-%d %H:%M:%S'
            ).timestamp()
            start_seconds = int(start_dt)

        site = f'{self.QUERY_CHART_URL}{ticker}'
        params = {
            'period1': start_seconds,
            'period2': end_seconds,
            'interval': interval.lower(),
            'events': 'div,splits'
        }

        return site, params

    async def get_daily_data(
            self, ticker: str, start_date: Union[str, None] = None,
            end_date: Union[str, None] = None, interval: str = '1d'
    ):

        if interval not in self.INTERVALS:
            raise AssertionError(f'interval must be one of {self.INTERVALS}')

        site, params = self._build_chart_url(ticker, start_date, end_date, interval)

        async with self._session.get(site, params=params) as response:
            if not response.ok:
                status = response.status
                raise HTTPResponseError(status)
            raw_data = await response.json()
            return raw_data
