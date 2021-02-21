import asyncio, telnetlib3
import os
import pathlib
from lib.zine_functions import ZineFunctions

async def shell(reader, writer):
    root_dir_path = pathlib.Path(__file__).parent.parent.absolute()

    zine = ZineFunctions(reader, writer, "%s/%s" % (root_dir_path.as_posix(), "issue1/index.json"))
    await zine.run_index()

loop = asyncio.get_event_loop()
srv = telnetlib3.create_server(port=23, shell=shell)
server = loop.run_until_complete(srv)
loop.run_until_complete(server.wait_closed())
