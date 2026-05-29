#!/usr/bin/env python3
"""
investment-framework v4.1.0 DAIR-AI 框架优化验证 - 完整测试执行脚本

实际调用 LLM API 执行所有测试用例，验证输出质量。
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# 测试用例文件
TEST_CASES_FILE = Path(__file__).parent / "test-cases-v4.1.0.json"

# 从 openclaw.json 读取 API 配置
def load_api_config():
    """加载 API 配置"""
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 使用 dashscope 配置
    dashscope_cfg = config.get('models', {}).get('providers', {}).get('dashscope', {})
    return {
        "base_url": dashscope_cfg.get('baseUrl', 'https://dashscope.aliyuncs.com/compatible-mode/v1'),
        "api_key": dashscope_cfg.get('apiKey', ''),
        "model": 'qwen3.5-plus'  # 使用优化后的模型
    }

def load_test_cases():
    """加载测试用例"""
    with open(TEST_CASES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_prompt(test_case):
    """为测试用例创建提示词"""
    return f"""你是一个专业投资顾问，基于经典投资框架（格雷厄姆/巴菲特/芒格/马尔基尔/林森池）提供分析支持。

请根据用户请求，调用合适的投资分析技能，生成结构化投资建议。

**关键规则**:
- 必须逐步推理，展示分析过程
- 必须输出 JSON 格式，字段完整
- 对于不确定的信息，标注置信度
- 必须包含免责声明

输出必须为以下 JSON 格式，不得包含额外解释：

```json
{{
  "status": "success | error",
  "data": {{
    "request_type": "个股分析 | 趋势分析 | 资产配置 | 决策检查",
    "skills_used": ["skill-name-1", "skill-name-2"],
    "analysis_result": {{}},
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "confidence": "高 | 中 | 低",
    "key_risks": ["风险 1", "风险 2"],
    "action_items": ["行动 1", "行动 2"],
    "next_steps": ["下一步 1", "下一步 2"],
    "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。请独立判断并自行承担风险。"
  }}
}}
```

用户输入：{test_case['input']}

