# 크래프톤 정글 면접 대비 요약

## 1. 공통 질문 대비

### 자기소개
안녕하세요. 크래프톤 정글 SW-AI Lab 지원자 김은기입니다. 저는 연구·공공데이터 업무를 하면서 정보시스템과 데이터를 다뤘고, 단순히 도구를 사용하는 것보다 시스템이 어떻게 동작하는지 이해하고 직접 구현하는 쪽에 관심이 커졌습니다. 이번 입학시험 과제를 통해 버튼 클릭, Ajax 요청, Flask route, MongoDB 작업, JSON 응답, 화면 반영 흐름을 공부했습니다. 정글에서 기본기와 팀 기반 문제해결 방식을 훈련하고 싶습니다.

### 지원동기
정글을 선택한 이유는 특정 기술만 배우기 위해서가 아니라, 기술이 바뀌어도 문제를 정의하고 원리로 해결할 수 있는 기본기를 만들고 싶기 때문입니다. AI 프로젝트를 진행하면서 효율적 설계와 디버깅에는 자료구조, 알고리즘, C언어, 시스템 이해가 필요하다고 느꼈습니다.

### 왜 개발자가 되려는가
데이터와 시스템을 사용하는 일을 하면서 반복되는 문제를 직접 구조화하고 개선하는 일에 관심이 생겼습니다. 입학시험 과제를 하며 화면, 서버, DB, 응답이 연결되는 흐름을 이해했고, 문제를 동작하는 시스템으로 만드는 개발자가 되고 싶다고 느꼈습니다.

### 정글을 버틸 수 있는가
쉽지 않은 과정이라는 점을 알고 있습니다. 저는 막히는 지점을 넘기지 않고 원인을 나누어 확인하는 편입니다. 다만 팀 과정에서는 혼자 오래 붙잡기보다 어디까지 확인했고, 어디서 막혔고, 어떤 도움이 필요한지를 중간에 공유하겠습니다.

### 협업 경험
사회복지학부에서 먼저 듣고 맥락을 이해하는 태도의 중요성을 배웠습니다. 프로젝트를 하면서 협업에서는 듣는 것만으로는 충분하지 않고, 제가 이해한 내용과 막힌 지점도 명확히 공유해야 한다는 것을 알게 되었습니다. 팀에서는 제가 아는 부분은 공유하고, 모르는 부분은 함께 확인하면서 문제를 풀겠습니다.

### 성취 경험
배터리 RUL 프로젝트에서 급격한 열화 패턴을 기존 방식이 잘 대응하지 못한다는 문제를 발견했습니다. 물리화학적 변수를 보완하고, 초기 소량 데이터 기반 예측을 위해 메타러닝 모델을 설계했습니다. 자원 제약은 Ray Tune과 ASHA 병렬 탐색으로 줄였고, 배포 제약은 Hugging Face와 React로 해결했습니다.

### 반드시 뽑혀야 하는 이유
저는 막연한 문제를 실행 가능한 기준으로 구조화하고 끝까지 완성하는 편입니다. Study Documentation AI Agent를 만들 때 기능 구현, 할루시네이션 억제, 테스트, 배포 기준을 나누고 체크리스트로 관리했습니다. 정글에서도 이 습관을 팀 안에서 공유하며 성장하겠습니다.

## 2. 입학시험 코드 질문 대비

### 과제 설명
나홀로메모장 ver2.0을 구현했습니다. 메모 저장, 조회, 수정, 삭제, 좋아요, 좋아요순 정렬 기능이 있습니다. 전체 구조는 JavaScript 함수와 Flask route가 한 쌍으로 연결되는 방식입니다.

### 코드 부족한 점
현재 코드는 요청 성공 후 reload로 페이지 전체를 새로고침합니다. 개선한다면 showMemos()만 호출해 카드 목록 영역만 갱신하겠습니다. 또 ObjectId 검증, 사용자 권한 확인, DB 접속 정보 환경변수 분리, debug=True 제거가 필요합니다.

### 어려웠던 점
처음에는 예제와 시험 문제가 달라서 헷갈렸습니다. 예제는 URL 저장 중심이었고, 시험은 메모 CRUD와 좋아요 정렬이었습니다. 그래서 기능을 저장, 조회, 수정, 삭제, 좋아요, 정렬로 쪼개고 각 기능을 JavaScript 함수와 Flask route 한 쌍으로 정리했습니다.

### 배포에서 막힌 점
EC2에서 페이지는 떴지만 저장 시 Unauthorized가 났습니다. Ajax나 화면 문제가 아니라 MongoDB 인증 문제라고 보고 접속 문자열을 확인했습니다. EC2에서는 test:test 계정과 authSource=admin이 필요해 연결 문자열을 수정했습니다.

### 127.0.0.1 설명
127.0.0.1은 자기 자신을 뜻합니다. 제 노트북에서의 127.0.0.1은 제 노트북이고, EC2에서의 127.0.0.1은 EC2 서버 자신입니다. 그래서 로컬 Flask와 EC2 Flask는 서로 다른 서버와 DB를 볼 수 있습니다.

## 3. 손코딩 최소 대비

### 짝수만 뽑기
```python
def get_even(arr):
    result = []
    for num in arr:
        if num % 2 == 0:
            result.append(num)
    return result
```

### 짝수 개수 세기
```python
def count_even(arr):
    count = 0
    for num in arr:
        if num % 2 == 0:
            count += 1
    return count
```

### 최댓값 찾기
```python
def find_max(arr):
    max_value = arr[0]
    for num in arr:
        if num > max_value:
            max_value = num
    return max_value
```

### 문자열 뒤집기
```python
def reverse_string(s):
    result = ""
    for ch in s:
        result = ch + result
    return result
```

### 중복 제거
```python
def remove_duplicates(arr):
    result = []
    for num in arr:
        if num not in result:
            result.append(num)
    return result
```

### 괄호 검사
```python
def is_valid(s):
    stack = []
    for ch in s:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0
```
