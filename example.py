import asyncio
import logging

from generic_cli import Client

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.WARNING)


async def main():
    async with Client('stag', service_name='skyscraper-api') as cli:
        print(await cli.get_host())
    async with Client('stag', service_name='not-exist') as cli:
        print(await cli.get_host())


if __name__ == '__main__':
    asyncio.run(main())
