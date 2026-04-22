"""
投资框架数据获取模块

统一接口获取股价、指数、财务数据，支持多数据源自动降级。
"""

from .core import DataFetcher, DataFetchError, Quote, IndexData, Financials
from .config import load_config, save_config, get_config_path

__all__ = [
    'DataFetcher',
    'DataFetchError', 
    'Quote',
    'IndexData',
    'Financials',
    'load_config',
    'save_config',
    'get_config_path',
]

__version__ = '1.0.0'
