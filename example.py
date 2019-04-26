import asyncio

from aiohttp import ClientSession as Session

from generic_cli import AutoResolveClient


async def main():
    async with AutoResolveClient.resolve('skyscraper-api', 'stag') as cli:
        print(cli, cli.__dict__, await cli.get_host())
    async with Session() as sess:
        async with sess.request('GET', 'https://inyourarea.co.uk') as res:
            print(await res.text())


if __name__ == '__main__':
    asyncio.run(main())
