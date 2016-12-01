# 파이썬으로 OCR 구현하기 프로젝트  
## 모든 함수는 PIL과 numpy 라이브러리가 설치된 환경을 필요로 합니다.  
- from PIL import Image    
- import numpy as np  

- [x] 정사각 사이즈의 알파뱃 이미지의 URL을 입력받아, RGB값을 가진 numpy array로 변환해 numpy array를 리턴해주는 함수  
- [x] RGB 3값을 튜플로 가지고있는 numpy array를 커스터마이징한 값에 따라 흑백 농도값만 갖는 gray scale numpy array를 리턴해주는 함수  
- [x] 정사각 사이즈의 알파뱃 이미지의 URL을 입력받아 numpy array로 바꾼후 5가지 알파뱃 데이터 생성 함수를 실행하고, 그 값을 이미지 내의 글자 픽셀수로 나눈 값을 리턴해주는 함수  
- [x] 정사각 사이즈의 A-Z까지 알파뱃 이미지의 URL List를 만들어주는 함수와, URL List를 입력받아 각 알파뱃 별로 5가지 데이터 생성 함수를 실행한 후, collection 라이브러리와, pandas 라이브러리를 통해, 자동으로 데이터를 테이블화하여 엑셀파일로 만들어주는 함수 작성   


