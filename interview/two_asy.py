import asyncio
import time

async def print_count(count):
    print(count)


async def print_thr_sec(count):
    await asyncio.sleep(3)
    print("%d seconds have passed" %(3*count))

async def main():
    count = 0
    while True:
        results = await asyncio.gather(
            print_count(count),
            print_thr_sec(count),
        )
        count += 1

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
