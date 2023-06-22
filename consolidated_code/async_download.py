#######################################################################################################################

# Following code is to download all the literature pdf from the links in CSV.
# It is downloading in asynch manner and making a log with status and timestamp.

import asyncio
import aiohttp
import pandas as pd
import time
from globalFunction import *



async def download_file(session, url,log_filename):
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            filename = url.rsplit('/',1)[1]
            download_path = f'../data/final/assets/{filename}'
            with open(download_path, "wb") as file:
                file.write(content)
        else:
            print(f"Error downloading {url}: {response.status}")
        
        filename = url.rsplit('/',1)[1]
        fileDownload_log(response.status,url,filename,log_filename)

async def main():
    df = pd.read_csv('literature_details.csv')
    urls = df['url']
    log_filename = 'allied_fileDownload_log.csv'
    
    async with aiohttp.ClientSession() as session:
        
        tasks = [download_file(session, url,log_filename) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())
    print(f'Total time = {time.time()-t1}')