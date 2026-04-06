"""
东方财富基金 API（天天基金）

无需 API Key，支持基金净值、基本信息、业绩、持仓等
接口：
- 估值: http://fundgz.1234567.com.cn/
- 详情: https://fundmobapi.eastmoney.com/
- 净值: https://api.fund.eastmoney.com/
"""

import re
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
from ..exceptions import ProviderError


# ============================================================
# 基金估值（盘中实时）
# ============================================================

def fetch_fund_estimated_nav(fund_code: str, timeout: int = 5) -> Dict:
    """
    获取基金实时估值（盘中）
    
    来源：天天基金估值接口
    
    Args:
        fund_code: 6位基金代码
        timeout: 超时秒数
    
    Returns:
        dict: {
            fund_code, fund_name, nav_date, nav, 
            estimated_nav, estimated_return, estimate_time
        }
    """
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    
    try:
        resp = requests.get(url, timeout=timeout, headers={
            'Referer': 'http://fund.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        
        text = resp.text.strip()
        if not text:
            raise ProviderError('fund_eastmoney', f'基金{fund_code}估值接口返回空')
        
        # 解析 JSONP: jsonpgz({...});
        match = re.search(r'jsonpgz\((.*?)\)', text)
        if not match:
            raise ProviderError('fund_eastmoney', f'基金{fund_code}估值数据格式异常')
        
        data = json.loads(match.group(1))
        
        return {
            'fund_code': data.get('fundcode', fund_code),
            'fund_name': data.get('name', ''),
            'nav_date': data.get('jzrq', ''),
            'nav': _safe_float(data.get('dwjz')),
            'estimated_nav': _safe_float(data.get('gsz')),
            'estimated_return': _safe_float(data.get('gszzl')),
            'estimate_time': data.get('gztime', ''),
            'source': 'fund_eastmoney_gz',
            'timestamp': datetime.now().isoformat(),
        }
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'估值请求失败: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise ProviderError('fund_eastmoney', f'估值数据解析失败: {e}')


# ============================================================
# 基金详情（基本信息 + 业绩 + 经理等）
# ============================================================

def fetch_fund_detail(fund_code: str, timeout: int = 10) -> Dict:
    """
    获取基金详情（综合信息）
    
    来源：天天基金移动端 API
    
    Args:
        fund_code: 6位基金代码
        timeout: 超时秒数
    
    Returns:
        dict: 包含基本信息、业绩、经理、费率等
    """
    url = "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo"
    params = {
        'plat': 'Android',
        'appType': 'ttjj',
        'product': 'EFund',
        'Version': '1',
        'deviceid': 'datafetcher',
        'Fcode': fund_code,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('ErrCode') != 0:
            raise ProviderError('fund_eastmoney', 
                f"基金{fund_code}详情接口错误: {data.get('ErrMsg', '未知错误')}")
        
        datas = data.get('Datas', {})
        if not datas:
            raise ProviderError('fund_eastmoney', f'基金{fund_code}详情数据为空')
        
        # 解析基本信息
        result = {
            'fund_code': fund_code,
            'fund_name': datas.get('SHORTNAME', ''),
            'fund_type': datas.get('FTYPE', ''),
            'fund_company': datas.get('JJGSID', ''),  # 基金公司ID
            'fund_company_name': datas.get('JJGS', ''),  # 基金公司名称
            'establishment_date': datas.get('ESTABDATE', ''),
            'fund_size': _safe_float(datas.get('ENDNAV')),  # 最新规模(亿)
            'fund_size_date': datas.get('FEGMRQ', ''),  # 规模截止日期
            'benchmark': datas.get('BENCH', ''),
            
            # 净值
            'nav': _safe_float(datas.get('DWJZ')),
            'acc_nav': _safe_float(datas.get('LJJZ')),
            'nav_date': datas.get('FSRQ', ''),
            'daily_return': _safe_float(datas.get('RZDF')),
            
            # 费率
            'management_fee': _safe_float(datas.get('MFEE')),
            'custody_fee': _safe_float(datas.get('CFEE')),
            'purchase_fee': _safe_float(datas.get('MAXSG')),
            'min_purchase': _safe_float(datas.get('MINSG')),
            
            # 风险等级
            'risk_level': datas.get('RISKLEVEL', ''),
            
            'source': 'fund_eastmoney_detail',
            'timestamp': datetime.now().isoformat(),
        }
        
        # 解析基金经理
        managers = datas.get('JJJL', [])
        if managers and isinstance(managers, list):
            mgr = managers[0] if managers else {}
            result['manager_name'] = mgr.get('NAME', '')
            result['manager_id'] = mgr.get('ID', '')
            result['manager_start_date'] = mgr.get('FEMPDATE', '')
            result['manager_days'] = _safe_int(mgr.get('DAYS'))
        else:
            result['manager_name'] = ''
            result['manager_id'] = ''
            result['manager_start_date'] = ''
            result['manager_days'] = 0
        
        return result
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'详情请求失败: {e}')
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ProviderError('fund_eastmoney', f'详情数据解析失败: {e}')


# ============================================================
# 基金阶段收益（业绩）
# ============================================================

def fetch_fund_performance(fund_code: str, timeout: int = 10) -> Dict:
    """
    获取基金阶段收益
    
    来源：天天基金移动端 API
    
    Args:
        fund_code: 6位基金代码
        timeout: 超时秒数
    
    Returns:
        dict: 各阶段收益率 + 同类排名
    """
    url = "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNPeriodIncrease"
    params = {
        'FCODE': fund_code,
        'deviceid': 'datafetcher',
        'plat': 'Iphone',
        'product': 'EFund',
        'Version': '6.3.8',
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('ErrCode') != 0:
            raise ProviderError('fund_eastmoney',
                f"基金{fund_code}业绩接口错误: {data.get('ErrMsg', '未知错误')}")
        
        datas = data.get('Datas', [])
        if not datas:
            raise ProviderError('fund_eastmoney', f'基金{fund_code}业绩数据为空')
        
        # 解析阶段收益
        # Datas 是一个列表，每个元素是不同时间段的收益
        result = {
            'fund_code': fund_code,
            'returns': {},
            'ranks': {},
            'similar_count': {},
            'source': 'fund_eastmoney_perf',
            'timestamp': datetime.now().isoformat(),
        }
        
        for item in datas:
            title = item.get('title', '')
            
            # 映射周期名称
            period_map = {
                '近一周': '1w', '近1周': '1w',
                '近一月': '1m', '近1月': '1m', '近一个月': '1m',
                '近三月': '3m', '近3月': '3m', '近三个月': '3m',
                '近六月': '6m', '近6月': '6m', '近六个月': '6m',
                '近一年': '1y', '近1年': '1y',
                '近二年': '2y', '近2年': '2y', '近两年': '2y',
                '近三年': '3y', '近3年': '3y',
                '近五年': '5y', '近5年': '5y',
                '今年来': 'ytd', '今年以来': 'ytd',
                '成立来': 'since_inception', '成立以来': 'since_inception',
            }
            
            period = period_map.get(title, title)
            
            syl = _safe_float(item.get('syl'))  # 收益率
            avg = _safe_float(item.get('avg'))  # 同类平均
            rank = item.get('rank', '')  # 排名 如 "123/456"
            sc = item.get('sc', '')  # 同类总数
            
            result['returns'][period] = syl
            if rank:
                result['ranks'][period] = rank
            if sc:
                result['similar_count'][period] = sc
        
        return result
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'业绩请求失败: {e}')
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ProviderError('fund_eastmoney', f'业绩数据解析失败: {e}')


# ============================================================
# 基金历史净值
# ============================================================

def fetch_fund_nav_history(fund_code: str, page_size: int = 20,
                           start_date: str = '', end_date: str = '',
                           timeout: int = 10) -> Dict:
    """
    获取基金历史净值
    
    来源：东方财富基金净值 API
    
    Args:
        fund_code: 6位基金代码
        page_size: 每页条数
        start_date: 起始日期 YYYY-MM-DD
        end_date: 结束日期 YYYY-MM-DD
        timeout: 超时秒数
    
    Returns:
        dict: {fund_code, records: [{date, nav, acc_nav, daily_return}]}
    """
    url = "https://api.fund.eastmoney.com/f10/lsjz"
    params = {
        'callback': 'jQuery',
        'fundCode': fund_code,
        'pageIndex': 1,
        'pageSize': page_size,
        'startDate': start_date,
        'endDate': end_date,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'Referer': 'https://fundf10.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        
        text = resp.text.strip()
        
        # 解析 JSONP: jQuery({...})
        match = re.search(r'jQuery\((.*)\)', text, re.DOTALL)
        if not match:
            raise ProviderError('fund_eastmoney', f'基金{fund_code}净值数据格式异常')
        
        data = json.loads(match.group(1))
        
        if data.get('ErrCode') != 0:
            raise ProviderError('fund_eastmoney',
                f"基金{fund_code}净值接口错误: {data.get('ErrMsg', '')}")
        
        result_data = data.get('Data', {})
        lsjz_list = result_data.get('LSJZList', [])
        
        records = []
        for item in lsjz_list:
            records.append({
                'date': item.get('FSRQ', ''),
                'nav': _safe_float(item.get('DWJZ')),
                'acc_nav': _safe_float(item.get('LJJZ')),
                'daily_return': _safe_float(item.get('JZZZL')),
                'dividend': item.get('FHSP', ''),
            })
        
        return {
            'fund_code': fund_code,
            'total_count': result_data.get('TotalCount', 0),
            'records': records,
            'source': 'fund_eastmoney_nav',
            'timestamp': datetime.now().isoformat(),
        }
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'净值请求失败: {e}')
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ProviderError('fund_eastmoney', f'净值数据解析失败: {e}')


# ============================================================
# 基金持仓（重仓股 + 资产配置）
# ============================================================

def fetch_fund_holdings(fund_code: str, timeout: int = 10) -> Dict:
    """
    获取基金重仓股
    
    来源：天天基金移动端 API
    
    Args:
        fund_code: 6位基金代码
        timeout: 超时秒数
    
    Returns:
        dict: {fund_code, stocks: [{name, code, percent, amount}], report_date}
    """
    url = "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition"
    params = {
        'FCODE': fund_code,
        'deviceid': 'datafetcher',
        'plat': 'Iphone',
        'product': 'EFund',
        'Version': '6.3.8',
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('ErrCode') != 0:
            raise ProviderError('fund_eastmoney',
                f"基金{fund_code}持仓接口错误: {data.get('ErrMsg', '未知错误')}")
        
        datas = data.get('Datas', {})
        
        # 重仓股
        stock_list = datas.get('fundStocks', [])
        stocks = []
        for s in stock_list:
            stocks.append({
                'name': s.get('GPJC', ''),
                'code': s.get('GPDM', ''),
                'percent': _safe_float(s.get('JZBL')),
                'amount': _safe_float(s.get('GPJZ')),
                'change': _safe_float(s.get('PCTNVCHG')),
            })
        
        # 重仓债券
        bond_list = datas.get('fundBoods', [])
        bonds = []
        for b in bond_list:
            bonds.append({
                'name': b.get('ZQMC', ''),
                'code': b.get('ZQDM', ''),
                'percent': _safe_float(b.get('ZJZBL')),
            })
        
        return {
            'fund_code': fund_code,
            'report_date': datas.get('FSRQ', ''),
            'stocks': stocks,
            'bonds': bonds,
            'stock_count': len(stocks),
            'top10_percent': sum(s['percent'] for s in stocks[:10]),
            'source': 'fund_eastmoney_holdings',
            'timestamp': datetime.now().isoformat(),
        }
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'持仓请求失败: {e}')
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ProviderError('fund_eastmoney', f'持仓数据解析失败: {e}')


# ============================================================
# 基金资产配置
# ============================================================

def fetch_fund_asset_allocation(fund_code: str, timeout: int = 10) -> Dict:
    """
    获取基金资产配置（股票/债券/现金占比）
    
    来源：天天基金移动端 API
    
    Args:
        fund_code: 6位基金代码
        timeout: 超时秒数
    
    Returns:
        dict: {fund_code, allocations: [{date, stock_pct, bond_pct, cash_pct, other_pct}]}
    """
    url = "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNAssetAllocationList"
    params = {
        'FCODE': fund_code,
        'deviceid': 'datafetcher',
        'plat': 'Iphone',
        'product': 'EFund',
        'Version': '6.3.8',
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('ErrCode') != 0:
            raise ProviderError('fund_eastmoney',
                f"基金{fund_code}资产配置接口错误: {data.get('ErrMsg', '未知错误')}")
        
        datas = data.get('Datas', [])
        
        allocations = []
        for item in datas:
            allocations.append({
                'date': item.get('FSRQ', ''),
                'stock_pct': _safe_float(item.get('GP')),
                'bond_pct': _safe_float(item.get('ZQ')),
                'cash_pct': _safe_float(item.get('HB')),
                'other_pct': _safe_float(item.get('QT')),
                'net_asset': _safe_float(item.get('JZC')),
            })
        
        return {
            'fund_code': fund_code,
            'allocations': allocations,
            'latest': allocations[0] if allocations else {},
            'source': 'fund_eastmoney_allocation',
            'timestamp': datetime.now().isoformat(),
        }
    
    except requests.RequestException as e:
        raise ProviderError('fund_eastmoney', f'资产配置请求失败: {e}')
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ProviderError('fund_eastmoney', f'资产配置数据解析失败: {e}')


# ============================================================
# 基金搜索
# ============================================================

def search_fund(keyword: str, timeout: int = 5) -> List[Dict]:
    """
    搜索基金（按代码或名称）
    
    Args:
        keyword: 基金代码或名称关键词
        timeout: 超时秒数
    
    Returns:
        list: [{fund_code, fund_name, fund_type}]
    """
    url = "https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx"
    params = {
        'callback': 'jQuery',
        'm': 1,
        'key': keyword,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=timeout, headers={
            'Referer': 'https://fund.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        
        text = resp.text.strip()
        match = re.search(r'jQuery\((.*)\)', text, re.DOTALL)
        if not match:
            return []
        
        data = json.loads(match.group(1))
        datas = data.get('Datas', [])
        
        results = []
        for item in datas:
            results.append({
                'fund_code': item.get('CODE', ''),
                'fund_name': item.get('NAME', ''),
                'fund_type': item.get('FundBaseInfo', {}).get('FTYPE', '') if isinstance(item.get('FundBaseInfo'), dict) else '',
                'fund_company': item.get('FundBaseInfo', {}).get('JJGS', '') if isinstance(item.get('FundBaseInfo'), dict) else '',
            })
        
        return results
    
    except Exception:
        return []


# ============================================================
# 工具函数
# ============================================================

def _safe_float(value, default: float = 0.0) -> float:
    """安全转换为 float"""
    if value is None or value == '' or value == '--':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_int(value, default: int = 0) -> int:
    """安全转换为 int"""
    if value is None or value == '' or value == '--':
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default