请直接输出 JSON，不要有任何额外解释。"""

def run_llm_test(prompt, api_config):
    """调用 LLM API 执行测试"""
    try:
        client = OpenAI(
            base_url=api_config['base_url'],
            api_key=api_config['api_key']
        )
        
        response = client.chat.completions.create(
            model=api_config['model'],
            messages=[
                {"role": "system", "content": "你是一个专业投资顾问。请严格按照 JSON 格式输出，不要有任何额外解释。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,  # 低温保证稳定性
            max_tokens=4096
        )
        
        return {
            "success": True,
            "output": response.choices[0].message.content,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": None
        }

def validate_json_format(output):
    """验证 JSON 格式"""
    try:
        # 尝试提取 JSON（处理可能的 markdown 代码块）
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()
        
        data = json.loads(output)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, str(e)

def check_required_fields(data, required_fields):
    """检查必填字段"""
    if not isinstance(data, dict):
        return False, ["data 不是对象"]
    
    if "data" not in data:
        return False, ["缺少 data 字段"]
    
    data_content = data["data"]
    if not isinstance(data_content, dict):
        return False, ["data 字段不是对象"]
    
    missing = []
    for field in required_fields:
        if field not in data_content:
            missing.append(field)
    
    return len(missing) == 0, missing

def check_enum_values(data):
    """检查枚举字段值"""
    errors = []
    
    data_content = data.get("data", {})
    
    # 检查 request_type
    request_type = data_content.get("request_type")
    valid_request_types = ["个股分析", "趋势分析", "资产配置", "决策检查"]
    if request_type and request_type not in valid_request_types:
        errors.append(f"request_type 无效：{request_type}")
    
    # 检查 recommendation
    recommendation = data_content.get("recommendation")
    valid_recommendations = ["强烈推荐", "推荐", "观察", "谨慎", "避免"]
    if recommendation and recommendation not in valid_recommendations:
        errors.append(f"recommendation 无效：{recommendation}")
    
    # 检查 confidence
    confidence = data_content.get("confidence")
    valid_confidences = ["高", "中", "低"]
    if confidence and confidence not in valid_confidences:
        errors.append(f"confidence 无效：{confidence}")
    
    return len(errors) == 0, errors

def run_all_tests():
    """运行所有测试"""
    print("🧪 investment-framework v4.1.0 完整测试执行")
    print("=" * 60)
    
    # 加载配置
    api_config = load_api_config()
    print(f"📡 API 配置：{api_config['base_url']}")
    print(f"🤖 模型：{api_config['model']}")
    print()
    
    # 加载测试用例
    test_suite = load_test_cases()
    test_cases = test_suite["test_cases"]
    print(f"📋 测试用例：{len(test_cases)}个")
    print()
    
    # 执行测试
    results = []
    total_tokens = {"input": 0, "output": 0}
    
    for i, case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] 执行 {case['id']}: {case['category']} - {case['input'][:30]}...")
        
        # 创建提示词
        prompt = create_prompt(case)
        
        # 调用 LLM
        llm_result = run_llm_test(prompt, api_config)
        
        if not llm_result["success"]:
            print(f"   ❌ API 调用失败：{llm_result['error']}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "input": case["input"],
                "status": "failed",
                "format_valid": False,
                "fields_complete": False,
                "enum_valid": False,
                "error": f"API 调用失败：{llm_result['error']}",
                "output": None
            })
            continue
        
        # 更新 token 统计
        if "usage" in llm_result:
            total_tokens["input"] += llm_result["usage"].get("input_tokens", 0)
            total_tokens["output"] += llm_result["usage"].get("output_tokens", 0)
        
        # 验证 JSON 格式
        format_valid, data, json_error = validate_json_format(llm_result["output"])
        
        if not format_valid:
            print(f"   ❌ JSON 格式失败：{json_error}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "input": case["input"],
                "status": "failed",
                "format_valid": False,
                "fields_complete": False,
                "enum_valid": False,
                "error": f"JSON 格式失败：{json_error}",
                "output": llm_result["output"][:500]  # 只保存前 500 字符
            })
            continue
        
        # 检查必填字段
        fields_complete, missing_fields = check_required_fields(data, case["required_fields"])
        
        if not fields_complete:
            print(f"   ⚠️  字段缺失：{missing_fields}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "input": case["input"],
                "status": "failed",
                "format_valid": True,
                "fields_complete": False,
                "enum_valid": False,
                "error": f"字段缺失：{missing_fields}",
                "output": llm_result["output"][:500]
            })
            continue
        
        # 检查枚举值
        enum_valid, enum_errors = check_enum_values(data)
        
        if not enum_valid:
            print(f"   ⚠️  枚举值无效：{enum_errors}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "input": case["input"],
                "status": "failed",
                "format_valid": True,
                "fields_complete": True,
                "enum_valid": False,
                "error": f"枚举值无效：{enum_errors}",
                "output": llm_result["output"][:500]
            })
            continue
        
        # 检查预期状态（如果有）
        if "expected_status" in case:
            if data.get("status") != case["expected_status"]:
                print(f"   ⚠️  状态不符：期望 {case['expected_status']}, 实际 {data.get('status')}")
                results.append({
                    "id": case["id"],
                    "category": case["category"],
                    "input": case["input"],
                    "status": "failed",
                    "format_valid": True,
                    "fields_complete": True,
                    "enum_valid": True,
                    "error": f"状态不符：期望 {case['expected_status']}, 实际 {data.get('status')}",
                    "output": llm_result["output"][:500]
                })
                continue
        
        print(f"   ✅ 通过")
        results.append({
            "id": case["id"],
            "category": case["category"],
            "input": case["input"],
            "status": "passed",
            "format_valid": True,
            "fields_complete": True,
            "enum_valid": True,
            "error": None,
            "output": llm_result["output"][:500],
            "expected_skills": case.get("expected_skills", [])
        })
    
    print()
    print("=" * 60)
    print(f"✅ 测试完成！")
    print(f"📊 Token 使用：输入 {total_tokens['input']:,} / 输出 {total_tokens['output']:,}")
    print()
    
    return results, test_suite, total_tokens

def generate_report(results, test_suite, total_tokens):
    """生成测试报告"""
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    
    # 计算指标
    format_pass_rate = sum(1 for r in results if r["format_valid"]) / total * 100 if total > 0 else 0
    field_completeness = sum(1 for r in results if r["fields_complete"]) / total * 100 if total > 0 else 0
    enum_valid_rate = sum(1 for r in results if r["enum_valid"]) / total * 100 if total > 0 else 0
    overall_pass_rate = passed / total * 100 if total > 0 else 0
    
    # 按类别统计
    by_category = {}
    for r in results:
        cat = r["category"]
        if cat not in by_category:
            by_category[cat] = {"passed": 0, "failed": 0, "total": 0}
        by_category[cat]["total"] += 1
        if r["status"] == "passed":
            by_category[cat]["passed"] += 1
        else:
            by_category[cat]["failed"] += 1
    
    report = f"""# investment-framework v4.1.0 测试报告

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**测试套件**: {test_suite['test_suite']}
**版本**: {test_suite['version']}
**模型**: qwen3.5-plus

