import streamlit as st

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


def get_product(product_id):
    """상품 id로 상품 정보를 찾아서 돌려줌"""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p


def add_to_cart(product_id):
    """[담기] 버튼을 누르면 실행: 해당 상품 수량을 1 늘림"""
    cart = st.session_state.cart
    cart[product_id] = cart.get(product_id, 0) + 1


# 지금 어떤 화면을 보여줄지 기억하는 변수 (처음엔 행사정보 입력 화면)
if "step" not in st.session_state:
    st.session_state.step = "event"

# [Task 2] 장바구니: {상품id: 수량} 형태로 저장
if "cart" not in st.session_state:
    st.session_state.cart = {}

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

    if st.button("← 상품 더 담기"):
        st.session_state.step = "products"
        st.rerun()