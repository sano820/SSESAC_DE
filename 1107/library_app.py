import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

# ==========================
# 📚 데이터 클래스 정의
# ==========================

class Book:
    def __init__(self, title, author, isbn, stock, borrow_count=0):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.stock = stock
        self.borrow_count = borrow_count

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "stock": self.stock,
            "borrow_count": self.borrow_count,
        }


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_dict(self):
        return {"name": self.name, "member_id": self.member_id}


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.records = []

    # ---------- 책 관리 ----------
    def add_book(self, book):
        self.books.append(book)

    def get_book(self, title):
        for b in self.books:
            if b.title == title:
                return b
        return None

    def search_books(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]

    # ---------- 회원 관리 ----------
    def add_member(self, member):
        if any(m.member_id == member.member_id for m in self.members):
            return False
        self.members.append(member)
        return True

    def get_member(self, member_id):
        for m in self.members:
            if m.member_id == member_id:
                return m
        return None

    # ---------- 대여/반납 ----------
    def borrow_book(self, title, member_id):
        book = self.get_book(title)
        member = self.get_member(member_id)
        if not book:
            return f"❌ '{title}'은(는) 존재하지 않습니다."
        if not member:
            return f"❌ 회원 ID '{member_id}'를 찾을 수 없습니다."
        if book.stock <= 0:
            return f"⚠️ '{title}'은(는) 재고가 없습니다."

        book.stock -= 1
        book.borrow_count += 1
        record = {
            "title": title,
            "member_id": member_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.records.append(record)
        return f"✅ '{title}' 대여 완료!"

    def return_book(self, title, member_id):
        book = self.get_book(title)
        if not book:
            return f"❌ '{title}'은(는) 존재하지 않습니다."
        book.stock += 1
        return f"📚 '{title}' 반납 완료!"

    # ---------- 통계 ----------
    def total_borrows(self):
        return sum(b.borrow_count for b in self.books)

    def most_borrowed(self):
        return max(self.books, key=lambda b: b.borrow_count, default=None)

    def overdue_records(self):
        overdue_list = []
        for r in self.records:
            date = datetime.strptime(r["date"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - date > timedelta(days=7):
                overdue_list.append(r)
        return overdue_list

    # ---------- 파일 입출력 ----------
    def save_to_file(self, path):
        data = {
            "books": [b.to_dict() for b in self.books],
            "members": [m.to_dict() for m in self.members],
            "records": self.records,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**b) for b in data.get("books", [])]
            self.members = [Member(**m) for m in data.get("members", [])]
            self.records = data.get("records", [])
        except FileNotFoundError:
            st.warning("📁 저장된 파일이 없어 기본 데이터를 불러옵니다.")
            self.load_default_data()

    def load_default_data(self):
        self.books = [
            Book("파이썬 완전정복", "김코딩", "9781234567890", 3),
            Book("데이터 과학 입문", "이데이터", "9781234567891", 2),
            Book("웹 개발의 모든 것", "박웹개", "9781234567892", 5),
            Book("AI 프로그래밍", "최인공", "9781234567893", 1),
            Book("알고리즘 기초", "정알고", "9781234567894", 4),
        ]
        self.members = [
            Member("홍길동", "user01"),
            Member("김데이터", "user02"),
        ]


# ==========================
# 🌐 Streamlit UI 구성
# ==========================

st.set_page_config(page_title="📚 도서 관리 시스템", layout="wide")
st.title("📚 도서 관리 시스템 (Streamlit 완성판)")

data_path = Path("library_data.json")
lib = Library()
lib.load_from_file(data_path)

tabs = st.tabs([
    "📖 도서 목록",
    "🙋 회원 관리",
    "📦 대여 / 반납",
    "🕓 대여 기록",
    "📊 통계 / 연체",
    "💾 파일 관리"
])

# ---------------------------
# 📖 탭 1: 도서 목록
# ---------------------------
with tabs[0]:
    st.subheader("📚 도서 목록 보기 및 검색")
    keyword = st.text_input("검색 (제목 또는 저자)")
    if keyword:
        filtered = lib.search_books(keyword)
        st.dataframe([b.to_dict() for b in filtered], use_container_width=True)
    else:
        st.dataframe([b.to_dict() for b in lib.books], use_container_width=True)

    st.markdown("---")
    with st.expander("➕ 새 도서 추가하기"):
        with st.form("add_book_form"):
            title = st.text_input("책 제목")
            author = st.text_input("저자")
            isbn = st.text_input("ISBN")
            stock = st.number_input("재고 수량", min_value=1, step=1)
            submit = st.form_submit_button("도서 추가")
            if submit and title:
                lib.add_book(Book(title, author, isbn, stock))
                st.success(f"'{title}' 추가 완료!")
                lib.save_to_file(data_path)

# ---------------------------
# 🙋 탭 2: 회원 관리
# ---------------------------
with tabs[1]:
    st.subheader("🙋 회원 목록 및 등록")
    st.dataframe([m.to_dict() for m in lib.members], use_container_width=True)

    st.markdown("---")
    with st.form("add_member_form"):
        name = st.text_input("이름")
        member_id = st.text_input("회원 ID")
        submit = st.form_submit_button("회원 등록")
        if submit:
            if lib.add_member(Member(name, member_id)):
                st.success(f"'{name}' 회원 등록 완료!")
                lib.save_to_file(data_path)
            else:
                st.warning("⚠️ 이미 존재하는 회원 ID입니다.")

# ---------------------------
# 📦 탭 3: 대여 / 반납
# ---------------------------
with tabs[2]:
    st.subheader("📦 도서 대여 및 반납")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📘 대여하기")
        member_id = st.text_input("회원 ID")
        title = st.text_input("책 제목 (대여)")
        if st.button("대여 실행"):
            msg = lib.borrow_book(title, member_id)
            st.success(msg) if "✅" in msg else st.warning(msg)
            lib.save_to_file(data_path)

    with col2:
        st.write("### 📗 반납하기")
        member_id_r = st.text_input("회원 ID (반납)")
        title_r = st.text_input("책 제목 (반납)")
        if st.button("반납 실행"):
            msg = lib.return_book(title_r, member_id_r)
            st.info(msg)
            lib.save_to_file(data_path)

# ---------------------------
# 🕓 탭 4: 대여 기록
# ---------------------------
with tabs[3]:
    st.subheader("🕓 전체 대여 기록")
    if lib.records:
        st.dataframe(lib.records, use_container_width=True)
    else:
        st.info("아직 대여 기록이 없습니다.")

# ---------------------------
# 📊 탭 5: 통계 / 연체
# ---------------------------
with tabs[4]:
    st.subheader("📊 대여 통계")
    st.metric("총 대여 횟수", lib.total_borrows())
    most = lib.most_borrowed()
    if most:
        st.metric("가장 많이 대여된 책", most.title)
    else:
        st.write("데이터가 없습니다.")

    st.markdown("---")
    st.subheader("⏰ 연체된 도서 목록 (7일 초과)")
    overdue = lib.overdue_records()
    if overdue:
        st.dataframe(overdue, use_container_width=True)
    else:
        st.success("모든 대여가 정상 기간 내에 있습니다.")

# ---------------------------
# 💾 탭 6: 파일 관리
# ---------------------------
with tabs[5]:
    st.subheader("💾 파일 저장 및 불러오기")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 저장"):
            lib.save_to_file(data_path)
            st.success("저장 완료!")
    with c2:
        if st.button("📂 불러오기"):
            lib.load_from_file(data_path)
            st.success("불러오기 완료!")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit - Final Version by ChatGPT")
