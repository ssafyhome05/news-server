## 1. 환경 설정

> 🔴 주의
> 파이썬 패키지 관리시스템 `anaconda`가 설치되어 있어야 합니다.

``` bash
git clone https://github.com/ssafyhome05/news-server.git
cd news-server
conda create -n zipchack python=3.9 -y
conda activate zipchack
pip install -r requirements.txt
uvicorn main:app --reload
```

## 2. 테스트

`http://127.0.0.1:8000/docs` 로 swagger 에 접근할 수 있습니다.
swagger 에서 getNews 메서드를 test 할 수 있습니다.


