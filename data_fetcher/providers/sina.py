"""
新浪财经数据源

免费、无需 API Key、实时数据
"""

import requests
import re
from datetime import datetime
from typing import Dict, Any, Optional

from data_fetcher.exceptions import DataFetchError


def convert_to_sina_code(symbol: str) -> str:
    """
    转换股票代码为新浪格式
    """
    symbol = symbol.upper()
    if symbol.endswith('.SH'):
        return 'sh' + symbol.replace('.SH', '')
    elif symbol.endswith('.SZ'):
        return 'sz' + symbol.replace('.SZ', '')
    else:
        return symbol.lower()


def fetch_sina_quote(symbol: str, timeout: int = 5) -> Dict[str, Any]:
    """
    从新浪财经获取个股行情
    
    Args:
        symbol: 股票代码（如：600519.SH）
        timeout: 超时时间（秒）
    
    Returns:
        行情数据字典
    
    Raises:
        DataFetchError: 获取失败时抛出
    """
    code = convert_to_sina_code(symbol)
    url = f"http://hq.sinajs.cn/list={code}"
    
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        text = response.content.decode('gbk')
        
        # 解析：var hq_str_sh600519="贵州茅台,1780.00,1785.00,1775.00,...
        pattern = r'hq_str_(\w+)="(.*?)"'
        match = re.search(pattern, text)
        
        if not match:
            raise DataFetchError(f"新浪未返回数据: {symbol}")
        
        data_str = match.group(2)
        fields = data_str.split(',')
        
        if len(fields) < 10:
            raise DataFetchError(f"新浪数据字段不足: {symbol}")
        
        name = fields[0]
        open_price = float(fields[1]) if fields[1] else 0.0
        prev_close = float(fields[2]) if fields[2] else 0.0
        price = float(fields[3]) if fields[3] else 0.0
        high = float(fields[4]) if fields[4] else 0.0
        low = float(fields[5]) if fields[5] else 0.0
        
        # 成交量（股）
        volume = int(float(fields[8])) if fields[8] else 0
        
        # 成交额（元）
        turnover = float(fields[9]) if fields[9] else 0.0
        
        # 涨跌额和涨跌幅
        change = price - prev_close
        change_percent = (change / prev_close * 100) if prev_close else 0.0
        
        return {
            'symbol': symbol,
            'name': name,
            'price': price,
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': volume,
            'turnover': turnover,
            'high': high,
            'low': low,
            'open': open_price,
            'prev_close': prev_close,
            'source': 'sina',
            'timestamp': datetime.now().isoformat(),
        }
        
    except requests.RequestException as e:
        raise DataFetchError(f"新浪请求失败: {e}")
    except Exception as e:
        raise DataFetchError(f"新浪数据处理异常: {e}")


def fetch_sina_index(symbol: str, timeout: int = 5) -> Dict[str, Any]:
    """
    从新浪财经获取大盘指数
    
    Args:
        symbol: 指数代码（标准格式，如：sh000001）
        timeout: 超时时间（秒）
    
    Returns:
        指数数据字典
    """
    # 新浪需要 sh 前缀
    symbol = symbol.lower()
    if not symbol.startswith('sh') and not symbol.startswith('sz'):
        symbol = 'sh' + symbol
    
    url = f"http://hq.sinajs.cn/list={symbol}"
    
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0',
    }
    
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        text = response.content.decode('gbk')
        
        pattern = r'hq_str_(\w+)="(.*?)"'
        match = re.search(pattern, text)
        
        if not match:
            raise DataFetchError(f"新浪未返回指数数据: {symbol}")
        
        data_str = match.group(2)
        fields = data_str.split(',')
        
        if len(fields) < 5:
            raise DataFetchError(f"新浪指数数据字段不足: {symbol}")
        
        name = fields[0]
        price = float(fields[1]) if fields[1] else 0.0
        prev_close = float(fields[2]) if fields[2] else 0.0
        
        change = price - prev_close
        change_percent = (change / prev_close * 100) if prev_close else 0.0
        
        return {
            'symbol': symbol,
            'name': name,
            'price': price,
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': int(float(fields[8])) if len(fields) > 8 and fields[8] else 0,
            'turnover': float(fields[9]) / 100000000 if len(fields) > 9 and fields[9] else 0.0,
            'source': 'sina',
            'timestamp': datetime.now().isoformat(),
        }
        
    except requests.RequestException as e:
        raise DataFetchError(f"新浪指数请求失败: {e}")
    except Exception as e:
        raise DataFetchError(f"新浪指数处理异常: {e}")
