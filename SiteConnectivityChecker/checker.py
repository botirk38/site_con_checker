from http.client import HTTPConnection
from urllib.parse import urlparse 
import asyncio
import aiohttp
import time

def site_is_online(url, timeout=5):
    error = Exception('Site is offline')
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for port in (80,443):
        connection = HTTPConnection(host=host, port=port,timeout=timeout)
        try:
            connection.request('HEAD', url)
            response = connection.getresponse()
            if response.status in (200, 301, 302):
                return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error

async def site_is_online_async(url, timeout=5):
    error = Exception("Unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for scheme in ('http', 'https'):
        try:
            target_url =f"{scheme}://{host}"
            async with aiohttp.ClientSession() as session:
                try:
                    await session.head(target_url,timeout=timeout)
                    return True
                except asyncio.exceptions.TimeoutError:
                    error = Exception("Timeout")
                except Exception as e:
                    error = e
        except Exception as e:
            error = e
    raise error

def get_response_time(url, timeout=5):
    start_time = time.time()
    site_is_online(url, timeout)
    return time.time() - start_time

async def get_response_time_async(url, timeout=5):
    start_time = time.time()
    await site_is_online_async(url, timeout)
    return time.time() - start_time
