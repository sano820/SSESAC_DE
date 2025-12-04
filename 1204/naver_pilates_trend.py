# naver_pilates_trend.py

import os
import json
from datetime import datetime, timedelta

import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 1) 네이버 개발자센터 값 넣기
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

print("CLIENT_ID prefix:", (CLIENT_ID or "")[:5])  # 앞 5글자만 확인용
print("CLIENT_SECRET 존재 여부:", CLIENT_SECRET is not None)

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET이 .env에 설정되지 않았습니다.")


def get_search_trend(keywords: dict,
                     start_date: str,
                     end_date: str,
                     time_unit: str = "week") -> dict:
    """
    네이버 데이터랩 검색어 트렌드 API 호출 함수

    keywords 예시:
        {"필라테스": ["필라테스"], "요가": ["요가"]}
    start_date, end_date:
        "YYYY-MM-DD" 문자열
    time_unit:
        "date" | "week" | "month"
    """
    url = "https://openapi.naver.com/v1/datalab/search"

    keyword_groups = [
        {"groupName": group_name, "keywords": kw_list}
        for group_name, kw_list in keywords.items()
    ]

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups,
        # 필요하면 필터 추가 가능
        # "device": "pc" or "mo"
        # "gender": "m" or "f"
        # "ages": ["3", "4"]  # 20대, 30대 이런 식
    }

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(body),
        timeout=5
    )
    # 🔍 디버깅용 출력 추가
    print("status_code:", response.status_code)
    print("response text:", response.text)

    response.raise_for_status()
    return response.json()


def trend_to_dataframe(trend_json: dict) -> pd.DataFrame:
    """
    데이터랩 응답 JSON -> 분석용 DataFrame으로 변환
    컬럼: [group, date, ratio]
    """
    rows = []
    for result in trend_json["results"]:
        group_name = result["title"]
        for point in result["data"]:
            rows.append(
                {
                    "group": group_name,
                    "date": point["period"],        # "YYYY-MM-DD"
                    "ratio": float(point["ratio"]), # 0~100 상대값
                }
            )

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def main():
    # 오늘 기준 최근 1년
    end = datetime.today().date()
    start = end - timedelta(days=365)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    print(f"조회 기간: {start_str} ~ {end_str}")

    # 1) 필라테스 키워드로 트렌드 조회
    trend_json = get_search_trend(
        keywords={"필라테스": ["필라테스"]},
        start_date=start_str,
        end_date=end_str,
        time_unit="week",  # 주간 단위
    )

    # 2) DataFrame으로 변환
    df = trend_to_dataframe(trend_json)
    print(df.head())

    # 3) CSV로 저장 (원하면 엑셀에서 확인)
    df.to_csv("naver_search_trend_pilates.csv",
              index=False,
              encoding="utf-8-sig")
    print("CSV 저장 완료: naver_search_trend_pilates.csv")

    # 4) 간단 그래프
    plt.figure(figsize=(10, 4))
    plt.plot(df["date"], df["ratio"])
    plt.title("네이버 검색어 트렌드 - 필라테스 (주간)")
    plt.xlabel("날짜")
    plt.ylabel("검색량(상대값)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
