from langchain_core import tools

from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Tra cứu theo chiều thuận trước.
    # FLIGHTS_DB dùng tuple (origin, destination) làm key nên phải tra chính xác.
    flights = FLIGHTS_DB.get((origin, destination))

    # Nếu không có chiều thuận, thử chiều ngược.
    # Phân biệt hai trường hợp để thông báo rõ cho user:
    # - Tìm thấy chiều thuận → trả về bình thường
    # - Chỉ có chiều ngược → trả về nhưng cảnh báo rõ
    # - Không có cả hai → báo không tìm thấy
    reversed_found = False
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if flights:
            reversed_found = True

    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Header khác nhau tùy trường hợp tìm thấy thuận hay ngược chiều.
    if reversed_found:
        header = (
            f"Không tìm thấy chuyến bay từ {origin} → {destination}.\n"
            f"Chỉ tìm thấy thông tin chiều ngược ({destination} → {origin}):\n"
        )
    else:
        header = f"Các chuyến bay từ {origin} → {destination}:\n"

    lines = [header]
    for f in flights:
        price_fmt = f"{f['price']:,}".replace(",", ".")
        lines.append(
            f"  • {f['airline']} | {f['departure']} → {f['arrival']}"
            f" | Hạng {f['class']} | {price_fmt}đ"
        )

    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # Tra cứu danh sách khách sạn theo thành phố.
    # Trả về list rỗng nếu thành phố không có trong DB,
    # tránh KeyError làm crash tool.
    hotels = HOTELS_DB.get(city, [])

    # Lọc theo ngân sách.
    # Lý do để filter ở đây thay vì để LLM tự filter:
    # LLM không đáng tin khi làm toán → tool phải làm thay.
    # Default 99999999 đảm bảo "không truyền max_price" = lấy tất cả.
    affordable = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    # Nếu không có kết quả sau khi lọc → gợi ý tăng ngân sách thay vì trả về rỗng.
    # Lý do: giúp agent đưa ra lời khuyên hữu ích thay vì chỉ báo "không có".
    if not affordable:
        price_fmt = f"{max_price_per_night:,}".replace(",", ".")
        
        if max_price_per_night == 99999999:
            return (f"Không tìm thấy khách sạn tại {city}")
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới {price_fmt}đ/đêm. "
            f"Hãy thử tăng ngân sách."
        )

    # Sắp xếp theo rating giảm dần để gợi ý tốt nhất lên đầu.
    # Lý do: LLM thường dùng vài kết quả đầu tiên → đặt chất lượng cao lên trước.
    affordable.sort(key=lambda h: h["rating"], reverse=True)

    # Chỉ hiển thị giá lọc trong header nếu user thực sự truyền vào.
    # Lý do: giá trị mặc định 99999999 là sentinel nội bộ, không có ý nghĩa với user.
    if max_price_per_night == 99999999:
        header = f"Khách sạn tại {city}:\n"
    else:
        price_fmt = f"{max_price_per_night:,}".replace(",", ".")
        header = f"Khách sạn tại {city} (giá ≤ {price_fmt}đ/đêm):\n"

    lines = [header]
    for h in affordable:
        price_fmt = f"{h['price_per_night']:,}".replace(",", ".")
        # Format đầy đủ: tên, sao, khu vực, giá, rating
        # Đặt rating cuối để LLM dễ extract khi cần so sánh.
        stars = h["stars"]
        lines.append(
            f"  • {h['name']} | {stars} Sao | {h['area']}"
            f" | {price_fmt}đ/đêm | Rating: {h['rating']}"
        )

    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
    định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # Parse chuỗi expenses thành dict {tên: số_tiền}.
    # Lý do dùng format "tên:số" thay vì JSON: LLM sinh text tự nhiên hơn,
    # ít bị hallucinate syntax lỗi hơn so với yêu cầu nó viết JSON thuần.
    parsed = {}
    try:
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue

            # Tách tại dấu ":" đầu tiên, maxsplit=1 để tên khoản có thể chứa ":"
            parts = item.split(":", maxsplit=1)
            if len(parts) != 2:
                # Format sai → báo lỗi rõ khoản nào bị sai thay vì crash toàn bộ.
                return (
                    f"Lỗi định dạng tại khoản '{item}'. "
                    f"Vui lòng dùng định dạng: 'tên_khoản:số_tiền' "
                    f"(VD: 'vé_máy_bay:890000,khách_sạn:650000')"
                )

            name = parts[0].strip().replace("_", " ")  # "vé_máy_bay" → "vé máy bay"
            amount_str = parts[1].strip()

            # Ép kiểu int, bắt lỗi nếu LLM truyền vào số không hợp lệ (VD: "890k")
            try:
                parsed[name] = int(float(amount_str))  # float trước để xử lý "890000.0"
            except ValueError:
                return (
                    f"Lỗi: '{amount_str}' không phải số hợp lệ cho khoản '{name}'. "
                    f"Vui lòng dùng số nguyên (VD: 890000)."
                )

    except Exception as e:
        # Bắt mọi lỗi parse không lường trước, trả về message thay vì crash.
        return f"Lỗi xử lý expenses: {str(e)}. Vui lòng kiểm tra lại định dạng."

    # Tính tổng chi phí
    total_spent = sum(parsed.values())
    remaining = total_budget - total_spent

    # --- Format bảng chi tiết ---
    # Dùng format rõ ràng để LLM dễ đọc và trích dẫn con số trong câu trả lời.
    lines = ["Bảng chi phí:"]
    for name, amount in parsed.items():
        amount_fmt = f"{amount:,}".replace(",", ".")
        lines.append(f"  - {name.capitalize()}: {amount_fmt}đ")

    lines.append("  ---")
    lines.append(f"  Tổng chi:   {f'{total_spent:,}'.replace(',', '.')}đ")
    lines.append(f"  Ngân sách:  {f'{total_budget:,}'.replace(',', '.')}đ")

    # Phân nhánh kết quả: còn dư hay vượt ngân sách
    if remaining >= 0:
        lines.append(f"  Còn lại:    {f'{remaining:,}'.replace(',', '.')}đ ✓")
    else:
        # Số âm → đổi sang dương để thông báo dễ hiểu hơn.
        over = f"{abs(remaining):,}".replace(",", ".")
        lines.append(f"  Còn lại:    -")
        lines.append(f"\n⚠️  Vượt ngân sách {over}đ! Cần điều chỉnh.")

    return "\n".join(lines)


