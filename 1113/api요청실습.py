import requests

# base_url = "https://restcountries.com/v3.1"
# path = '/all'
# url = base_url + path

# params = {
#     "fields":"name,population,area"
# }

# response = requests.get(url=url,params=params)
# https://restcountries.com/v3.1/all?fields=name,poulation,area

# if response.status_code == 200:  # 요청에 성공했을 때
#     data = response.json()       # 응답 바디를 딕셔너리 형태로 변환
#     print(data)                  # 딕셔너리를 원소로 갖는 리스트
#     for country in data:
#         name = country['name']['common']
#         population = country['population']
#         area = country['area']
#         print(f"이름: {name}, 인구수: {population}, 면적: {area}")
# else:  # 요청에 실패했을때(응답 상태 코드가 4xx or 5xx)
#     print(response.text)



# # ------------------------
# path2 = '/alpha'
# url2 = base_url + path2
# params2 = {
#     "codes":"kr,jp,cn",
#     "fields":"name,population,area"
# }

# response2 = requests.get(url=url2, params=params2)
# # https://restcountries.com/v3.1/all?codes=kr,jp,cn&fields=name,poulation,area

# if response2.status_code == 200:
#     data2 = response2.json()
#     print(data2)
#     for d in data2:
#         name = d['name']['common']
#         nativename = d['name']['nativeName']
#         native_common = list(nativename.values())[0]['common']
#         area = d['area']
#         population = d['population']
#         print(f"{name} {native_common} {population} {area}")
# else:
#     print(response2.text)


# 333------

import requests
'''
다양한 path, 다양한 query parameter
응답 body의 결과도 확인 --> 데이터 추출
'''

base_url = "https://restcountries.com/v3.1"
path = "/all"
path2 = "/alpha"

url3 = base_url + path2

params3 = {
    "codes" : "KOR,JPN,CHN,USA,GBR,FRA,DEU"
    # "fieds" : "name,population"
}

response3 = requests.get(url=url3, params=params3)
# https://restcountries.com/v3.1/all?fields=name,population
if response3.status_code == 200: # 요청에 성공했을 때
    data3 = response3.json() # 응답 바디를 딕셔너리로 형태로 변환
    # print(data) # 딕셔너리를 원소로 갖는 리스트
    for country in data3:
        print("=" * 20)
        capital = country.get('capital','N/A')[0]
        continents = country.get('continents', 'N/A')[0]
        img_url = country.get('flags', {}).get('png',"N/A")
        google_map = country.get('maps', {}).get('googleMaps', "N/A")
        name = country.get('name', {}).get('common','N/A')
        population = country.get('population', "N/A")
        languages = country.get('languages', "N/A")

        print(f"나라 이름: {name}, 수도: {capital}, 대륙: {continents}")
        print(f"인구수: {population}, 언어: {languages}")
        print(f"국기 사진: {img_url}, 구글 지도: {google_map}")
else: # 요청에 실패했을 때 (응답 상태 코드가 4xx or 5xx)
    print(response3.text)