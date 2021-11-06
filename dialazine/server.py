import asyncio, telnetlib3
import os
import pathlib
from lib.zine_functions import ZineFunctions

LOCALHOST_PORT = 23
CONTENT_FOLDER = "issue1"

async def shell(reader, writer):
    root_dir_path = pathlib.Path(__file__).parent.parent.absolute()

    zine = ZineFunctions(reader, writer, "%s/%s" % (root_dir_path.as_posix(), f"{CONTENT_FOLDER}/index.json"))
    await zine.run_index()

loop = asyncio.get_event_loop()
srv = telnetlib3.create_server(port=LOCALHOST_PORT, shell=shell, timeout=3600)
server = loop.run_until_complete(srv)
loop.run_until_complete(server.wait_closed())
