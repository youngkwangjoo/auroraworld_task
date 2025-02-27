# 🔗 웹 링크 관리 시스템

## 📌 개요  
이 프로젝트는 사용자가 자신의 웹 링크를 등록, 수정, 삭제, 공유할 수 있는 웹 애플리케이션입니다.  
사용자는 로그인 후 웹 링크를 관리할 수 있으며, 보안 강화를 위해 Argon2 암호화 및 JWT 기반 인증을 적용하였습니다.

---

## ⚙️ 기술 스택

- **언어**: Python, JavaScript
- **프레임워크**: Django
- **라이브러리**
  - `asgiref==3.8.1`
  - `Django==5.1.6`
  - `djangorestframework==3.15.2`
  - `PyJWT==2.10.1`
  - `sqlparse==0.5.3`
  - `argon2-cffi`
- **프론트엔드**: HTML, CSS, JavaScript

---

## 🎯 주요 기능  

### 🔹 1. 회원가입 및 로그인
- **아이디 중복 검사**: 이미 사용 중인 아이디인지 확인 후 회원가입 가능  
  ![아이디 중복 검사](https://github.com/user-attachments/assets/e15d2330-5918-4283-b6ca-a1cd836ceefd)
  
- **비밀번호 정책 강화**:
  - `argon2` 알고리즘을 사용하여 비밀번호를 안전하게 저장  
  - 최소 12자 이상의 비밀번호 요구  
  ![비밀번호 제한 규칙](https://github.com/user-attachments/assets/d1342402-2891-4963-9428-e19d8c3a95ea)
  
- **회원가입 완료 후 로그인 가능**
  ![로그인, 로그아웃](https://github.com/user-attachments/assets/07e8b7f4-0dbd-47e6-a95b-d09052657b4a)

---

### 🔹 2. 웹 링크 관리
웹 링크는 다음과 같은 필수 속성을 가집니다:
- `id` : 고유한 식별자
- `created_by` : 생성한 사용자 아이디
- `name` : 웹 링크 이름
- `url` : 저장할 웹 사이트의 URL
- `category` : 카테고리 (예: 개인 즐겨 찾기, 업무 활용 자료 등)

#### ✅ 웹 링크 등록
사용자는 새로운 웹 링크를 추가할 수 있습니다.  
![웹 링크 등록](https://github.com/user-attachments/assets/6a303b07-aadc-423c-9b1a-8957654922ee)

#### ✅ 웹 링크 수정
사용자는 자신이 등록했거나 **쓰기 권한이 있는 웹 링크**를 수정할 수 있습니다.  
![웹 링크 수정](https://github.com/user-attachments/assets/44264694-e440-460d-9156-aed4934cbd0f)

#### ✅ 웹 링크 삭제
사용자는 **본인이 등록한 웹 링크**를 삭제할 수 있습니다.  
![웹 링크 삭제](https://github.com/user-attachments/assets/35eda35f-396b-437f-a104-9105196d1052)

---

### 🔹 3. 웹 링크 공유
- 사용자는 자신의 웹 링크를 특정 사용자와 공유할 수 있습니다.  
- 공유 시 **읽기 / 쓰기 권한**을 설정할 수 있습니다.  
![웹 링크 공유](https://github.com/user-attachments/assets/173a2975-1417-46ec-88ca-d71c184836b7)

---

### 🔹 4. 검색 및 필터링
- **이름 또는 카테고리**로 검색 가능  
- **부분 일치(like 검색)**를 지원  
- **검색 대상**:
  - 내 웹 링크 목록에서 검색
  - 공유 대상 사용자 검색  
![검색 기능](https://github.com/user-attachments/assets/e8e29d3c-39b4-4e0d-8c7a-1d793a0e377f)

---

## 🔒 보안 요구사항
1. **로그인하지 않은 사용자는 웹 링크 관련 API를 사용할 수 없음**  
2. **JWT 인증이 필요한 API 요청은 반드시 인가(Authorization) 처리**  
   - `@jwt_required` 데코레이터를 적용하여 로그인하지 않은 사용자는 접근 불가  
   - 인증되지 않은 사용자가 API 요청 시 다음과 같은 에러 메시지 반환  
   ![인증 에러](https://github.com/user-attachments/assets/c5643f16-8a17-4014-8fe6-910472a9b81a)

---

## 🛠️ 설치 및 실행 방법

### 1️⃣ 가상환경 설정 및 패키지 설치
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
