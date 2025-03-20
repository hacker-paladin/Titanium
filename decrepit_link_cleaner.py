import aiohttp
import asyncio

RAWLIST_FILE = "RAWLIST.txt"
CLEANEDLIST_FILE = "CLEANEDLIST.txt"
CONCURRENT_REQUESTS = 100  # Adjust based on system performance

async def check_url(session, url):
    """Check if a URL is valid (returns a successful HTTP status)."""
    try:
        async with session.get(url, timeout=5) as response:
            if response.status < 400:  # Successful responses (2xx and 3xx)
                return url
    except:
        pass
    return None

async def process_urls():
    """Read RAWLIST, check URLs concurrently, and write valid ones to CLEANEDLIST."""
    with open(RAWLIST_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]  # Remove empty lines

    connector = aiohttp.TCPConnector(limit_per_host=CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    valid_urls = [url for url in results if url]

    with open(CLEANEDLIST_FILE, "w") as f:
        f.write("\n".join(valid_urls))

    print(f"Completed! {len(valid_urls)} valid URLs saved to {CLEANEDLIST_FILE}")

if __name__ == "__main__":
    asyncio.run(process_urls())