#!/usr/bin/env python3
"""
investment-framework v4.1.0 完整测试执行脚本 - 简化版（仅使用标准库）
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# 配置文件
CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"
TEST_CASES_FILE = Path(__file__).parent / "test-cases-v4.1.0.json"

def load_config():
    """加载 API 配置"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    dashscope = config.get('models', {}).get('providers', {}).get('dashscope', {})
    return {
        "base_url": dashscope.get('baseUrl'),
        "api_key": dashscope.get('apiKey'),
        "model": 'qwen3.5-plus'
    }

def load_test_cases():
    """加载测试用例"""
    with open(TEST_CASES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def call_llm_api(prompt, config):
    """调用 LLM API（使用标准库）"""
    url = f"{config['base_url']}/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}"
    }
    
    data = {
        "model": config['model'],
        "messages": [
            {"role": "system", "content": "你是一个专业投资顾问。请严格按照 JSON 格式输出，不要有任何额外解释。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 4096
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "output": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {})
            }
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.read().decode('utf-8')[:200]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_prompt(input_text):
    """创建提示词"""
    return f"""请根据用户请求，调用合适的投资分析技能，生成结构化投资建议。

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

用户输入：{input_text}

请直接输出 JSON，不要有任何额外解释。"""

def validate_output(output, required_fields, expected_status=None):
    """验证输出"""
    try:
        # 处理 markdown 代码块
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()
        
        data = json.loads(output)
        
        # 检查必填字段
        data_content = data.get("data", {})
        missing = [f for f in required_fields if f not in data_content]
        
        if missing:
            return False, f"字段缺失：{missing}", data
        
        # 检查预期状态
        if expected_status and data.get("status") != expected_status:
            return False, f"状态不符：期望 {expected_status}, 实际 {data.get('status')}", data
        
        return True, None, data
    
    except json.JSONDecodeError as e:
        return False, f"JSON 格式失败：{str(e)}", None

def main():
    """主函数"""
    print("🧪 investment-framework v4.1.0 完整测试执行")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    print(f"📡 API: {config['base_url']}")
    print(f"🤖 模型：{config['model']}")
    print()
    
    # 加载测试用例
    test_suite = load_test_cases()
    test_cases = test_suite["test_cases"]
    print(f"📋 测试用例：{len(test_cases)}个")
    for cat, count in test_suite['categories'].items():
        print(f"   - {cat}: {count}个")
    print()
    print("=" * 60)
    print()
    
    # 执行测试
    results = []
    total_tokens = {"input": 0, "output": 0}
    
    for i, case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] {case['id']}: {case['input'][:40]}...")
        
        # 创建提示词
        prompt = create_prompt(case['input'])
        
        # 调用 API
        llm_result = call_llm_api(prompt, config)
        
        if not llm_result["success"]:
            print(f"   ❌ API 失败：{llm_result['error'][:50]}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "status": "failed",
                "error": llm_result["error"],
                "output": None
            })
            continue
        
        # 更新 token 统计
        if "usage" in llm_result:
            total_tokens["input"] += llm_result["usage"].get("prompt_tokens", 0)
            total_tokens["output"] += llm_result["usage"].get("completion_tokens", 0)
        
        # 验证输出
        valid, error, data = validate_output(
            llm_result["output"],
            case["required_fields"],
            case.get("expected_status")
        )
        
        if valid:
            print(f"   ✅ 通过")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "status": "passed",
                "error": None,
                "output": llm_result["output"][:300]
            })
        else:
            print(f"   ❌ {error[:50]}")
            results.append({
                "id": case["id"],
                "category": case["category"],
                "status": "failed",
                "error": error,
                "output": llm_result["output"][:300]
            })
    
    print()
    print("=" * 60)
    
    # 统计结果
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = total - passed
    pass_rate = passed / total * 100 if total > 0 else 0
    
    print(f"✅ 测试完成！")
    print(f"📊 Token 使用：输入 {total_tokens['input']:,} / 输出 {total_tokens['output']:,}")
    print(f"📊 结果：{passed}/{total} 通过 ({pass_rate:.1f}%)")
    
    if passed == total:
        print("✅ 所有测试通过！可以发布 v4.1.0")
    else:
        print(f"⚠️  {failed} 个测试失败")
    
    # 保存结果
    results_dir = Path(__file__).parent / f"results-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    results_dir.mkdir(exist_ok=True)
    
    with open(results_dir / "results.json", 'w', encoding='utf-8') as f:
        json.dump({
            "test_suite": test_suite["test_suite"],
            "version": test_suite["version"],
            "timestamp": datetime.now().isoformat(),
            "total_tokens": total_tokens,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📄 结果已保存：{results_dir}/results.json")

if __name__ == "__main__":
    main()
