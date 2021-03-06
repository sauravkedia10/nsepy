# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 21:51:41 2015

@author: SW274998
"""
from .commons import *
import ast
import json
from .liveurls import quote_eq_url, quote_derivative_url, option_chain_url
import urllib.parse

eq_quote_referer = "https://archives.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}&illiquid=0&smeFlag=0&itpFlag=0"
derivative_quote_referer = "https://archives.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying={}&instrument={}&expiry={}&type={}&strike={}"
option_chain_referer = "https://archives.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-9999&symbol=NIFTY&symbol=BANKNIFTY&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17"

def get_quote(symbol, series='EQ', instrument=None, expiry=None, option_type=None, strike=None):
    """
    1. Underlying security (stock symbol or index name)
    2. instrument (FUTSTK, OPTSTK, FUTIDX, OPTIDX)
    3. expiry (ddMMMyyyy)
    4. type (CE/PE for options, - for futures
    5. strike (strike price upto two decimal places
    """
    symbol1 = urllib.parse.quote_plus(symbol)
    if instrument:
        expiry_str = "%02d%s%d"%(expiry.day, months[expiry.month][0:3].upper(), expiry.year)
        quote_derivative_url.session.headers.update({'Referer': eq_quote_referer.format(symbol)})
        strike_str = "{:.2f}".format(strike) if strike else "" 
        res = quote_derivative_url(symbol1, instrument, expiry_str, option_type, strike_str, timeout=10)
    else:
        quote_eq_url.session.headers.update({'Referer': eq_quote_referer.format(symbol)})
        res = quote_eq_url(symbol1, series, timeout=10)

    d =  json.loads(res.text)['data'][0]
    res = {}
    for k in d.keys():
        v = d[k]
        try:
            v_ = None
            if v.find('.') > 0:
                v_ = float(v.strip().replace(',', ''))
            else:
                v_ = int(v.strip().replace(',', ''))
        except:
            v_ = v
        res[k] = v_
    return res

def get_option_chain(symbol, instrument="OPTSTK", expiry=None):
    
    """This method is incomplete"""
    symbol1 = urllib.parse.quote_plus(symbol)
    if expiry:
        expiry_str = "%02d%s%d"%(expiry.day, months[expiry.month][0:3].upper(), expiry.year)
    else:
        expiry_str = "-"
    option_chain_url.session.headers.update({'Referer': option_chain_referer})
    r = option_chain_url(symbol1, instrument, expiry_str, timeout=10)
    # r needs to be decoded.
    return r

