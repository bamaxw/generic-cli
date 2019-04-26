import asyncio

from generic_cli import AutoResolveClient


async def main():
    async with AutoResolveClient('skyscraper-api', 'stag') as cli:
        print(cli, cli.__dict__, await cli.get_host())
    async with AutoResolveClient('nonexistant', 'stag') as cli:
        print(cli, cli.__dict__, await cli.get_host())


if __name__ == '__main__':
    asyncio.run(main())
