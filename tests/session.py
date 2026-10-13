"""Exercise the example telnet UI inside the running Docker image."""
import asyncio
import os
from pathlib import Path

import telnetlib3


async def read_until(reader, expected):
    received = ""
    while expected not in received.replace("\r", ""):
        chunk = await asyncio.wait_for(reader.read(4096), timeout=15)
        if not chunk:
            raise AssertionError("Connection closed before expected content: " + expected[:50])
        received += chunk
    return received


async def main():
    port = int(os.environ.get("PORT", "8023"))
    issue = Path("/app") / os.environ.get("CONTENT_FOLDER", "issue")
    reader, writer = await telnetlib3.open_connection("127.0.0.1", port)
    try:
        await read_until(reader, "This is the introduction to the zine")
        print("PASS: welcome text received")
        writer.write("\n")
        await writer.drain()
        menu = await read_until(reader, "(or X to quit!)")
        assert "blah" in menu and "another one" in menu
        print("PASS: both story titles appear in the index")
        writer.write("1")
        await writer.drain()
        await read_until(reader, "...press RETURN")
        writer.write("\n")
        await writer.drain()
        for page in (1, 2):
            expected = (issue / "testtest" / f"{page}.txt").read_text().strip()
            await read_until(reader, expected)
            print(f"PASS: full story page {page} received")
            writer.write("\n")
            await writer.drain()
        await read_until(reader, "(or X to quit!)")
        print("PASS: returned to index after final page")
        writer.write("X")
        await writer.drain()
        assert await asyncio.wait_for(reader.read(1), timeout=5) == ""
        print("PASS: X closes the session")
    finally:
        writer.close()


asyncio.run(main())
