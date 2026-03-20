#!/usr/bin/env python3
"""
行业分析师 - 数据获取脚本

基于肖璟《如何快速了解一个行业》分析行业生命周期、竞争格局、投资价值
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from datetime import datetime


def analyze_lifecycle(industry_name: str, growth_rate: float = None, market_size: str = None) -> dict:
    """
    行业生命周期分析
    
    Args:
        industry_name: 行业名称
        growth_rate: 行业增长率（%）
        market_size: 市场规模描述
    
    Returns:
        生命周期分析结果
    """
    result = {
        'industry': industry_name,
        'stage': '未知',
        'characteristics': [],
        'investment_strategy': '观察',
    }
    
    # 根据增长率判断生命周期阶段
    if growth_rate is not None:
        if growth_rate > 30:
            result['stage'] = '成长期'
            result['characteristics'] = [
                '市场快速扩大',
                '盈利改善',
                '竞争加剧',
            ]
            result['investment_strategy'] = '积极投资龙头'
        elif growth_rate > 10:
            result['stage'] = '成熟期早期'
            result['characteristics'] = [
                '增速放缓',
                '集中度提高',
                '现金牛企业',
            ]
            result['investment_strategy'] = '投资现金牛'
        elif growth_rate > 0:
            result['stage'] = '成熟期晚期'
            result['characteristics'] = [
                '增长停滞',
                '高度集中',
                '分红稳定',
            ]
            result['investment_strategy'] = '关注分红'
        else:
            result['stage'] = '衰退期'
            result['characteristics'] = [
                '市场萎缩',
                '利润下降',
                '企业退出',
            ]
            result['investment_strategy'] = '回避或做空'
    else:
        result['stage'] = '需要数据'
        result['characteristics'] = [
            '需要收集行业数据',
            '需要分析增长率',
            '需要评估渗透率',
        ]
    
    return result


def analyze_competition(industry_name: str, companies: list = None) -> dict:
    """
    竞争格局分析
    
    Args:
        industry_name: 行业名称
        companies: 公司列表（包含市场份额）
    
    Returns:
        竞争格局分析结果
    """
    result = {
        'industry': industry_name,
        'concentration': '未知',
        'cr3': None,  # 前 3 名份额
        'cr5': None,  # 前 5 名份额
        'competition_type': '未知',
        'companies': companies or [],
    }
    
    if companies and len(companies) > 0:
        # 计算 CR3 和 CR5
        sorted_companies = sorted(companies, key=lambda x: x.get('market_share', 0), reverse=True)
        
        cr3 = sum(c.get('market_share', 0) for c in sorted_companies[:3])
        cr5 = sum(c.get('market_share', 0) for c in sorted_companies[:5])
        
        result['cr3'] = cr3
        result['cr5'] = cr5
        
        # 判断竞争类型
        if cr3 > 70:
            result['concentration'] = '高度集中'
            result['competition_type'] = '寡头垄断'
        elif cr3 > 50:
            result['concentration'] = '中度集中'
            result['competition_type'] = '寡头竞争'
        elif cr5 > 50:
            result['concentration'] = '较低集中'
            result['competition_type'] = '垄断竞争'
        else:
            result['concentration'] = '分散'
            result['competition_type'] = '完全竞争'
    
    return result


def analyze_investment_value(industry_name: str, lifecycle: dict, competition: dict) -> dict:
    """
    投资价值评估
    
    Args:
        industry_name: 行业名称
        lifecycle: 生命周期分析结果
        competition: 竞争格局分析结果
    
    Returns:
        投资价值评估结果
    """
    result = {
        'industry': industry_name,
        'score': 0,
        'max_score': 10,
        'factors': [],
        'recommendation': '观察',
    }
    
    # 生命周期评分
    stage_scores = {
        '成长期': 3,
        '成熟期早期': 2,
        '成熟期晚期': 1,
        '衰退期': 0,
    }
    lifecycle_score = stage_scores.get(lifecycle.get('stage', ''), 1)
    result['score'] += lifecycle_score
    result['factors'].append(f"生命周期：{lifecycle.get('stage', '未知')} ({lifecycle_score}/3 分)")
    
    # 竞争格局评分
    concentration_scores = {
        '高度集中': 3,
        '中度集中': 2,
        '较低集中': 1,
        '分散': 0,
    }
    concentration_score = concentration_scores.get(competition.get('concentration', ''), 1)
    result['score'] += concentration_score
    result['factors'].append(f"竞争格局：{competition.get('concentration', '未知')} ({concentration_score}/3 分)")
    
    # 进入壁垒（简化，实际需要更多数据）
    result['factors'].append("❓ 进入壁垒：需要分析")
    result['score'] += 2  # 假设中等壁垒
    
    # 综合建议
    if result['score'] >= 8:
        result['recommendation'] = '强烈推荐'
    elif result['score'] >= 6:
        result['recommendation'] = '推荐'
    elif result['score'] >= 4:
        result['recommendation'] = '观察'
    else:
        result['recommendation'] = '回避'
    
    return result


def analyze_industry(industry_name: str, growth_rate: float = None, companies: list = None) -> dict:
    """
    行业完整分析
    
    Args:
        industry_name: 行业名称
        growth_rate: 行业增长率（%）
        companies: 公司列表
    
    Returns:
        分析结果字典
    """
    result = {
        'industry': industry_name,
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
    }
    
    # 生命周期分析
    result['lifecycle'] = analyze_lifecycle(industry_name, growth_rate)
    
    # 竞争格局分析
    result['competition'] = analyze_competition(industry_name, companies)
    
    # 投资价值评估
    result['investment_value'] = analyze_investment_value(
        industry_name,
        result['lifecycle'],
        result['competition']
    )
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"🏭 行业分析师：{result['industry']}")
    print("="*60)
    
    # 生命周期
    lifecycle = result.get('lifecycle', {})
    print(f"\n📊 生命周期分析")
    print(f"   阶段：{lifecycle.get('stage', '未知')}")
    for char in lifecycle.get('characteristics', []):
        print(f"   • {char}")
    print(f"   投资策略：{lifecycle.get('investment_strategy', 'N/A')}")
    
    # 竞争格局
    competition = result.get('competition', {})
    print(f"\n🏆 竞争格局")
    if competition.get('cr3'):
        print(f"   CR3: {competition['cr3']:.1f}%")
    if competition.get('cr5'):
        print(f"   CR5: {competition['cr5']:.1f}%")
    print(f"   集中度：{competition.get('concentration', '未知')}")
    print(f"   竞争类型：{competition.get('competition_type', '未知')}")
    
    if competition.get('companies'):
        print(f"\n   主要公司：")
        for company in competition['companies'][:5]:
            name = company.get('name', 'Unknown')
            share = company.get('market_share', 0)
            print(f"   • {name}: {share:.1f}%")
    
    # 投资价值
    value = result.get('investment_value', {})
    print(f"\n💎 投资价值评估")
    print(f"   评分：{value.get('score', 0)}/{value.get('max_score', 10)}")
    for factor in value.get('factors', []):
        print(f"   • {factor}")
    print(f"   建议：{value.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    else:
        print(f"\n⚠️  数据来源：手动输入（需要搜索补充）")
    
    # 免责声明
    print(f"\n⚠️  免责声明")
    print(f"   本分析仅供参考，不构成投资建议")
    print(f"   请结合其他因素综合判断")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 analyze-industry.py <行业名称> [增长率%]")
        print("示例：python3 analyze-industry.py 新能源汽车 35")
        return 1
    
    industry_name = sys.argv[1]
    growth_rate = float(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # 示例公司数据（实际应从搜索或数据库获取）
    companies = []
    
    result = analyze_industry(industry_name, growth_rate, companies)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
