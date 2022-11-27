# lottesupper
## 데이터베이스 프로젝트

#### 기능
- 로그인 (회원 id로만)
- 상품목록 db에서 가져오기
- 상품목록에서 상품 주문하기 (db에 주문 저장)
- 주문목록 db에서 가져오기
- 상품발주로 재고 채우기 (db 상품 재고 update)
- 페이지 간 이동하기

#### 설치
langauge : python
```
pip install pyqt5
pip install pyqt5-tools
```

#### 시작
페이지 시작은 login.py 부터 시작. ( 각 파일 실행 가능)

페이지 순환
>login -> main <-> supply, \
>         main <-> orderedProduct
