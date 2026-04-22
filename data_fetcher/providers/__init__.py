"""
data_fetcher 数据源提供者

提供统一的数据获取接口，封装各数据源 API。
"""

from .tencent import fetch_tencent_quote, fetch_tencent_index
from .sina import fetch_sina_quote, fetch_sina_index
from .eastmoney import fetch_eastmoney_quote, fetch_eastmoney_financials

__all__ = [
    'fetch_tencent_quote',
    'fetch_tencent_index',
    'fetch_sina_quote',
    'fetch_sina_index',
    'fetch_eastmoney_quote',
    'fetch_eastmoney_financials',
]
