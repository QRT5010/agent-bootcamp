import httpx
import time

URLS = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 6)]

def fetch_one(url):
    resp = httpx.get(url)
    return resp.json()["title"][:20]

def run_sync():
    start = time.time()
    for url in URLS:
        title = fetch_one(url)
        print(f"  拿到: {title}")
    print(f"【同步】总耗时: {time.time() - start:.2f} 秒")

run_sync()

import asyncio

async def fetch_one_async(client, url):
    resp = await client.get(url)
    return resp.json()["title"][:20]

async def run_async():
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_one_async(client, url) for url in URLS]
        titles = await asyncio.gather(*tasks)
    for title in titles:
        print(f"  拿到: {title}")
    print(f"【异步】总耗时: {time.time() - start:.2f} 秒")

asyncio.run(run_async())
