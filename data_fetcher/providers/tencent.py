"""
腾讯财经数据源

免费、无需 API Key、实时数据
"""

import requests
import re
from datetime import datetime
from typing import Dict, Any, Optional

from data_fetcher.exceptions import DataFetchError


# 指数代码映射（腾讯返回的 code -> 名称）
INDEX_NAME_MAP = {
    'sh000001': '上证指数',
    'sz399001': '深证成指',
    'sz399006': '创业板指',
    'sh000300': '沪深300',
    'sh000016': '上证50',
    'sh000688': '科创50',
    'sz399005': '中小板指',
    'sh000905': '中证500',
}


def convert_to_tencent_code(symbol: str) -> str:
    """
    转换股票代码为腾讯格式
    
    Args:
        symbol: 标准代码（如：600519.SH）
    
    Returns:
        腾讯格式代码（如：sh600519）
    """
    symbol = symbol.upper()
    if symbol.endswith('.SH'):
        return 'sh' + symbol.replace('.SH', '')
    elif symbol.endswith('.SZ'):
        return 'sz' + symbol.replace('.SZ', '')
    elif symbol.startswith('s_'):
        return symbol  # 已经是腾讯格式
    else:
        # 假设沪市
        return 'sh' + symbol


def fetch_tencent_quote(symbol: str, timeout: int = 5) -> Dict[str, Any]:
    """
    从腾讯财经获取个股行情
    
    Args:
        symbol: 股票代码（如：600519.SH）
        timeout: 超时时间（秒）
    
    Returns:
        行情数据字典
    
    Raises:
        DataFetchError: 获取失败时抛出
    """
    code = convert_to_tencent_code(symbol)
    url = f"http://qt.gtimg.cn/q={code}"
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # 腾讯返回 GBK 编码
        text = response.content.decode('gbk')
        
        # 解析：v_sh600519="23~贵州茅台~600519~1780.00~1785.00~1775.00~...~..."
        pattern = r'v_(.*?)=\"(.*?)\"'
        matches = re.findall(pattern, text)
        
        if not matches:
            raise DataFetchError(f"腾讯未返回数据: {symbol}")
        
        for _, data in matches:
            fields = data.split('~')
            
            if len(fields) < 40:
                continue
            
            price_str = fields[3]
            prev_close_str = fields[11]
            
            price = float(fields[3]) if fields[3] else 0.0
            prev_close = float(fields[11]) if fields[11] else 0.0
            
            # 涨跌额：字段31，涨跌幅：字段32（已经是%格式）
            change = float(fields[31]) if fields[31] else 0.0
            change_percent = float(fields[32]) if fields[32] else 0.0
            
            # 市盈率：字段39，市净率：字段46
            pe = float(fields[39]) if fields[39] else 0.0
            pb = float(fields[46]) if fields[46] else 0.0
            
            # 市值（单位：亿元）
            market_cap_str = fields[45] if len(fields) > 45 else '0'
            market_cap = float(market_cap_str) if market_cap_str else 0.0
            
            return {
                'symbol': symbol,
                'name': fields[1],
                'price': price,
                'change': change,
                'change_percent': round(change_percent, 2),
                'volume': int(float(fields[6])) if fields[6] else 0,
                'turnover': float(fields[7]) if fields[7] else 0.0,
                'high': float(fields[8]) if fields[8] else 0.0,
                'low': fields[9],
                'open': float(fields[10]) if fields[10] else 0.0,
                'prev_close': prev_close,
                'market_cap': market_cap,
                'pe': pe,
                'pb': pb,
                'source': 'tencent',
                'timestamp': datetime.now().isoformat(),
            }
        
        raise DataFetchError(f"腾讯解析失败: {symbol}")
        
    except requests.RequestException as e:
        raise DataFetchError(f"腾讯请求失败: {e}")
    except Exception as e:
        raise DataFetchError(f"腾讯数据处理异常: {e}")


def fetch_tencent_index(symbol: str, timeout: int = 5) -> Dict[str, Any]:
    """
    从腾讯财经获取大盘指数
    
    Args:
        symbol: 指数代码（腾讯格式，如：s_sh000001）
        timeout: 超时时间（秒）
    
    Returns:
        指数数据字典
    
    Raises:
        DataFetchError: 获取失败时抛出
    """
    # 确保是腾讯格式
    if not symbol.startswith('s_'):
        # 转换标准格式为腾讯格式
        s = symbol.upper()
        if '.SH' in s:
            symbol = 's_sh' + s.replace('.SH', '')
        elif '.SZ' in s:
            symbol = 's_sz' + s.replace('.SZ', '')
        else:
            # 假设沪市
            symbol = 's_sh' + s
    
    url = f"http://qt.gtimg.cn/q={symbol}"
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        text = response.content.decode('gbk')
        
        pattern = r'v_(.*?)=\"(.*?)\"'
        matches = re.findall(pattern, text)
        
        if not matches:
            raise DataFetchError(f"腾讯未返回指数数据: {symbol}")
        
        for code, data in matches:
            fields = data.split('~')
            
            if len(fields) < 10:
                continue
            
            # code 格式如 sh000001（无 s_ 前缀），直接查映射表
            name = INDEX_NAME_MAP.get(code, fields[1] if len(fields) > 1 else code)
            
            price = float(fields[3]) if fields[3] else 0.0
            prev_close = float(fields[11]) if fields[11] else 0.0
            change = float(fields[4]) if fields[4] else 0.0
            
            if prev_close > 0 and price > 0:
                change_percent = (change / prev_close) * 100
            else:
                change_percent = float(fields[5]) if len(fields) > 5 and fields[5] else 0.0
            
            # 成交额单位是元，转换为亿元
            turnover = float(fields[7]) / 100000000 if fields[7] else 0.0
            
            return {
                'symbol': symbol,
                'name': name,
                'price': price,
                'change': change,
                'change_percent': round(change_percent, 2),
                'volume': int(float(fields[6])) if fields[6] else 0,
                'turnover': round(turnover, 2),
                'source': 'tencent',
                'timestamp': datetime.now().isoformat(),
            }
        
        raise DataFetchError(f"腾讯指数解析失败: {symbol}")
        
    except requests.RequestException as e:
        raise DataFetchError(f"腾讯指数请求失败: {e}")
    except Exception as e:
        raise DataFetchError(f"腾讯指数处理异常: {e}")
