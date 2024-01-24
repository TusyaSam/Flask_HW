import sys
import time
import requests
import multiprocessing
import concurrent.futures
import asyncio
import aiohttp


urls = [
    'https://ru.freepik.com/popular-photos',
    'https://ru.freepik.com/free-photo/peaceful-cute-horses-in-the-nature_17342857.htm',
    'https:/https://ru.freepik.com/free-photo/front-view-woman-with-flowers-outdoors_34002136.htm'
]


def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                if chunk:
                    file.write(chunk)
        return f'Downloaded {filename}'
    else:
        return f'Failed to download {url}'


def download_images_multiprocessing(urls):
    start_time = time.time()
    num_processes = multiprocessing.cpu_count()
    results = []
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(download_image, urls)
    end_time = time.time()
    total_time = end_time - start_time
    return results, total_time


def download_images_multithreading(urls):
    start_time = time.time()
    num_threads = multiprocessing.cpu_count() * 2
    results = []
    with concurrent.futures.ThreadPoolExecutor(num_threads) as executor:
        results = list(executor.map(download_image, urls))
    end_time = time.time()
    total_time = end_time - start_time
    return results, total_time


async def download_image_async(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            filename = url.split('/')[-1]
            with open(filename, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
            return f'Downloaded {filename}'
        else:
            return f'Failed to download {url}'


async def download_images_async(urls):
    results = []
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(download_image_async(url, session))
        results = await asyncio.gather(*tasks)
    end_time = time.time()
    total_time = end_time - start_time
    return results, total_time


if __name__ == "__main__":
    urls = sys.argv[1:]
    if len(urls) == 0:
        print("Please provide a list of URLs")
        sys.exit(1)

    print("Downloading images using multiprocessing...")
    multiprocessing_results, multiprocessing_time = download_images_multiprocessing(urls)
    for result in multiprocessing_results:
        print(result)
    print(f"Total time using multiprocessing: {multiprocessing_time} seconds")

    print("\nDownloading images using multithreading...")
    multithreading_results, multithreading_time = download_images_multithreading(urls)
    for result in multithreading_results:
        print(result)
    print(f"Total time using multithreading: {multithreading_time} seconds")

    print("\nDownloading images using asyncio...")
    loop = asyncio.get_event_loop()
    asyncio_results, asyncio_time = loop.run_until_complete(download_images_async(urls))
    for result in asyncio_results:
        print(result)
    print(f"Total time using asyncio: {asyncio_time} seconds")