import tkinter as tk
from tkinter import messagebox
import ollama
import json
import re
import ast

# ---------- 함수 정의 ---------- #

def generate_quiz():
    topic = entry_topic.get()
    if not topic:
        messagebox.showwarning("입력 오류", "퀴즈 주제를 입력하세요.")
        return

    label_status.config(text="문제 생성 중... 잠시만 기다리세요.")
    root.update_idletasks()

    prompt = f"""
    '{topic}' Make 5 Quizs of Topic to JSON Format.
    
    format:
    [
      {{
        "question": "Question",
        "options": ["option1", "option2", "option3", "option4"],
        "answer": 0
      }}
    ]

    example:
    [
        {{
            "question": "What is the capital city of South Korea?",
            "options": ["Seoul","Busan","Daegu","Inchean"],
            "answer": 1
        }}
    ]
    Make sure you only print out JSON arrays and never include other sentences.
    Also you must to make 4 options of each question.
    """

    text = ""
    try:
        res = ollama.chat(model="llama3.2:1b", messages=[
            {"role": "user", "content": prompt}
        ])
        text = res["message"]["content"].strip()

        # JSON 배열만 추출
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            raise ValueError("JSON 형식을 찾을 수 없음")

        json_text = match.group(0)

        # ✅ 비정상 JSON을 파이썬 표현식으로 정제
        try:
            quiz_data_raw = json.loads(json_text)
        except json.JSONDecodeError:
            # 불완전한 JSON → 파이썬 dict 형식으로 변환 시도
            quiz_data_raw = ast.literal_eval
            (json_text.replace("true", "True").replace("false", "False"))

        global quiz_data
        quiz_data = quiz_data_raw

        label_status.config(text="")
        start_quiz()

    except Exception as e:
        label_status.config(text="")
        messagebox.showerror("오류", f"퀴즈 생성 실패: {e}\n\n응답 내용:\n{text[:300] if text else '응답 없음'}")


def start_quiz():
    """첫 번째 문제로 이동"""
    global current_q, score
    current_q = 0
    score = 0
    show_question()


def show_question():
    """현재 문제를 표시"""
    for widget in frame_main.winfo_children():
        widget.destroy()

    if current_q < len(quiz_data):
        q = quiz_data[current_q]
        label_qnum = tk.Label(frame_main, text=f"문제 {current_q+1}/{len(quiz_data)}", font=("Arial", 12))
        label_qnum.pack(pady=5)

        label_question = tk.Label(frame_main, text=q["question"], font=("Arial", 14), wraplength=450)
        label_question.pack(pady=10)

        global selected_option
        selected_option = tk.IntVar(value=-1)

        for i, opt in enumerate(q["options"]):
            tk.Radiobutton(frame_main, text=opt, variable=selected_option, value=i).pack(anchor="w", padx=30)

        btn_submit = tk.Button(frame_main, text="제출", command=check_answer)
        btn_submit.pack(pady=15)
    else:
        show_result()


def check_answer():
    """사용자 선택 확인 후 다음 문제로 이동"""
    global current_q, score

    choice = selected_option.get()
    if choice == -1:
        messagebox.showinfo("선택 필요", "보기를 선택하세요.")
        return

    correct = quiz_data[current_q]["answer"]
    if choice == correct:
        score += 1

    current_q += 1
    show_question()


def show_result():
    """결과창 표시"""
    for widget in frame_main.winfo_children():
        widget.destroy()

    tk.Label(frame_main, text="결과", font=("Arial", 18)).pack(pady=20)
    tk.Label(frame_main, text=f"점수: {score}/{len(quiz_data)}", font=("Arial", 14)).pack(pady=10)

    tk.Button(frame_main, text="다시하기", command=reset_app).pack(pady=10)
    tk.Button(frame_main, text="종료", command=root.quit).pack(pady=10)


def reset_app():
    """앱 초기화"""
    for widget in frame_main.winfo_children():
        widget.destroy()

    label_intro = tk.Label(frame_main, text="AI 퀴즈 생성기 (Llama3.2:1b)", font=("Arial", 16))
    label_intro.pack(pady=15)

    global entry_topic
    entry_topic = tk.Entry(frame_main, width=40)
    entry_topic.pack(pady=5)

    tk.Button(frame_main, text="문제 생성", command=generate_quiz).pack(pady=10)

    global label_status
    label_status = tk.Label(frame_main, text="", fg="gray")
    label_status.pack()


# ---------- GUI 초기화 ---------- #
root = tk.Tk()
root.title("AI Quiz Generator - Llama3.2:1b")
root.geometry("500x400")

frame_main = tk.Frame(root)
frame_main.pack(expand=True)

quiz_data = []
current_q = 0
score = 0

# 초기 화면 호출
reset_app()

root.mainloop()

