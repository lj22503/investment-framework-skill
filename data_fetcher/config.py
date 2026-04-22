"""
data_fetcher 配置管理

管理数据源优先级、API Keys、降级策略。
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_CONFIG = {
    'data_sources': {
        'priority': ['tencent', 'sina', 'eastmoney'],
    },
    'api_keys': {
        'tushare': {
            'token': '',
            'enabled': False,
        },
        'lixinger': {
            'token': '',
            'enabled': False,
        },
    },
    'fallback': {
        'use_cache': True,
        'cache_ttl': 300,
        'allow_manual_input': True,
        'timeout': 5,
    },
    'preferences': {
        'a_share_prefix': {
            'sh': 'sh',
            'sz': 'sz',
        },
        'default_fields': ['price', 'change_percent', 'pe', 'pb', 'market_cap'],
    },
}


def get_config_path() -> Path:
    """获取配置文件路径"""
    config_dir = Path(os.path.expanduser("~/.investment_framework"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径，默认 ~/.investment_framework/config.yaml
    
    Returns:
        配置字典
    """
    if config_path is None:
        config_path = get_config_path()
    else:
        config_path = Path(config_path)
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            # 合并默认配置
            merged = DEFAULT_CONFIG.copy()
            _deep_merge(merged, config)
            return merged
        except (yaml.YAMLError, IOError) as e:
            import logging
            logging.warning(f"配置文件读取失败: {e}，使用默认配置")
            return DEFAULT_CONFIG.copy()
    
    # 配置文件不存在，创建默认配置
    save_config(DEFAULT_CONFIG, config_path)
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any], config_path: Optional[str] = None):
    """
    保存配置文件
    
    Args:
        config: 配置字典
        config_path: 配置文件路径
    """
    if config_path is None:
        config_path = get_config_path()
    else:
        config_path = Path(config_path)
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def _deep_merge(base: Dict, overlay: Dict) -> Dict:
    """深度合并字典"""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base
