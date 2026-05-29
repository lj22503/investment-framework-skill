#!/usr/bin/env python3
"""
investment-framework v4.1.0 手动测试脚本
由当前会话的 LLM 执行测试用例，验证优化效果
"""

import json
from datetime import datetime
from pathlib import Path

TEST_CASES_FILE = Path(__file__).parent / "test-cases-v4.1.0.json"

def load_test_cases():
    with open(TEST_CASES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("🧪 investment-framework v4.1.0 手动测试")
    print("=" * 60)
    
    test_suite = load_test_cases()
    test_cases = test_suite["test_cases"]
    
    print(f"测试用例：{len(test_cases)}个")
    print(f"版本：{test_suite['version']}")
    print()
    
    # 创建测试执行文件
    exec_file = Path(__file__).parent / "manual-test-inputs.md"
    
    with open(exec_file, 'w', encoding='utf-8') as f:
        f.write(f"# investment-framework v4.1.0 手动测试输入\n\n")
        f.write(f"**版本**: {test_suite['version']}\n")
        f.write(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"请将以下内容逐个发送给 LLM，记录输出并验证。\n\n")
        f.write(f"---\n\n")
        
        for case in test_cases:
            f.write(f"## {case['id']}: {case['category']}\n\n")
            f.write(f"**输入**:\n")
            f.write(f"```\n{case['input']}\n```\n\n")
            f.write(f"**预期技能**: {case.get('expected_skills', 'N/A')}\n\n")
            f.write(f"**必填字段**: {case['required_fields']}\n\n")
            if 'expected_status' in case:
                f.write(f"**预期状态**: {case['expected_status']}\n\n")
            f.write(f"**输出**:\n")
            f.write(f"```json\n\n```\n\n")
            f.write(f"**验证**:\n")
            f.write(f"- [ ] JSON 格式有效\n")
            f.write(f"- [ ] 字段完整\n")
            f.write(f"- [ ] 枚举值正确\n")
            f.write(f"- [ ] 推理连贯\n\n")
            f.write(f"---\n\n")
    
    print(f"📄 测试输入文件已创建：{exec_file}")
    print()
    print("下一步：")
    print("1. 打开 manual-test-inputs.md 文件")
    print("2. 逐个将输入发送给 LLM")
    print("3. 记录输出并勾选验证项")
    print("4. 统计通过率")
    print()
    print("或者，让我现在就开始执行前 5 个测试用例作为抽样测试？")

if __name__ == "__main__":
    main()
