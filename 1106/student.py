'''
`student.py` 파일 생성 후, 학생 정보 관리 모듈을 정의하세요.
- students: 학생 정보를 보관하는 리스트


- add_student(name, age, grade): 학생 정보를 추가
- get_all_students(): 모든 학생 정보를 출력
- find_student(name): 이름으로 학생을 검색 후, 학생 정보 딕셔너리 반환
- get_average_age(): 학생들의 평균 나이를 계산후, 반환

학생 정보는 딕셔너리 형태로 정의합니다. (이름, 나이, 성적)
'''
# 학생 정보 리스트를 정의하세요.
students = []

# 함수들을 정의하세요.
def add_student(name, age, grade):
    student = {}
    student['name'] = name
    student['age'] = age
    student['grade'] = grade
    students.append(student)

def get_all_students():
    print("=== 전체 학생 목록 ===")
    for i in range(len(students)):
        print(students[i])
    print("\n")

def find_student(name):
    print(f"학생 검색: {name}")
    for i in range(len(students)):
        if name in students[i]['name']:
            print(f"{students[i]['name']}")
            break
        else: 
            continue
    print("\n")

def get_average_age():
    answer = 0
    for i in range(len(students)):
        answer += students[i]['age']
    return answer / len(students)
