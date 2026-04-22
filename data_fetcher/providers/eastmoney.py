"""
东方财富数据源

免费、无需 API Key、支持实时行情和财务数据
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

from data_fetcher.exceptions import DataFetchError


def convert_to_eastmoney_secid(symbol: str) -> str:
    """
    转换股票代码为东方财富格式
    
    东方财富 secid 格式：
    - 上海：1.600519
    - 深圳：0.000001
    """
    symbol = symbol.upper()
    if symbol.endswith('.SH'):
        return f"1.{symbol.replace('.SH', '')}"
    elif symbol.endswith('.SZ'):
        return f"0.{symbol.replace('.SZ', '')}"
    else:
        return symbol


def fetch_eastmoney_quote(symbol: str, timeout: int = 10) -> Dict[str, Any]:
    """
    从东方财富获取个股行情
    
    Args:
        symbol: 股票代码（如：600519.SH）
        timeout: 超时时间（秒）
    
    Returns:
        行情数据字典
    
    Raises:
        DataFetchError: 获取失败时抛出
    """
    secid = convert_to_eastmoney_secid(symbol)
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    
    params = {
        'secid': secid,
        # 重要字段：f43=当前价, f44=涨跌额, f45=涨跌幅%,
        # f46=最高, f47=成交量, f48=成交额, f49=最低,
        # f50=开盘, f51=昨收, f52=总市值, f58=名称,
        # f116=总市值, f117=实时时间戳, f162=市净率
        'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fltt': '2',
        'invt': '2',
    }
    
    headers = {
        'Referer': 'https://www.eastmoney.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('data'):
            raise DataFetchError(f"东方财富未返回数据: {symbol}")
        
        d = data['data']
        
        # 东方财富的价格字段需要除以 100
        price = d.get('f43', 0)
        if price:
            price = price / 100.0
        
        high = d.get('f46', 0)
        if high:
            high = high / 100.0
        
        low = d.get('f49', 0)
        if low:
            low = low / 100.0
        
        open_price = d.get('f50', 0)
        if open_price:
            open_price = open_price / 100.0
        
        prev_close = d.get('f51', 0)
        if prev_close:
            prev_close = prev_close / 100.0
        
        change = d.get('f44', 0)
        if change:
            change = change / 100.0
        
        change_percent = d.get('f45', 0)
        if change_percent:
            change_percent = change_percent / 100.0
        
        return {
            'symbol': symbol,
            'name': d.get('f58', ''),
            'price': price,
            'change': change,
            'change_percent': round(change_percent, 2),
            'volume': d.get('f47', 0),
            'turnover': d.get('f48', 0.0),
            'high': high,
            'low': low,
            'open': open_price,
            'prev_close': prev_close,
            'market_cap': d.get('f116', 0.0),
            'pe': d.get('f164', 0.0),
            'pb': d.get('f165', 0.0),
            'source': 'eastmoney',
            'timestamp': datetime.now().isoformat(),
        }
        
    except requests.RequestException as e:
        raise DataFetchError(f"东方财富请求失败: {e}")
    except json.JSONDecodeError as e:
        raise DataFetchError(f"东方财富 JSON 解析失败: {e}")
    except Exception as e:
        raise DataFetchError(f"东方财富数据处理异常: {e}")


def fetch_eastmoney_financials(symbol: str, timeout: int = 10) -> Dict[str, Any]:
    """
    从东方财富获取财务数据（主要财务指标）
    
    Args:
        symbol: 股票代码（如：600519.SH）
        timeout: 超时时间（秒）
    
    Returns:
        财务数据字典
    """
    symbol_clean = symbol.upper().replace('.SH', '').replace('.SZ', '')
    
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        'type': 'RPT_F10_FINANCE_MAINFINADATA',
        'secucode': symbol,
        'code': symbol_clean,
        'p': '1',
        'ps': '1',
        'fields': 'REPORTDATE,TOTAL_OPERATE_INCOME,PARENT_NETPROFIT,ROE,DEBT_ASSET_RATIO',
    }
    
    headers = {
        'Referer': 'https://www.eastmoney.com/',
        'User-Agent': 'Mozilla/5.0',
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('result') or not data['result'].get('data'):
            raise DataFetchError(f"东方财富未返回财务数据: {symbol}")
        
        items = data['result']['data']
        if not items:
            raise DataFetchError(f"东方财富财务数据为空: {symbol}")
        
        latest = items[0]
        
        return {
            'symbol': symbol,
            'revenue': float(latest.get('TOTAL_OPERATE_INCOME', 0) or 0) / 100000000,  # 转为亿元
            'net_profit': float(latest.get('PARENT_NETPROFIT', 0) or 0) / 100000000,
            'roe': float(latest.get('ROE', 0) or 0),
            'debt_ratio': float(latest.get('DEBT_ASSET_RATIO', 0) or 0),
            'source': 'eastmoney',
            'timestamp': datetime.now().isoformat(),
        }
        
    except requests.RequestException as e:
        raise DataFetchError(f"东方财富财务请求失败: {e}")
    except json.JSONDecodeError as e:
        raise DataFetchError(f"东方财富财务 JSON 解析失败: {e}")
    except (KeyError, IndexError, TypeError) as e:
        raise DataFetchError(f"东方财富财务数据解析失败: {e}")
    except Exception as e:
        raise DataFetchError(f"东方财富财务处理异常: {e}")