---

## 📊 总体结果

| 指标 | 结果 | 目标 | 状态 |
|------|------|------|------|
| 总用例数 | {total} | - | - |
| 通过 | {passed} | - | {'✅' if passed == total else '⚠️'} |
| 失败 | {failed} | 0 | {'✅' if failed == 0 else '⚠️'} |
| 通过率 | {overall_pass_rate:.1f}% | 100% | {'✅' if overall_pass_rate == 100 else '⚠️'} |

**Token 使用**: 输入 {total_tokens['input']:,} / 输出 {total_tokens['output']:,}

---

## 📈 评估指标

| 指标 | 当前值 | 目标值 | 状态 |
|------|--------|--------|------|
| JSON 格式通过率 | {format_pass_rate:.1f}% | ≥95% | {'✅' if format_pass_rate >= 95 else '⚠️'} |
| 字段完整率 | {field_completeness:.1f}% | 100% | {'✅' if field_completeness == 100 else '⚠️'} |
| 枚举值正确率 | {enum_valid_rate:.1f}% | 100% | {'✅' if enum_valid_rate == 100 else '⚠️'} |
| 整体通过率 | {overall_pass_rate:.1f}% | 100% | {'✅' if overall_pass_rate == 100 else '⚠️'} |

---

## 📋 按类别统计

| 类别 | 总数 | 通过 | 失败 | 通过率 |
|------|------|------|------|--------|
"""
    
    for cat, stats in sorted(by_category.items()):
        rate = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        report += f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} | {rate:.1f}% |\n"
    
    report += f"""
---

## ❌ 失败用例详情

"""
    
    failed_cases = [r for r in results if r["status"] == "failed"]
    if failed_cases:
        for r in failed_cases:
            report += f"### {r['id']}: {r['category']}\n\n"
            report += f"- **输入**: {r['input']}\n"
            report += f"- **错误**: {r['error']}\n"
            if r['output']:
                report += f"- **输出预览**: `{r['output'][:100]}...`\n"
            report += "\n"
    else:
        report += "**无失败用例** ✅\n\n"
    
    report += f"""---

## 📝 结论与建议

"""
    
    if overall_pass_rate == 100:
        report += f"""### ✅ 测试通过

所有 {total} 个测试用例均通过验证！

**优化效果确认**:
- JSON 格式通过率：{format_pass_rate:.1f}% (目标≥95%) ✅
- 字段完整率：{field_completeness:.1f}% (目标 100%) ✅
- 枚举值正确率：{enum_valid_rate:.1f}% (目标 100%) ✅

**建议**: 可以发布 v4.1.0 版本。
"""
    else:
        report += f"""### ⚠️ 需要改进

{failed} 个测试用例失败，需要进一步优化。

**主要问题**:
"""
        # 统计错误类型
        error_types = {}
        for r in failed_cases:
            error_type = r['error'].split(':')[0] if ':' in r['error'] else '其他'
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in error_types.items():
            report += f"- {error_type}: {count}例\n"
        
        report += f"""
**建议**:
1. 分析失败用例，调整提示词
2. 增加 Few-shot 示例覆盖失败场景
3. 强化负面约束
4. 重新执行测试
"""
    
    report += f"""
---

## 📎 附录：测试用例列表

"""
    
    for r in results:
        status_icon = "✅" if r["status"] == "passed" else "❌"
        report += f"- {status_icon} {r['id']}: {r['input'][:60]}...\n"
    
    return report

def main():
    """主函数"""
    # 运行测试
    results, test_suite, total_tokens = run_all_tests()
    
    # 生成报告
    report = generate_report(results, test_suite, total_tokens)
    
    # 保存报告
    report_file = Path(__file__).parent / f"test-report-v4.1.0-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 测试报告已保存到：{report_file}")
    print()
    
    # 打印摘要
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    print(f"📊 测试结果：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("✅ 所有测试通过！可以发布 v4.1.0")
    else:
        print(f"⚠️  {total - passed} 个测试失败，需要优化")

if __name__ == "__main__":
    main()