if __name__ == "__main__":
    
    print(f"========== Test Search Flight tool ============")
    # Test chiều thuận
    print(search_flights.invoke({"origin": "Hà Nội", "destination": "Đà Nẵng"}))
    print("---")
    # Test chiều ngược
    print(search_flights.invoke({"origin": "Đà Nẵng", "destination": "Hà Nội"}))
    print("---")
    # Test không tồn tại
    print(search_flights.invoke({"origin": "Hà Nội", "destination": "Tokyo"}))

    print(f"========== Test Search Hotel tool ============")

    # Test không lọc giá
    print(search_hotels.invoke({"city": "Đà Nẵng"}))
    print("---")
    # Test lọc giá (chỉ lấy <= 500.000đ)
    print(search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 500000}))
    print("---")
    # Test thành phố không có trong DB
    print(search_hotels.invoke({"city": "Hà Nội"}))

    print(f"========== Test Calculate Budget tool ============")

    # Test bình thường - còn dư
    print(
        calculate_budget.invoke(
            {"total_budget": 5000000, "expenses": "vé_máy_bay:1100000,khách_sạn:800000"}
        )
    )
    print("---")
    # Test vượt ngân sách
    print(
        calculate_budget.invoke(
            {
                "total_budget": 2000000,
                "expenses": "vé_máy_bay:1100000,khách_sạn:1500000",
            }
        )
    )
    print("---")
    # Test format lỗi
    print(
        calculate_budget.invoke({"total_budget": 5000000, "expenses": "vé_máy_bay:abc"})
    )
