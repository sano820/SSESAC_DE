import tkinter as tk
import random

# --------------------
# 기본 윈도우 설정
# --------------------
master = tk.Tk()
master.title("Rhythm Game")
master.geometry("400x600+550+100")

score = 0
lives = 1
note_speed = 5
note_interval = 1000   # ms
notes = []

HIT_RANGE = 60          # 판정 범위 픽셀
judgement_y = 380       # 판정선 y좌표

# --------------------
# 점수 업데이트
# --------------------
def update_score(points):
    global score
    score += points
    score_label.config(text=f"Score : {score}")

# --------------------
# 목숨 표시 업데이트
# --------------------
def update_lives():
    life_label.config(text=f"Lives : {lives}")

# --------------------
# 게임 오버
# --------------------
def game_over():
    canvas.delete("all")
    for i in range(1,3):
        canvas.create_line(i*100, 0, i*100, 400, fill="white")
    canvas.create_line(0, judgement_y, 300, judgement_y, fill="yellow", width=2)
    canvas.create_text(150, 200, text=f"Game Over\nScore: {score}", fill="red", font=("Arial", 20, "bold"))

# --------------------
# 버튼 깜빡임
# --------------------
def flash_button(btn):
    original = btn.cget("bg")
    btn.config(bg="yellow")
    master.after(100, lambda: btn.config(bg=original))

# --------------------
# 노트 생성
# --------------------
note_job = None
move_job = None

def generate_note():
    global note_job
    col = random.randint(0, 2)
    x = 50 + col*100
    note_id = canvas.create_rectangle(x-20, 0, x+20, 30, fill="red")
    notes.append({"id": note_id, "col": col})
    note_job = master.after(note_interval, generate_note)

# --------------------
# 노트 이동
# --------------------
def move_notes():
    global move_job, lives
    for note in notes[:]:
        canvas.move(note["id"], 0, note_speed)
        coords = canvas.coords(note["id"])
        if coords[3] >= judgement_y:
            lives -= 1
            update_lives()
            canvas.delete(note["id"])
            notes.remove(note)
            if lives <= 0:
                game_over()
                return
    move_job = master.after(50, move_notes)

# --------------------
# 키 입력
# --------------------
def key_pressed(event):
    global lives
    key = event.char
    if key not in ['1','2','3']:
        return
    
    col_pressed = int(key)-1
    btn = [button1, button2, button3][col_pressed]
    flash_button(btn)

    hit = False
    for note in notes[:]:
        coords = canvas.coords(note["id"])
        note_bottom = coords[3]
        if note["col"] == col_pressed and (judgement_y - HIT_RANGE <= note_bottom <= judgement_y):
            canvas.delete(note["id"])
            notes.remove(note)
            update_score(10)
            hit = True
            break
    if not hit:
        lives -= 1
        update_lives()
        if lives <= 0:
            game_over()

# --------------------
# 게임 리셋
# --------------------
def reset_game():
    global score, lives, notes, note_job, move_job
    if note_job is not None:
        master.after_cancel(note_job)
    if move_job is not None:
        master.after_cancel(move_job)

    score = 0
    lives = 1
    update_score(0)
    update_lives()
    for note in notes:
        canvas.delete(note["id"])
    notes = []

    canvas.delete("all")
    for i in range(1,3):
        canvas.create_line(i*100, 0, i*100, 400, fill="white")
    # 판정선
    canvas.create_line(0, judgement_y, 300, judgement_y, fill="yellow", width=2)
    # 판정 범위 위쪽 시각화
    canvas.create_line(0, judgement_y - HIT_RANGE, 300, judgement_y - HIT_RANGE, fill="orange", width=1, dash=(4,2))

    generate_note()
    move_notes()

# --------------------
# GUI 세팅
# --------------------
score_label = tk.Label(master, text=f"Score : {score}", font=("Arial",16))
score_label.pack(pady=5)

life_label = tk.Label(master, text=f"Lives : {lives}", font=("Arial",16))
life_label.pack(pady=5)

canvas = tk.Canvas(master, width=300, height=400, bg='black')
canvas.pack(pady=20)

# 3열 구분선
for i in range(1,3):
    canvas.create_line(i*100, 0, i*100, 400, fill="white")
# 판정선
canvas.create_line(0, judgement_y, 300, judgement_y, fill="yellow", width=2)
# 판정 범위 위쪽 표시
canvas.create_line(0, judgement_y - HIT_RANGE, 300, judgement_y - HIT_RANGE, fill="orange", width=1, dash=(4,2))

# 버튼 프레임
button_frame = tk.Frame(master)
button_frame.pack(pady=10)
button1 = tk.Button(button_frame, text='1', width=5, height=1, bg='gray')
button2 = tk.Button(button_frame, text='2', width=5, height=1, bg='gray')
button3 = tk.Button(button_frame, text='3', width=5, height=1, bg='gray')
button1.pack(side='left', padx=5)
button2.pack(side='left', padx=5)
button3.pack(side='left', padx=5)

# Reset 버튼
reset_btn = tk.Button(master, text="RESET", width=12, height=10, bg="#4CAF50", fg="white",
                      font=("Arial", 12,"bold"), relief="raised", bd=4, command=reset_game)
reset_btn.pack(pady=10)

def on_enter(e):
    reset_btn['bg'] = "#45a049"
def on_leave(e):
    reset_btn['bg'] = "#4CAF50"

reset_btn.bind("<Enter>", on_enter)
reset_btn.bind("<Leave>", on_leave)

# --------------------
# 키 입력 바인딩 & 게임 시작
# --------------------
master.bind("<Key>", key_pressed)
generate_note()
move_notes()

master.mainloop()

