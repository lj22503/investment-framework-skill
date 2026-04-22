"""
data_fetcher 核心模块

提供统一的 DataFetcher 接口，支持多数据源自动降级和缓存。
"""

import os
import sys
import time
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# 添加父目录到路径（用于导入 providers）
_Framework_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _Framework_Dir)

from data_fetcher.exceptions import DataFetchError
from data_fetcher.config import load_config
from data_fetcher.cache import CacheManager
from data_fetcher.providers.tencent import fetch_tencent_quote, fetch_tencent_index
from data_fetcher.providers.sina import fetch_sina_quote, fetch_sina_index
from data_fetcher.providers.eastmoney import fetch_eastmoney_quote, fetch_eastmoney_financials

logger = logging.getLogger(__name__)


@dataclass
class Quote:
    """个股行情数据结构"""
    symbol: str
    name: str
    price: float
    change: float = 0.0
    change_percent: float = 0.0
    volume: int = 0
    turnover: float = 0.0
    high: float = 0.0
    low: float = 0.0
    open: float = 0.0
    prev_close: float = 0.0
    market_cap: float = 0.0
    pe: float = 0.0
    pb: float = 0.0
    source: str = "unknown"
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """从字典创建 Quote 对象"""
        return cls(
            symbol=data.get('symbol', ''),
            name=data.get('name', ''),
            price=data.get('price', 0.0),
            change=data.get('change', 0.0),
            change_percent=data.get('change_percent', 0.0),
            volume=data.get('volume', 0),
            turnover=data.get('turnover', 0.0),
            high=data.get('high', 0.0),
            low=data.get('low', 0.0),
            open=data.get('open', 0.0),
            prev_close=data.get('prev_close', 0.0),
            market_cap=data.get('market_cap', 0.0),
            pe=data.get('pe', 0.0),
            pb=data.get('pb', 0.0),
            source=data.get('source', 'unknown'),
            timestamp=data.get('timestamp', ''),
        )


@dataclass
class IndexData:
    """大盘指数数据结构"""
    symbol: str
    name: str
    price: float
    change: float = 0.0
    change_percent: float = 0.0
    volume: int = 0
    turnover: float = 0.0  # 亿元
    source: str = "unknown"
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            symbol=data.get('symbol', ''),
            name=data.get('name', ''),
            price=data.get('price', 0.0),
            change=data.get('change', 0.0),
            change_percent=data.get('change_percent', 0.0),
            volume=data.get('volume', 0),
            turnover=data.get('turnover', 0.0),
            source=data.get('source', 'unknown'),
            timestamp=data.get('timestamp', ''),
        )


@dataclass
class Financials:
    """财务数据结构"""
    symbol: str
    revenue: float = 0.0       # 营业收入（亿元）
    net_profit: float = 0.0     # 净利润（亿元）
    roe: float = 0.0           # 净资产收益率
    debt_ratio: float = 0.0    # 资产负债率
    gross_margin: float = 0.0  # 毛利率
    net_margin: float = 0.0   # 净利率
    source: str = "unknown"
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            symbol=data.get('symbol', ''),
            revenue=data.get('revenue', 0.0),
            net_profit=data.get('net_profit', 0.0),
            roe=data.get('roe', 0.0),
            debt_ratio=data.get('debt_ratio', 0.0),
            gross_margin=data.get('gross_margin', 0.0),
            net_margin=data.get('net_margin', 0.0),
            source=data.get('source', 'unknown'),
            timestamp=data.get('timestamp', ''),
        )


