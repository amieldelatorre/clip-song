#!/bin/python3
import clip
import asyncio


song = "<example_song>"


async def main():
    await clip.download_clip(song)


if __name__ == "__main__":
    asyncio.run(main())
