import streamlit as st
from datetime import date

st.set_page_config(page_title="대학 행사 식자재 주문", page_icon="🛒")

# ---------- [Task 2] Demo 상품 데이터 ----------
# 실제 회사 데이터가 아닌, 프로젝트용으로 만든 가상 데이터
PRODUCTS = [
    {"id": 1, "icon": "🥩", "name": "냉장 삼겹살", "unit": "1kg", "price": 18900},
    {"id": 2, "icon": "🥩", "name": "냉장 목살", "unit": "1kg", "price": 17500},
    {"id": 3, "icon": "🌭", "name": "비엔나 소시지", "unit": "1kg", "price": 9800},
    {"id": 4, "icon": "🥬", "name": "쌈채소 모둠", "unit": "1kg", "price": 6900},
    {"id": 5, "icon": "🥫", "name": "쌈장", "unit": "2kg", "price": 7800},
    {"id": 6, "icon": "🥢", "name": "포기김치", "unit": "5kg", "price": 22000},
    {"id": 7, "icon": "🍚", "name": "즉석밥", "unit": "210g x 24개", "price": 21600},
    {"id": 8, "icon": "🍜", "name": "컵라면", "unit": "24개입", "price": 19800},
    {"id": 9, "icon": "💧", "name": "생수", "unit": "2L x 6병", "price": 4500},
    {"id": 10, "icon": "🥤", "name": "탄산음료", "unit": "1.5L x 12병", "price": 18000},
    {"id": 11, "icon": "🔥", "name": "바비큐용 숯", "unit": "3kg", "price": 8900},
    {"id": 12, "icon": "🥤", "name": "일회용 종이컵", "unit": "1,000개", "price": 15000},
]

# ---------- [Task 5] Demo 학생회 고객 데이터 ----------
# 실제 고객정보가 아닌 가상 데이터. 미주문 고객은 주문금액 0원
DEMO_CUSTOMERS = [
    {"school": "부경대학교", "major": "경영학과", "event_type": "축제", "event_date": date(2026, 10, 22), "people": 120, "status": "주문 완료", "amount": 412000},
    {"school": "부경대학교", "major": "컴퓨터공학과", "event_type": "축제", "event_date": date(2026, 10, 22), "people": 90, "status": "주문 완료", "amount": 298500},
    {"school": "부경대학교", "major": "식품공학과", "event_type": "축제", "event_date": date(2026, 10, 23), "people": 70, "status": "주문 대기", "amount": 215800},
    {"school": "부경대학교", "major": "해양학과", "event_type": "축제", "event_date": date(2026, 10, 23), "people": 60, "status": "미주문", "amount": 0},
    {"school": "부경대학교", "major": "국어국문학과", "event_type": "MT", "event_date": date(2026, 11, 7), "people": 45, "status": "주문 대기", "amount": 168300},
    {"school": "부경대학교", "major": "물리학과", "event_type": "MT", "event_date": date(2026, 11, 14), "people": 35, "status": "미주문", "amount": 0},
    {"school": "부산대학교", "major": "경제학과", "event_type": "축제", "event_date": date(2026, 10, 29), "people": 110, "status": "주문 완료", "amount": 365400},
    {"school": "부산대학교", "major": "기계공학과", "event_type": "축제", "event_date": date(2026, 10, 29), "people": 95, "status": "주문 대기", "amount": 287200},
    {"school": "부산대학교", "major": "사회학과", "event_type": "축제", "event_date": date(2026, 10, 30), "people": 50, "status": "미주문", "amount": 0},
]


def get_product(product_id):
    """상품 id로 상품 정보를 찾아서 돌려줌"""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p


def add_to_cart(product_id):
    """[담기] 버튼을 누르면 실행: 해당 상품 수량을 1 늘림"""
    cart = st.session_state.cart
    cart[product_id] = cart.get(product_id, 0) + 1


