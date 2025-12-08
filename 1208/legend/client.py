from module import * 
from matplotlib import pyplot as plt 
import numpy as np 

# -------------------
# 4) 메뉴 실행 함수
# -------------------
def run_program():
    while(True) : 
        print("실행할 작업을 선택하세요:")
        print("1. AND 게이트 출력")
        print("2. 선형 그래프 그리기")
        print("3. sigmoid 그래프 그리기")
        print("4. relu 그래프 그리기")
        print("5. keras 모델 요약 보기")
        print("6. 종료")
    
        choice = int(input("번호 입력: "))
    
        # 1. AND 게이트 테스트
        if choice == 1:
            print(AND(0,0))
            print(AND(1,0))
            print(AND(2,2))  # 2,2는 AND 논리 정의상 1이 아님 → 0 출력
    
        # 2. 선형 함수 그래프
        elif choice == 2:
            draw_line()
    
        # 3. sigmoid 그래프
        elif choice == 3:
            draw_sigmoid()
    
        # 4. relu 그래프
        elif choice == 4:
            draw_relu()
    
        # 5. Keras 모델 실행
        elif choice == 5:
            keras_exam()
    
        elif choice == 6:
            break

# 프로그램 실행
run_program()