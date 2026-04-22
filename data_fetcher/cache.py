"""
data_fetcher 缓存管理模块
"""

import time
import json
import os
from typing import Optional, Any, Dict
from pathlib import Path


class CacheManager:
    """
    简单的内存 + 磁盘缓存管理器
    
    TTL: Time To Live，缓存有效期（秒）
    """
    
    def __init__(self, ttl: int = 300, cache_dir: Optional[str] = None):
        """
        Args:
            ttl: 缓存有效期（秒），默认 5 分钟
            cache_dir: 磁盘缓存目录，默认 ~/.investment_framework/cache
        """
        self.ttl = ttl
        self._memory_cache: Dict[str, tuple] = {}  # key -> (value, expire_timestamp)
        
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.investment_framework/cache")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _make_key(self, key: str) -> str:
        """生成安全的文件名"""
        return key.replace(":", "_").replace("/", "_")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        now = time.time()
        
        # 1. 先查内存缓存
        if key in self._memory_cache:
            value, expire = self._memory_cache[key]
            if now < expire:
                return value
            else:
                del self._memory_cache[key]
        
        # 2. 查磁盘缓存
        cache_file = self.cache_dir / f"{self._make_key(key)}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                
                if now < entry['expire']:
                    # 写回内存
                    self._memory_cache[key] = (entry['value'], entry['expire'])
                    return entry['value']
                else:
                    try:
                        cache_file.unlink()
                    except FileNotFoundError:
                        pass
            except (json.JSONDecodeError, KeyError, IOError):
                pass
        
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        now = time.time()
        expire = now + self.ttl
        
        # 写内存
        self._memory_cache[key] = (value, expire)
        
        # 写磁盘
        cache_file = self.cache_dir / f"{self._make_key(key)}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'key': key,
                    'value': value if isinstance(value, (dict, list, str, int, float, bool, type(None))) else str(value),
                    'expire': expire,
                    'timestamp': now,
                }, f, ensure_ascii=False, indent=2, default=str)
        except (IOError, TypeError) as e:
            import logging
            logging.warning(f"磁盘缓存写入失败: {e}")
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        cache_file = self.cache_dir / f"{self._make_key(key)}.json"
        try:
            cache_file.unlink()
        except FileNotFoundError:
            pass
    
    def clear(self):
        """清空所有缓存"""
        self._memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except FileNotFoundError:
                pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        now = time.time()
        valid_count = sum(1 for _, expire in self._memory_cache.values() if now < expire)
        
        disk_files = list(self.cache_dir.glob("*.json"))
        
        return {
            "enabled": True,
            "ttl": self.ttl,
            "memory_entries": len(self._memory_cache),
            "memory_valid": valid_count,
            "disk_entries": len(disk_files),
            "cache_dir": str(self.cache_dir),
        }