def show_dashboard():
    """[Task 5] 유통사 직원용 Dashboard"""
    st.title("📊 유통사 Dashboard")
    st.caption("Demo 학생회 데이터와 이번 접속에서 들어온 주문을 함께 보여줍니다.")

    # Demo 고객 + 학생회 화면에서 실제로 들어온 주문을 합침
    all_orders = DEMO_CUSTOMERS + st.session_state.orders

    # 학교 선택 필터
    schools = sorted(set(o["school"] for o in all_orders))
    selected = st.selectbox("학교 선택", ["전체"] + schools)
    if selected != "전체":
        all_orders = [o for o in all_orders if o["school"] == selected]

    # 1) 전체 요약 숫자
    count_done = len([o for o in all_orders if o["status"] == "주문 완료"])
    count_wait = len([o for o in all_orders if o["status"] == "주문 대기"])
    count_none = len([o for o in all_orders if o["status"] == "미주문"])
    total_amount = sum(o["amount"] for o in all_orders)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("주문 완료", f"{count_done}곳")
    c2.metric("주문 대기", f"{count_wait}곳")
    c3.metric("미주문", f"{count_none}곳")
    c4.metric("현재 주문금액", f"{total_amount:,}원")

    # 2) 대학 + 행사 유형별로 묶어서 집계
    st.subheader("대학 · 행사 유형별 현황")
    groups = {}
    for o in all_orders:
        key = (o["school"], o["event_type"])  # 예: ("부경대학교", "축제")
        if key not in groups:
            groups[key] = {
                "학교": o["school"], "행사 유형": o["event_type"],
                "등록 고객": 0, "주문 완료": 0, "주문 대기": 0, "미주문": 0,
                "현재 주문금액": 0,
            }
        g = groups[key]
        g["등록 고객"] += 1
        g[o["status"]] += 1  # 해당 상태 칸의 숫자를 1 늘림
        g["현재 주문금액"] += o["amount"]

    summary_rows = list(groups.values())
    for row in summary_rows:
        row["현재 주문금액"] = f"{row['현재 주문금액']:,}원"
    st.dataframe(summary_rows, hide_index=True)

    # 3) 학생회 고객 목록
    st.subheader("학생회 고객 목록")
    customer_rows = []
    for o in all_orders:
        customer_rows.append({
            "학교": o["school"],
            "학과": o["major"],
            "행사 유형": o["event_type"],
            "행사일": str(o["event_date"]),
            "예상 인원": o["people"],
            "주문 상태": o["status"],
            "주문금액": f"{o['amount']:,}원",
        })
    st.dataframe(customer_rows, hide_index=True)


# 지금 어떤 화면을 보여줄지 기억하는 변수 (처음엔 행사정보 입력 화면)
if "step" not in st.session_state:
    st.session_state.step = "event"

# [Task 2] 장바구니: {상품id: 수량} 형태로 저장
if "cart" not in st.session_state:
    st.session_state.cart = {}

# [Task 4] 주문 목록: 주문할 때마다 하나씩 추가 (Task 5 Dashboard에서 사용)
if "orders" not in st.session_state:
    st.session_state.orders = []

# ---------- [Task 5] 사용자 유형 선택 (왼쪽 사이드바) ----------
mode = st.sidebar.radio("사용자 선택", ["학생회", "유통사 직원"])
if mode == "유통사 직원":
    show_dashboard()
    st.stop()  # 여기서 멈추고, 아래 학생회 화면은 그리지 않음

# ---------- 화면 1: 행사정보 입력 ----------
if st.session_state.step == "event":
    st.title("🎉 행사 정보 입력")

    school = st.text_input("학교", placeholder="예: 부경대학교")
    major = st.text_input("학과", placeholder="예: 경영학과")
    event_type = st.selectbox("행사 종류", ["MT", "축제", "기타"])
    event_date = st.date_input("행사일")
    people = st.number_input("예상 참여 인원", min_value=1, value=30, step=1)

    if st.button("다음"):
        # 학교·학과가 비어 있으면 넘어가지 않음
        if school.strip() == "" or major.strip() == "":
            st.error("학교와 학과를 입력해 주세요.")
        else:
            # 입력한 정보를 저장하고 다음 화면으로 이동
            st.session_state.event = {
                "school": school.strip(),
                "major": major.strip(),
                "event_type": event_type,
                "event_date": event_date,
                "people": people,
            }
            st.session_state.step = "products"
            st.rerun()

# ---------- 화면 2: 상품 탐색 ----------
elif st.session_state.step == "products":
    event = st.session_state.event
    st.title("🛒 상품 탐색")
    st.info(
        f"{event['school']} {event['major']} · {event['event_type']} · "
        f"{event['event_date']} · {event['people']}명"
    )

    # [Task 2] 장바구니 요약 + 장바구니 화면 이동 버튼
    cart = st.session_state.cart
    st.write(f"🧺 장바구니: {len(cart)}개 품목, 총 {sum(cart.values())}개")
    if st.button("장바구니 보기 →"):
        st.session_state.step = "cart"
        st.rerun()

    # [Task 2] 상품 검색: 입력한 글자가 상품명에 들어 있는 상품만 남김
    keyword = st.text_input("🔍 상품 검색", placeholder="예: 삼겹살")
    results = [p for p in PRODUCTS if keyword.strip() in p["name"]]

    if len(results) == 0:
        st.warning("검색 결과가 없습니다.")

    # [Task 2] 상품 목록: 한 줄에 아이콘 | 상품정보 | 담기 버튼
    for p in results:
        col1, col2, col3 = st.columns([1, 4, 2])
        col1.markdown(f"## {p['icon']}")
        col2.markdown(f"**{p['name']}**  \n판매단위 {p['unit']} · {p['price']:,}원")
        col3.button("담기", key=f"add_{p['id']}", on_click=add_to_cart, args=(p["id"],))
        qty = cart.get(p["id"], 0)
        if qty > 0:
            col3.caption(f"담김 {qty}개")

    st.divider()
    if st.button("← 행사 정보 다시 입력"):
        st.session_state.step = "event"
        st.rerun()

