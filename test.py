import os
import io
import sys
from datetime import datetime
from contextlib import redirect_stdout

from agent import graph

# ============================================================
# 5 TEST CASES theo đề bài
# ============================================================
TEST_CASES = [
    {
        "id": 1,
        "name": "Direct Answer — Không cần tool",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "expect": "Agent chào hỏi, hỏi thêm sở thích/ngân sách/thời gian. Không gọi tool.",
        "expect_tool_calls": 0,
    },
    {
        "id": 2,
        "name": "Single Tool Call — Tìm chuyến bay",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "expect": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.",
        "expect_tool_calls": 1,
    },
    {
        "id": 3,
        "name": "Multi-Step Tool Chaining — Kế hoạch trọn gói",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "expect": "Agent chuỗi 3 tools: search_flights → search_hotels → calculate_budget.",
        "expect_tool_calls": 3,
    },
    {
        "id": 4,
        "name": "Missing Info — Hỏi lại khi thiếu thông tin",
        "input": "Tôi muốn đặt khách sạn",
        "expect": "Hỏi lại: thành phố? bao nhiêu đêm? ngân sách? Không gọi tool.",
        "expect_tool_calls": 0,
    },
    {
        "id": 5,
        "name": "Guardrail — Từ chối ngoài phạm vi",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "expect": "Từ chối lịch sự, nói chỉ hỗ trợ về du lịch.",
        "expect_tool_calls": 0,
    },
]


def run_test(tc: dict) -> dict:
    """Chạy một test case, capture stdout (logs từ agent_node), trả về kết quả."""
    buf = io.StringIO()
    error = None
    result_messages = []

    try:
        with redirect_stdout(buf):
            result = graph.invoke({"messages": [("human", tc["input"])]})
        result_messages = result["messages"]
    except Exception as e:
        error = str(e)

    logs = buf.getvalue().strip()
    tool_call_count = logs.count("Gọi tool:")
    final_answer = result_messages[-1].content if result_messages else "(no response)"

    return {
        "logs": logs or "(no tool calls)",
        "answer": final_answer,
        "tool_call_count": tool_call_count,
        "error": error,
    }


def check_pass(tc: dict, result: dict) -> bool:
    if result["error"]:
        return False
    return result["tool_call_count"] == tc["expect_tool_calls"]


def format_section(tc: dict, result: dict) -> str:
    status = "✅ PASS" if check_pass(tc, result) else "❌ FAIL"
    error_block = f"\n**Error:**\n```\n{result['error']}\n```\n" if result["error"] else ""

    return f"""## Test {tc['id']}: {tc['name']} — {status}

**Input:** `{tc['input']}`

**Kỳ vọng:** {tc['expect']}

| | Kỳ vọng | Thực tế |
|---|---|---|
| Tool calls | {tc['expect_tool_calls']} | {result['tool_call_count']} |
{error_block}
**Agent Logs (stdout):**
{result['logs']}

**Agent Answer:**
> {result['answer']}

---
"""


def main():
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{timestamp}.md"

    print("=" * 55)
    print("  TravelBuddy — Test Runner")
    print("=" * 55)

    results = []
    for tc in TEST_CASES:
        print(f"[Test {tc['id']}] {tc['name']}...", end=" ", flush=True)
        r = run_test(tc)
        results.append(r)
        print("PASS" if check_pass(tc, r) else "FAIL")

    # --- Build report ---
    passed = sum(1 for tc, r in zip(TEST_CASES, results) if check_pass(tc, r))
    total = len(TEST_CASES)
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    header = f"""# Test Run Log — {run_time}

## Summary: {passed}/{total} passed

| Test | Name | Tool calls (expect→actual) | Status |
|---|---|---|---|
"""
    for tc, r in zip(TEST_CASES, results):
        status = "✅ PASS" if check_pass(tc, r) else "❌ FAIL"
        header += f"| {tc['id']} | {tc['name']} | {tc['expect_tool_calls']} → {r['tool_call_count']} | {status} |\n"

    header += "\n---\n\n"

    sections = [format_section(tc, r) for tc, r in zip(TEST_CASES, results)]

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(sections))

    print("=" * 55)
    print(f"  Result: {passed}/{total} passed")
    print(f"  Log saved → {log_file}")
    print("=" * 55)


if __name__ == "__main__":
    main()