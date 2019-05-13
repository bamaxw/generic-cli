import asyncio
import logging
from pprint import pprint

from generic_cli import Client

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.WARNING)


async def main():
    async with Client('stag', service_name='skyscraper-api') as cli:
        print(await cli.get_host())
    try:
        async with Client('stag', service_name='not-exist') as cli:
            print(await cli.get_host())
    except Exception as ex:
        print(type(ex), ex)
    async with Client('stag', service_name='skyscraper-api', config=dict(retry_codes={404}, timeout=5)) as cli:
        async with cli.get('/scrape'
                           '/103942643058347905226786937033882997479'
                           '/284331308606900884490446715759372814970') as res:
            print(res)
            pprint(await res.text())

    async with Client(host='http://localhost:81', config=dict(on_connerr=True)) as cli:
        async with cli.get('/healthcheck') as res:
            print(res)
            pprint(await res.text())


if __name__ == '__main__':
    asyncio.run(main())
