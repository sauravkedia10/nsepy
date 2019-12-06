from .history import get_history, get_index_pe_history, get_rbi_ref_history
from .live import get_quote
from .derivatives import get_expiry_date

__VERSION__ = 0.7


"""
Changes:
    
    
Date: 2019-12-06: timeout in case response not comimg.
--------------------------------------------------------
there was a problem in few calls, especially to fetch FO bhavcopy and the
request to fetch it was indefinitely waiting.

So, we decided to wait for the responde till a certain timeout period
(timeout period can be provided in function calls, default is 30 secs) using 
timeout feature of requests library which powers this library under the hood. 
Further, it makes three retries before raising an error. Once three retries are
exceeded, it will raise Timeout error which can be caught by other packages using
this package.
     
At core is the URLFetch object in commons.py which does the ultimate call to
nse. Its __call__ method is executed to scpare NSE. I have added a timeout
as well as max retries feature there. The timeout is set at 20 secs by default. 
If any downstream code sends timeout param in the __call__ method, then timeout
will be implemented, else timeout will be 30 sec. Please, note the timeout param
is to be provided in the __call__ method and not to the URLFetch object directly.
Max retries is hardcoded at 3.

If the response takes more than timeout param and max retries exceed it will raise
an Timeout error which can be caught by downstream code. nsepy will raise it and
the downstream applications will catch it.

    ConnectionError: HTTPSConnectionPool(host='www.nseindia.com', port=443): Max retries exceeded with url: /live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=ACC&series=EQ&timeout=0.01 (Caused by ReadTimeoutError("HTTPSConnectionPool(host='www.nseindia.com', port=443): Read timed out. (read timeout=0.01)",))
catch using 

    from requests.exceptions import Timeout
    try:
        derivative_price_list_url(2019, 'DEC', '05DEC2019', timeout=(0.01,0.01))
    except Timeout:
        print ('Failed!')

"""


    