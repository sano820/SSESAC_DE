# rhythm_game.py

import tkinter as tk
import random

# 1. 기본 윈도우 설정
master = tk.Tk()
master.title("Rhythm Game")
master.geometry("400x600+550+100")

score = 0

def flash_button(btn):
    original_color = btn.cget("bg")
    btn.config(bg = "yellow")
    master.after(100, lambda: btn.config(bg = original_color))

# 키 입력 함수
def key_pressed(event):
    key = event.char
    if key in ['1','2','3']:
        print(f"{key} pressed")

# 점수 업데이트 함수
def update_score(points):
    global score
    score += points
    score_label.config(text=f"Score : {score}")

def start_game(evet):
    if evet.keysym == "space":
        canvas.delete(text1)
        canvas.delete(text2)
        canvas.delete(text3)

master.bind("<Key>", key_pressed)
master.bind("<KeyPress-space>", start_game)

score_label = tk.Label(master, text = f"Score : {score}", font=("Arial",16))
score_label.pack(pady=10)

canvas = tk.Canvas(master, width = 300, height = 400, bg = 'black')
text1 = canvas.create_text( 150,  160, fill="white", font=("Arial", 24, "bold"), text=" 리듬 게임 ")
text2 = canvas.create_text( 150,  210, fill="gray", font=("Arial", 14), text="Press SPACE to Start")
text3 = canvas.create_text( 150,  240, fill="gray", font=("Arial", 10), text="Use 1 2 3 for Playing")
canvas.pack(pady = 20)

button_frame = tk.Frame(master)
button_frame.pack(pady=10)

button1 = tk.Button(button_frame, text = '1', width = 5, height= 1, relief = 'groove', font = 'Arial', bg = 'gray' )
button2 = tk.Button(button_frame, text = '2', width= 5, height= 1, relief = 'groove', font = 'Arial', bg = 'gray')
button3 = tk.Button(button_frame, text = '3', width= 5, height= 1, relief = 'groove', font = 'Arial', bg = 'gray')

button1.pack(side='left', padx=5)
button2.pack(side='left', padx=5)
button3.pack(side='left', padx=5)

master.mainloop()
