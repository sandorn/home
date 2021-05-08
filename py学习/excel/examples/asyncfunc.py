"""
PyXLL Examples: Async function

Starting with Excel 2010 worksheet functions can
be registered as asynchronous.

This can be used for querying results from a server
asynchronously to improve the worksheet calculation
performance.
"""

from pyxll import xl_func, xl_version
import logging

_log = logging.getLogger(__name__)

try:
    import json
except ImportError:
    _log.warning("json could not be imported. Async example will not work", exc_info=True)
    json = None

try:
    import aiohttp
except ImportError:
    _log.warning("aiohttp could not be imported. Async example will not work", exc_info=True)
    aiohttp = None

try:
    import asyncio
except ImportError:
    _log.warning("asyncio could not be imported. Async example will not work", exc_info=True)
    asyncio = None

#
# Async functions are only supported from Excel 2010
#
if xl_version() >= 14 and json is not None and aiohttp is not None and asyncio is not None:

    @xl_func
    async def pyxll_stock_price(endpoint, api_token, symbol):
        """Return the latest price for a symbol from alphavantage.co"""
        url = "{endpoint}/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_token}".format(
            endpoint=endpoint,
            symbol=symbol,
            api_token=api_token)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # If we got a 429 error wait a second and try again
                if response.status == 429:
                    delay = int(response.headers.get("Retry-After", "1"))
                    await asyncio.sleep(delay)
                    return await pyxll_stock_price(endpoint, api_token, symbol)

                # Otherwise check the status and read the response
                assert response.status == 200, f"Request failed: {response.status}"
                data = await response.read()

        data = json.loads(data.decode("utf-8"))
        quote = data.get("Global Quote", {}).get("05. price")
        if quote is None:
            return data.get("Information", "#DataNotAvailable")

        return quote

else:

    @xl_func
    def pyxll_stock_price(endpoint, api_token, symbol):
        """not supported in this version of Excel"""
        if xl_version() < 14:
            return "async functions are not supported in Excel %s" % xl_version()
        if aiohttp is None:
            return "aiohttp module could not be imported"
        if asyncio is None:
            return "asyncio module could not be imported"
        if json is None:
            return "json module could not be imported"