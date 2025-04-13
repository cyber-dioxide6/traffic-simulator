import asyncio
import aiohttp
import random
from faker import Faker

fake = Faker()

# Generate unique headers
def generate_headers():
    return {
        'User-Agent': fake.user_agent(),
        'X-Forwarded-For': fake.ipv4(),
        'Referer': fake.url(),
    }

# Send a single request
async def send_visit(session, url, index):
    headers = generate_headers()
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            print(f"[{index}] Status: {response.status} | IP: {headers['X-Forwarded-For']}")
    except Exception as e:
        print(f"[{index}] Request failed: {e}")

# Main function
async def main():
    url = input("Enter website URL (with https://): ").strip()
    try:
        total_requests = int(input("Total number of visits: "))
    except ValueError:
        print("Invalid number entered.")
        return

    connector = aiohttp.TCPConnector(limit=1000)  # Increase for higher concurrency
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_visit(session, url, i+1) for i in range(total_requests)]
        await asyncio.gather(*tasks)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