class DataFetcher:
    """
    统一数据获取接口
    
    支持多数据源自动降级、缓存、配置管理。
    
    使用示例：
        fetcher = DataFetcher()
        
        # 获取个股行情（自动降级）
        quote = fetcher.get_quote('600519.SH')
        print(f"贵州茅台: ¥{quote.price}")
        
        # 获取大盘指数
        indices = fetcher.get_indices(['000001.SH', '399001.SZ', '399006.SZ'])
        for idx in indices:
            print(f"{idx.name}: {idx.price} ({idx.change_percent}%)")
        
        # 获取财务数据
        financials = fetcher.get_financials('600519.SH')
        print(f"ROE: {financials.roe}%")
    """
    
    # 数据源优先级（免费数据源）
    DEFAULT_PRIORITY = ['tencent', 'sina', 'eastmoney']
    
    # 数据源到函数的映射
    QUOTE_FETCHERS = {
        'tencent': fetch_tencent_quote,
        'sina': fetch_sina_quote,
        'eastmoney': fetch_eastmoney_quote,
    }
    
    INDEX_FETCHERS = {
        'tencent': fetch_tencent_index,
        'sina': fetch_sina_index,
    }
    
    def __init__(self, config_path: Optional[str] = None, 
                 enable_cache: bool = True,
                 cache_ttl: int = 300):
        """
        初始化 DataFetcher
        
        Args:
            config_path: 配置文件路径，默认使用 ~/.investment_framework/config.yaml
            enable_cache: 是否启用缓存
            cache_ttl: 缓存有效期（秒）
        """
        self.config = load_config(config_path)
        self.enable_cache = enable_cache and self.config.get('fallback', {}).get('use_cache', True)
        self.cache_ttl = cache_ttl or self.config.get('fallback', {}).get('cache_ttl', 300)
        
        if self.enable_cache:
            self.cache = CacheManager(ttl=self.cache_ttl)
        else:
            self.cache = None
        
        self.timeout = self.config.get('fallback', {}).get('timeout', 5)
        self.priority = self.config.get('data_sources', {}).get('priority', self.DEFAULT_PRIORITY)
        
        logger.info(f"DataFetcher 初始化完成，缓存: {'启用' if self.enable_cache else '禁用'}, "
                    f"TTL: {self.cache_ttl}s, 优先级: {self.priority}")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """从缓存获取"""
        if self.cache:
            cached = self.cache.get(key)
            if cached and isinstance(cached, dict):
                # 根据 key 前缀重建正确的 dataclass
                if key.startswith("index:"):
                    return IndexData(**cached)
                elif key.startswith("quote:"):
                    return Quote(**cached)
                elif key.startswith("financials:"):
                    return Financials(**cached)
            return cached
        return None
    
    def _set_cache(self, key: str, value: Any):
        """设置缓存"""
        if self.cache:
            # 将 dataclass 转为 dict 再序列化
            if hasattr(value, '__dataclass_fields__'):
                self.cache.set(key, value.__dict__)
            else:
                self.cache.set(key, value)
    
    def get_quote(self, symbol: str, use_cache: bool = True) -> Quote:
        """
        获取个股行情
        
        按优先级尝试各数据源，失败则自动降级。
        
        Args:
            symbol: 股票代码（如：600519.SH）
            use_cache: 是否使用缓存，默认 True
        
        Returns:
            Quote 对象
        
        Raises:
            DataFetchError: 所有数据源都失败时抛出
        """
        cache_key = f"quote:{symbol}"
        
        # 检查缓存
        if use_cache and self.enable_cache:
            cached = self._get_cached(cache_key)
            if cached:
                logger.debug(f"缓存命中: {symbol}")
                return cached
        
        # 按优先级尝试数据源
        last_error = None
        for source in self.priority:
            if source not in self.QUOTE_FETCHERS:
                continue
            
            fetcher = self.QUOTE_FETCHERS[source]
            try:
                start_time = time.time()
                data = fetcher(symbol, timeout=self.timeout)
                elapsed = time.time() - start_time
                
                if data and data.get('price', 0) > 0:
                    data['source'] = source
                    data['timestamp'] = data.get('timestamp') or self._now_iso()
                    quote = Quote.from_dict(data)
                    
                    logger.info(f"获取成功: {symbol} @ {source} ({elapsed*1000:.0f}ms) = ¥{quote.price}")
                    
                    # 写入缓存
                    if use_cache:
                        self._set_cache(cache_key, quote)
                    
                    return quote
                    
            except DataFetchError as e:
                last_error = e
                logger.warning(f"{source} 获取失败: {e}")
                continue
            except Exception as e:
                last_error = DataFetchError(f"{source} 异常: {e}")
                logger.error(f"{source} 异常: {e}")
                continue
        
        # 全部失败，检查是否允许手动输入
        if self.config.get('fallback', {}).get('allow_manual_input', True):
            logger.info(f"所有数据源失败，返回手动输入模式: {symbol}")
            return self._manual_input_quote(symbol)
        
        raise DataFetchError(f"获取 {symbol} 失败，所有数据源均不可用: {last_error}")
    
    def get_indices(self, symbols: Optional[List[str]] = None) -> List[IndexData]:
        """
        获取大盘指数
        
        Args:
            symbols: 指数代码列表，默认获取主要指数
        
        Returns:
            IndexData 列表
        """
        if symbols is None:
            symbols = ['s_sh000001', 's_sz399001', 's_sz399006', 's_sh000300']
        
        results = []
        
        # 优先使用腾讯
        try:
            tencent_fetcher = fetch_tencent_index
            for sym in symbols:
                cache_key = f"index:{sym}"
                
                if self.enable_cache:
                    cached = self._get_cached(cache_key)
                    if cached:
                        results.append(cached)
                        continue
                
                try:
                    data = tencent_fetcher(sym, timeout=self.timeout)
                    if data:
                        data['source'] = 'tencent'
                        data['timestamp'] = data.get('timestamp') or self._now_iso()
                        index = IndexData.from_dict(data)
                        
                        if self.enable_cache:
                            self._set_cache(cache_key, index)
                        
                        results.append(index)
                except DataFetchError as e:
                    logger.warning(f"获取指数失败: {sym} -> {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"腾讯指数获取出错: {e}")
        
        # 如果腾讯全部失败，尝试新浪
        if not results:
            try:
                sina_fetcher = fetch_sina_index
                for sym in symbols:
                    try:
                        data = sina_fetcher(sym, timeout=self.timeout)
                        if data:
                            data['source'] = 'sina'
                            data['timestamp'] = data.get('timestamp') or self._now_iso()
                            index = IndexData.from_dict(data)
                            results.append(index)
                    except DataFetchError:
                        continue
            except Exception as e:
                logger.error(f"新浪指数获取出错: {e}")
        
        return results
    
    def get_financials(self, symbol: str, use_cache: bool = True) -> Financials:
        """
        获取财务数据
        
        主要使用东方财富 API，失败则尝试其他源。
        
        Args:
            symbol: 股票代码
            use_cache: 是否使用缓存
        
        Returns:
            Financials 对象
        """
        cache_key = f"financials:{symbol}"
        
        if use_cache and self.enable_cache:
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        try:
            data = fetch_eastmoney_financials(symbol, timeout=self.timeout)
            if data:
                data['source'] = 'eastmoney'
                financials = Financials.from_dict(data)
                
                if use_cache:
                    self._set_cache(cache_key, financials)
                
                return financials
        except DataFetchError as e:
            logger.warning(f"东方财富财务数据获取失败: {e}")
        
        # 返回空财务数据
        return Financials(symbol=symbol, source="unknown")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        if self.cache:
            return self.cache.get_stats()
        return {"enabled": False}
    
    def clear_cache(self):
        """清空缓存"""
        if self.cache:
            self.cache.clear()
    
    def _now_iso(self) -> str:
        """返回当前时间的 ISO 格式字符串"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _manual_input_quote(self, symbol: str) -> Quote:
        """手动输入降级方案"""
        print(f"\n⚠️  无法自动获取 {symbol} 数据，请手动输入：")
        try:
            price = float(input("  当前价格: ") or 0)
            pe = float(input("  市盈率 (PE): ") or 0)
            pb = float(input("  市净率 (PB): ") or 0)
            name = input("  股票名称: ") or symbol
            
            return Quote(
                symbol=symbol,
                name=name,
                price=price,
                pe=pe,
                pb=pb,
                source="manual"
            )
        except (ValueError, KeyboardInterrupt):
            return Quote(symbol=symbol, name=symbol, price=0, source="manual")
