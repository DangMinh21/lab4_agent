# Lab 4: Xây Dựng AI Agent Đầu Tiên Với LangGraph
**AI in Action — Vingrouph & VinUniversity**

**Học viện: Đặng Văn Minh**
**MSHV: 2A202600027**

TravelBuddy là một AI Agent tư vấn du lịch thông minh, tự động tra cứu chuyến bay, khách sạn và tính toán ngân sách thông qua vòng lặp Agent–Tool của
LangGraph.

---

## Kiến trúc

**Nodes:**
- `agent` — GPT-4o-mini với system prompt, quyết định gọi tool hay trả lời thẳng
- `tools` — LangGraph ToolNode thực thi 3 custom tools

**Edges:**
- `START → agent`
- `agent → tools` (nếu có tool_calls) hoặc `agent → END`
- `tools → agent` (luôn quay lại để tổng hợp)

---

## Cấu Trúc Project
```
lab4_agent/
├── agent.py            # LangGraph graph: nodes, edges, chat loop
├── tools.py            # 3 custom tools + mock data
├── system_prompt.txt   # System prompt định hình hành vi agent
├── test.py             # Test runner tự động 10 test cases
├── test_results.md     # Kết quả test thủ công (console log)
├── logs/               # Kết quả test tự động (markdown, có timestamp)
└── .env                # API key (không commit)
```
---

## Cài Đặt

**Yêu cầu:** Python 3.9+

```bash
# 1. Tạo và kích hoạt virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows

# 2. Cài đặt thư viện
pip install langchain langchain-openai langgraph python-dotenv

# 3. Tạo file .env
echo "OPENAI_API_KEY=sk-proj-..." > .env

---
Chạy Agent

python agent.py

Agent sẽ khởi động chế độ chat tương tác:

============================================================
TravelBuddy — Trợ lý Du lịch Thông minh
    Gõ 'quit' để thoát
============================================================

Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu
TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 5000000, ...})
Trả lời trực tiếp

TravelBuddy: ...

Gõ quit, exit hoặc q để thoát.

---
Chạy Tests

python test.py

Kết quả in ra console và tự động lưu vào logs/YYYYMMDD_HHMMSS.md:

=======================================================
  TravelBuddy — Test Runner
=======================================================
[Test 1] Direct Answer — Không cần tool... PASS
[Test 2] Single Tool Call — Tìm chuyến bay... PASS
[Test 3] Multi-Step Tool Chaining — Kế hoạch trọn gói... PASS
...
=======================================================
  Result: 9/10 passed
  Log saved → logs/20260407_153621.md
=======================================================
```
---

## Quá Trình Thực Hiện

### Phần 1 — System Prompt
Thiết kế system prompt dạng XML với 4 khối: `<persona>`, `<rules>`, `<tools_instruction>`, `<response_format>`, `<constraints>`. Qua 2 vòng chỉnh sửa:
- **V1:** Agent bỏ qua `calculate_budget`, tự tính toán trong câu trả lời → thêm rule bắt buộc dùng tool.
- **V2:** Rule quá rộng khiến agent hỏi lại khi không cần → chỉ định rõ input tối thiểu cho từng tool.

### Phần 2 — Custom Tools (`tools.py`)
Implement 3 tools theo thứ tự tăng dần độ phức tạp:

- **`search_flights`:** Tra cứu tuple key, xử lý chiều ngược với cảnh báo rõ ràng trong output.
- **`search_hotels`:** Lọc theo giá, sort rating giảm dần, ẩn sentinel value `99999999` khỏi output.
- **`calculate_budget`:** Parse chuỗi `"tên:số"`, xử lý lỗi format, in bảng chi tiết, cảnh báo vượt ngân sách.

Lý do dùng format `"tên_khoản:số_tiền"` thay vì JSON: LLM ít bị lỗi syntax hơn khi sinh chuỗi đơn giản.

### Phần 3 — LangGraph Agent (`agent.py`)
Xây dựng graph với 2 nodes (`agent`, `tools`) và conditional edges. Agent tự quyết định gọi tool bao nhiêu lần dựa trên `tools_condition` của LangGraph — không cần hard-code thứ tự.

### Phần 4 — Testing
Viết `test.py` tự động hóa 10 test cases, capture stdout để đếm tool calls, lưu kết quả vào `logs/` có timestamp. Chạy 2 vòng:
- **Vòng 1 (baseline):** 4/5 pass — Test 3 fail vì agent tự tính thay vì dùng tool.
- **Vòng 2 (sau cải thiện prompt):** 9/10 pass — Test 7 agent dùng domain knowledge (Hội An không có sân bay) thay vì gọi tool, đây là hành vi đúng về nghiệp vụ dù lệch metric.