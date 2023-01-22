# 도둑 포커

### 프로그램 실행

#### 개발자 버전 (컴퓨터에 git이 설치되어 있는 경우)
1. 컴퓨터 아무 곳에나 빈 폴더를 만든다.
2. cmd창이나 powershell에서 cd 명령어로 그 폴더까지 이동한다.
3. 다음 명령어로 레포지토리를 로컬로 갖고 간다.
```powershell
git clone https://github.com/jbs30lcy/Thief-Poker
```
4. 필요한 모듈을 설치한다.
```powershell
pip install pygame
pip install --upgrade oauth2client
pip install gspread
```
5. main.py 프로그램을 실행한다.
6. 개발 환경을 구축하기 위해, 다음 명령어를 폴더 내에서 입력해준다. (확실하진 않음 ㅋㅋㄹ)
```powershell
git init
git branch --set-upstream-to=origin/master HEAD
```


#### 비개발자 버전 (git이 설치되어 있지 않은 경우)
1. <> Code 라고 쓰인 초록색 버튼을 누른다.
2. Download ZIP을 누른다.
3. 압축을 풀고, 개발자 버전의 4~5번을 실행하면 된다.
---
git pull 명령어로, 이 짓을 반복하지 않고 최신 버전을 가져올 수 있다.
업데이트가 굉장히 자주 이루어지고 있으니 git을 사용하면 편할 것.


그리고 혹시 실행 중 버그가 있다면, 갠톡이나 github 가로줄 메뉴의 Issues에 제보해 주시면 감사하겠습니다.