# ---------- [Task 3] 화면 3: 장바구니 ----------
elif st.session_state.step == "cart":
    st.title("🧺 장바구니")
    cart = st.session_state.cart

    if len(cart) == 0:
        st.write("장바구니가 비어 있습니다.")
    else:
        total = 0  # 총 상품금액을 더해갈 변수

        # 반복 중에 상품을 삭제할 수 있도록 list()로 복사해서 반복
        for product_id, qty in list(cart.items()):
            p = get_product(product_id)
            col1, col2, col3 = st.columns([4, 2, 2])

            col1.markdown(f"{p['icon']} **{p['name']}**  \n{p['unit']} · {p['price']:,}원")
            new_qty = col2.number_input(
                "수량", min_value=0, value=qty, step=1, key=f"qty_{product_id}"
            )
            line_total = p["price"] * new_qty  # 상품별 금액 = 가격 × 수량
            col3.markdown(f"**{line_total:,}원**")
            total += line_total

            if new_qty == 0:
                # 수량을 0으로 만들면 장바구니에서 삭제
                del cart[product_id]
                st.rerun()
            else:
                cart[product_id] = new_qty

        st.divider()
        st.subheader(f"총 상품금액: {total:,}원")

        # ---------- [Task 4] 주문 확정 방식 선택 ----------
        st.subheader("주문 확정 방식")
        order_type = st.radio(
            "주문 방식을 선택하세요",
            ["바로 주문", "추가 혜택 가능성을 위한 주문 확정 대기"],
        )

        if order_type == "바로 주문":
            st.caption("현재 주문 내용을 그대로 확정합니다.")
        else:
            # 다른 학생회의 구체적인 주문정보는 보여주지 않고, 안내 문구만 표시
            st.info(
                "동일 대학 내 주문 수요가 있습니다. "
                "주문 확정 시점을 조정하면 추가적인 대량 주문 혜택이 적용될 수 있습니다."
            )
            st.caption("동의하면 주문이 일정 기간 '주문 대기' 상태로 보류됩니다.")

        if st.button("주문하기", type="primary"):
            # 선택한 방식에 따라 주문 상태 결정
            if order_type == "바로 주문":
                status = "주문 완료"
            else:
                status = "주문 대기"

            # 주문 정보를 하나로 묶어서 주문 목록에 추가
            event = st.session_state.event
            order = {
                "school": event["school"],
                "major": event["major"],
                "event_type": event["event_type"],
                "event_date": event["event_date"],
                "people": event["people"],
                "status": status,
                "amount": total,
                "items": dict(cart),  # 주문 시점의 장바구니를 따로 보관
            }
            st.session_state.orders.append(order)
            st.session_state.last_order = order

            # 장바구니를 비우고 주문 결과 화면으로 이동
            st.session_state.cart = {}
            st.session_state.step = "done"
            st.rerun()

    if st.button("← 상품 더 담기"):
        st.session_state.step = "products"
        st.rerun()

# ---------- [Task 4] 화면 4: 주문 결과 ----------
elif st.session_state.step == "done":
    order = st.session_state.last_order
    st.title("✅ 주문이 접수되었습니다")

    if order["status"] == "주문 완료":
        st.success("주문이 바로 확정되었습니다.")
    else:
        st.warning(
            "주문이 '주문 대기' 상태로 접수되었습니다. "
            "유통사가 동일 대학 주문을 집계한 뒤 확정 여부를 안내합니다."
        )

    st.write(f"학교/학과: {order['school']} {order['major']}")
    st.write(f"행사: {order['event_type']} · {order['event_date']} · {order['people']}명")
    st.write(f"주문 상태: **{order['status']}**")
    st.write(f"주문금액: **{order['amount']:,}원**")

    col1, col2 = st.columns(2)
    if col1.button("같은 행사로 추가 주문"):
        # 행사정보는 그대로 두고 상품 화면으로 이동
        st.session_state.step = "products"
        st.rerun()
    if col2.button("다른 학생회로 새 주문"):
        # 다른 학교·학과로 주문할 때만 행사정보를 새로 입력
        st.session_state.step = "event"
        st.rerun()