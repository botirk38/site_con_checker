import sys
import pathlib
import asyncio


from SiteConnectivityChecker.checker import site_is_online,site_is_online_async,get_response_time, get_response_time_async
from SiteConnectivityChecker.cli import read_user_cli_args,display_result

def main():

    args = read_user_cli_args()
    print(args)
    urls = _get_websites_urls(args)
    if not urls:
        print("Error: No URLs to check",file=sys.stderr)
        sys.exit(1)
    if args.asynchronous:
        asyncio.run(_asynchronously_check_websites(urls))
        for url in urls:
            print(f"The response time for {url} was: {get_response_time(url)}")
        
    else:
        _syncrhonously_check_websites(urls)
        print(f"The response time for {url} was: {get_response_time(url)}")
    
        



def _get_websites_urls(user_args):
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)
    return urls

def _read_urls_from_file(input_file):
    filePath = pathlib.Path(input_file)
    if filePath.is_file():
        with filePath.open() as urls_file:
            urls = [url.strip() for url in urls_file]
        if urls:
            return urls
        print("Error: File is empty",file=sys.stderr)
    else:
        print("Error: File not found",file=sys.stderr)
        return None
async def _asynchronously_check_websites(urls):
    async def _check(url):
        error =""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_result(result, url,error)
    await asyncio.gather(*[_check(url) for url in urls])

def _syncrhonously_check_websites(urls):
    for url in urls:
        error =""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_result(result,url,error)
if __name__ == "__main__":
    main()
    

