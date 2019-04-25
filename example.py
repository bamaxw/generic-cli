import asyncio

from generic_cli import AutoResolveClient


async def main():
    cli = await AutoResolveClient.resolve('skyscraper-api', 'stag')
    print(cli, cli.__dict__, await cli.get_host())
    await cli.close()


if __name__ == '__main__':
    asyncio.run(main())
