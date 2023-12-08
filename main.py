#!/bin/python3
import clip
import asyncio
import sys


def get_usage() -> str:
    return "Usage: main.py <song>"


async def main():
    if len(sys.argv) != 2:
        print(get_usage())
        exit(1)

    song = sys.argv[1]
    await clip.download_clip(song)


if __name__ == "__main__":
    asyncio.run(main())
