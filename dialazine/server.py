#!/usr/bin/env python3
import asyncio
import os
import pathlib

import telnetlib3

from lib.zine_functions import ZineFunctions

LOCALHOST_PORT = int(os.environ.get("PORT", "8023"))
CONTENT_FOLDER = os.environ.get("CONTENT_FOLDER", "example_issue")

async def shell(reader, writer):
    root_dir_path = pathlib.Path(__file__).resolve().parent.parent

    zine = ZineFunctions(reader, writer, str(root_dir_path / CONTENT_FOLDER / "index.json"))
    try:
        await zine.run_index()
    finally:
        writer.close()


async def main():
    server = await telnetlib3.create_server(
        host="0.0.0.0", port=LOCALHOST_PORT, shell=shell, timeout=3600
    )
    print(f"dial-a-zine listening on port {LOCALHOST_PORT}", flush=True)
    try:
        await server.wait_closed()
    finally:
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
