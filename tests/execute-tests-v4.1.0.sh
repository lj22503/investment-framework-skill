#!/bin/bash
# investment-framework v4.1.0 完整测试执行脚本 (curl 版本)

set -e

echo "🧪 investment-framework v4.1.0 完整测试执行"
echo "============================================================"

# 读取 API 配置
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BASE_URL=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['models']['providers']['dashscope']['baseUrl'])")
API_KEY=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['models']['providers']['dashscope']['apiKey'])")
MODEL="qwen3.5-plus"

echo "📡 API: $BASE_URL"
echo "🤖 模型：$MODEL"
echo ""

# 测试用例 JSON 文件
TEST_CASES_FILE="$(dirname "$0")/test-cases-v4.1.0.json"

# 创建临时目录存储结果
RESULTS_DIR="$(dirname "$0")/results-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RESULTS_DIR"

# 系统提示词
SYSTEM_PROMPT="你是一个专业投资顾问，基于经典投资框架（格雷厄姆/巴菲特/芒格/马尔基尔/林森池）提供分析支持。你必须输出严格的 JSON 格式，不要有任何额外解释。"

# 计数器
total=0
passed=0
failed=0

# 读取测试用例并逐个执行
python3 << PYTHON_SCRIPT
import json
import subprocess
import os
from datetime import datetime

# 加载测试用例
with open("$TEST_CASES_FILE", 'r', encoding='utf-8') as f:
    test_suite = json.load(f)

test_cases = test_suite["test_cases"]
print(f"📋 测试用例：{len(test_cases)}个")
print(f"   - 个股分析：{test_suite['categories']['个股分析']}个")
print(f"   - 趋势分析：{test_suite['categories']['趋势分析']}个")
print(f"   - 资产配置：{test_suite['categories']['资产配置']}个")
print(f"   - 决策检查：{test_suite['categories']['决策检查']}个")
print(f"   - 边界情况：{test_suite['categories']['边界情况']}个")
print()
print("=" * 60)
print()

results = []
total_tokens_input = 0
total_tokens_output = 0

for i, case in enumerate(test_cases, 1):
    case_id = case["id"]
    category = case["category"]
    input_text = case["input"]
    required_fields = case["required_fields"]
    expected_status = case.get("expected_status")
    
    print(f"[{i}/{len(test_cases)}] 执行 {case_id}: {category} - {input_text[:40]}...")
    
    # 创建提示词
    user_prompt = f"""请根据用户请求，调用合适的投资分析技能，生成结构化投资建议。

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
    
    # 调用 API
    curl_cmd = f'''curl -s "{os.environ.get('BASE_URL')}" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer {os.environ.get('API_KEY')}" \\
  -d '{{
    "model": "{os.environ.get('MODEL')}",
    "messages": [
      {{"role": "system", "content": "你是一个专业投资顾问。请严格按照 JSON 格式输出，不要有任何额外解释。"}},
      {{"role": "user", "content": """{user_prompt}"""}}
    ],
    "temperature": 0,
    "max_tokens": 4096
  }}' '''
    
    # 保存结果到文件
    result_file = f"{os.environ.get('RESULTS_DIR')}/{case_id}.json"
    
    # 执行 curl 命令
    try:
        result = subprocess.run(
            ["curl", "-s", os.environ.get('BASE_URL'),
             "-H", "Content-Type: application/json",
             "-H", f"Authorization: Bearer {os.environ.get('API_KEY')}",
             "-d", json.dumps({
                 "model": os.environ.get('MODEL'),
                 "messages": [
                     {"role": "system", "content": "你是一个专业投资顾问。请严格按照 JSON 格式输出，不要有任何额外解释。"},
                     {"role": "user", "content": user_prompt}
                 ],
                 "temperature": 0,
                 "max_tokens": 4096
             })],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        api_response = json.loads(result.stdout)
        output = api_response["choices"][0]["message"]["content"]
        
        # 提取 token 使用
        if "usage" in api_response:
            total_tokens_input += api_response["usage"].get("prompt_tokens", 0)
            total_tokens_output += api_response["usage"].get("completion_tokens", 0)
        
        # 验证 JSON 格式
        try:
            # 处理 markdown 代码块
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].split("```")[0].strip()
            
            data = json.loads(output)
            
            # 检查必填字段
            data_content = data.get("data", {})
            missing_fields = [f for f in required_fields if f not in data_content]
            
            if missing_fields:
                print(f"   ⚠️  字段缺失：{missing_fields}")
                results.append({
                    "id": case_id,
                    "category": category,
                    "input": input_text,
                    "status": "failed",
                    "format_valid": True,
                    "fields_complete": False,
                    "error": f"字段缺失：{missing_fields}",
                    "output": output[:500]
                })
            else:
                # 检查预期状态
                if expected_status and data.get("status") != expected_status:
                    print(f"   ⚠️  状态不符：期望 {expected_status}, 实际 {data.get('status')}")
                    results.append({
                        "id": case_id,
                        "category": category,
                        "input": input_text,
                        "status": "failed",
                        "format_valid": True,
                        "fields_complete": True,
                        "error": f"状态不符：期望 {expected_status}, 实际 {data.get('status')}",
                        "output": output[:500]
                    })
                else:
                    print(f"   ✅ 通过")
                    results.append({
                        "id": case_id,
                        "category": category,
                        "input": input_text,
                        "status": "passed",
                        "format_valid": True,
                        "fields_complete": True,
                        "error": None,
                        "output": output[:500]
                    })
        
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON 格式失败：{str(e)[:50]}")
            results.append({
                "id": case_id,
                "category": category,
                "input": input_text,
                "status": "failed",
                "format_valid": False,
                "fields_complete": False,
                "error": f"JSON 格式失败：{str(e)}",
                "output": output[:500] if output else None
            })
    
    except subprocess.TimeoutExpired:
        print(f"   ❌ 超时")
        results.append({
            "id": case_id,
            "category": category,
            "input": input_text,
            "status": "failed",
            "format_valid": False,
            "fields_complete": False,
            "error": "API 调用超时",
            "output": None
        })
    except Exception as e:
        print(f"   ❌ 错误：{str(e)[:50]}")
        results.append({
            "id": case_id,
            "category": category,
            "input": input_text,
            "status": "failed",
            "format_valid": False,
            "fields_complete": False,
            "error": str(e),
            "output": None
        })

print()
print("=" * 60)
print(f"✅ 测试完成！")
print(f"📊 Token 使用：输入 {total_tokens_input:,} / 输出 {total_tokens_output:,}")
print()

# 保存结果
with open(f"{os.environ.get('RESULTS_DIR')}/results.json", 'w', encoding='utf-8') as f:
    json.dump({"results": results, "total_tokens": {"input": total_tokens_input, "output": total_tokens_output}}, f, ensure_ascii=False, indent=2)

print(f"📄 结果已保存到：{os.environ.get('RESULTS_DIR')}/results.json")

# 计算统计
total = len(results)
passed = sum(1 for r in results if r["status"] == "passed")
failed = total - passed
pass_rate = passed / total * 100 if total > 0 else 0

print(f"📊 测试结果：{passed}/{total} 通过 ({pass_rate:.1f}%)")

if passed == total:
    print("✅ 所有测试通过！可以发布 v4.1.0")
else:
    print(f"⚠️  {failed} 个测试失败，需要优化")

PYTHON_SCRIPT
