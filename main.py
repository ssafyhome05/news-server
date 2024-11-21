# main.py
import requests
from fastapi import FastAPI
from fastapi import Depends
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


# database

#custom
from database import engineconn
from models import News

# SQLAlchemy Setup
engine = engineconn()

def get_db():
    db = engine.sessionmaker()
    try:
        yield db
    finally:
        db.close()


# database dto 
class NewsAdd(BaseModel):
    dong_code   : str
    title       : str
    url         : str
    city_name   : str
    ref         : str
    img         : str






# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Zip-chack",  # 문서 제목 수정
    description="# Zip-chack service APIs \n\n"
        		+ "## 마음에 드는 집에 착! 집착 서비스 api sample 입니다. \n\n"
        		+ "### 제공 API : \n\n"
        		+ "1. __News__ 뉴스기사 크롤링 서비스 \n\n",
        		
    version="1.0.0"  # API 버전 수정
)


# 응답 모델 정의
class NewsItem(BaseModel):
    dong_code: str = Field(..., description="행정동 코드")
    title: str = Field(..., description="뉴스 제목")
    url: str = Field(..., description="뉴스 기사 URL")
    city_name: str = Field(..., description="도시/구 이름")
    ref: str = Field(..., description="출처")
    img: str = Field(..., description="관련사진")

class NewsResponse(BaseModel):
    news: list[NewsItem]

    class Config:
        json_schema_extra = {
            "example": {
                "news": [
                    {
                        "dong_code": "4159000000",
                        "title": "LH, 동탄2 ‘종합병원 건립 패키지형 개발사업’ 사업자공모 추진",
                        "url": "https://n.news.naver.com/article/119/0002894004",
                        "city_name": "화성시",
                        "ref": "데일리안",
                        "img":"https://imgnews.pstatic.net/image/009/2024/11/18/0005398589_001_20241118170815139.jpg?type=w860"
                    },
                    {
                        "dong_code": "1165000000",
                        "title": "서초구 \"미청산 재건축조합 이렇게 관리하세요\"",
                        "url": "https://n.news.naver.com/article/014/0005269235",
                        "city_name": "서초구",
                        "ref": "파이낸셜뉴스",
                        "img":"https://imgnews.pstatic.net/image/009/2024/11/18/0005398589_001_20241118170815139.jpg?type=w860"
                    },
                ]
            }
        }


# Create a new user
@app.post("/addNewsList", tags=["News"])
async def addNewsList(db = Depends(get_db)):
    
    search = "https://land.naver.com/news/region.naver?city_no=1100000000&dvsn_no="
    response = requests.get(search)
    soup = BeautifulSoup(response.text, "html.parser")
    dong_codes = soup.select(".area") # 결과는 리스트

    links = soup.select(".category_list li a:nth-of-type(2)") 
    news_list = []

    idx = 0
    for link, code in zip(links, dong_codes):
        city_name = code.text[1:-1]
        dong_code = code.attrs['href'].split("dvsn_no")[1][1:]
        url = link.attrs['href']

        title_soup = BeautifulSoup(requests.get(url).text, "html.parser")
        title = title_soup.select('#title_area span')[0].text
        ref = title_soup.select('.ofhd_float_title_text_press')[0].text
        if title_soup.select('#img1')==[]: # 이미지 없는 경우 건너뛰기
            idx+=1
            continue;    
        img = title_soup.select('#img1')[0].attrs['data-src']

        news_list.append(
            News(
                dong_code = dong_code,
                title = title,
                ref   = ref,
                url = url,
                city_name = city_name,
                img = img
            )
        )
        
        if idx==3: break
        idx+=1

    db.add_all(news_list)
    db.commit()
    return 







# 기본 경로에 대한 get 요청 처리
@app.get("/news", tags=["News"], response_model=NewsResponse)
def getNewsList():
    search = "https://land.naver.com/news/region.naver?city_no=1100000000&dvsn_no="
    response = requests.get(search)
    soup = BeautifulSoup(response.text, "html.parser")
    dong_codes = soup.select(".area") # 결과는 리스트

    links = soup.select(".category_list li a:nth-of-type(2)") 
    response = {"news":[]}

    idx = 0
    for link, code in zip(links, dong_codes):
        city_name = code.text[1:-1]
        dong_code = code.attrs['href'].split("dvsn_no")[1][1:]
        url = link.attrs['href']

        title_soup = BeautifulSoup(requests.get(url).text, "html.parser")
        title = title_soup.select('#title_area span')[0].text
        ref = title_soup.select('.ofhd_float_title_text_press')[0].text
        img = title_soup.select('#img1')[0].attrs['data-src']

        data = {"dong_code":dong_code, "title":title,"url":url,"city_name":city_name, "ref":ref, "img":img}
        response["news"].append(data)
        
        news = News(name=title, email=url)
        db.add(news)
        
        
        
        
        if idx==3: break
        idx+=1


    return response


# # POST 요청 예시: 데이터를 받아서 응답하는 엔드포인트
# @app.post("/items/")
# def create_item(item: dict):
#     return {"message": "Item created", "data": item}