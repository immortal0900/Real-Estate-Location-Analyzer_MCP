# 프로젝트 구조

```
real_estate_location_mcp/
│
├── app.py                          # Hugging Face Spaces 메인 진입점
├── test_tool.py                    # 테스트 스크립트
├── requirements.txt                # Python 의존성
├── .env.example                    # 환경 변수 예시
├── .gitignore                      # Git 제외 파일
├── LICENSE                         # MIT 라이선스
├── README.md                       # 프로젝트 설명
├── QUICKSTART.md                   # 빠른 시작 가이드
├── PROJECT_STRUCTURE.md            # 이 파일
│
├── src/                            # 소스 코드
│   ├── __init__.py
│   ├── mcp_server.py              # FastMCP 서버
│   ├── gradio_app.py              # Gradio 웹 애플리케이션
│   │
│   └── tools/                      # 도구 모듈
│       ├── __init__.py
│       └── kakao_tool.py          # 카카오 API 도구
│
└── docs/                           # 문서
    ├── MCP_SETUP.md               # MCP 서버 설정 가이드
    └── GRADIO_DEPLOYMENT.md       # Gradio 배포 가이드
```

## 파일 설명

### 루트 디렉토리

#### `app.py`
- Hugging Face Spaces에서 실행되는 메인 파일
- `src/gradio_app.py`의 인터페이스를 import하여 실행

#### `test_tool.py`
- 카카오 API 연동 테스트 스크립트
- 로컬 환경에서 API 키가 제대로 작동하는지 확인

#### `requirements.txt`
- 프로젝트 의존성 목록
- `pip install -r requirements.txt`로 설치

#### `.env.example`
- 환경 변수 템플릿
- 복사하여 `.env` 파일 생성 후 API 키 입력

#### `.gitignore`
- Git에서 제외할 파일 목록
- `.env`, `__pycache__`, 가상환경 등

### src/ 디렉토리

#### `src/mcp_server.py`
- FastMCP 기반 MCP 서버
- Claude Desktop, Cline 등에서 사용 가능
- 제공 도구:
  - `analyze_location`: 종합 입지 분석
  - `get_address_coordinates`: 주소 → 좌표 변환
- 제공 리소스:
  - `config://api-info`: API 정보
  - `config://usage-examples`: 사용 예시

#### `src/gradio_app.py`
- Gradio 웹 UI 애플리케이션
- 사용자 친화적인 인터페이스 제공
- HTML 포맷팅으로 예쁜 결과 표시
- JSON 원본 데이터도 함께 제공

#### `src/tools/kakao_tool.py`
- 카카오 로컬 API 래퍼
- LangChain 의존성 제거 (순수 Python)
- 주요 함수:
  - `get_coordinates(address)`: 주소 → 좌표
  - `get_location_profile(address, radius)`: 입지 분석
  - 내부 헬퍼 함수들 (`_get_school_info`, `_get_transport_info` 등)

### docs/ 디렉토리

#### `docs/MCP_SETUP.md`
- MCP 서버 설정 방법
- Claude Desktop, Cline 연동 가이드
- 문제 해결 팁

#### `docs/GRADIO_DEPLOYMENT.md`
- Gradio 앱 배포 가이드
- 로컬 실행, Hugging Face Spaces, Railway 등
- 커스터마이징 방법

## 데이터 흐름

### Gradio 웹 앱
```
사용자 입력 (주소, 반경)
    ↓
gradio_app.py → analyze_location()
    ↓
kakao_tool.py → get_location_profile()
    ↓
카카오 API 호출
    ↓
결과 포맷팅 (HTML + JSON)
    ↓
사용자에게 표시
```

### MCP 서버
```
AI 에이전트 요청
    ↓
mcp_server.py → analyze_location 도구
    ↓
kakao_tool.py → get_location_profile()
    ↓
카카오 API 호출
    ↓
JSON 결과 반환
    ↓
AI 에이전트가 해석하여 응답
```

## 환경 변수

### `.env` 파일
```bash
KAKAO_REST_API_KEY=your_api_key_here
```

### Hugging Face Spaces
- Space Settings → Repository secrets
- Name: `KAKAO_REST_API_KEY`
- Value: API 키

### MCP 서버 (Claude Desktop)
- `claude_desktop_config.json`의 `env` 섹션
```json
{
  "env": {
    "KAKAO_REST_API_KEY": "your_api_key"
  }
}
```

## 의존성

### 핵심 의존성
- `gradio>=4.0.0`: 웹 UI 프레임워크
- `requests>=2.31.0`: HTTP 클라이언트
- `python-dotenv>=1.0.0`: 환경 변수 관리
- `mcp>=0.9.0`: MCP 프로토콜 (FastMCP)

### 선택적 의존성
- `typing-extensions`: 타입 힌팅 (Python 3.8+)

## 개발 워크플로우

### 1. 로컬 개발
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 테스트
python test_tool.py

# 개발 서버 실행
python app.py
```

### 2. MCP 서버 개발
```bash
# MCP 서버 실행
python src/mcp_server.py

# 또는 MCP Inspector로 테스트
mcp-inspector python src/mcp_server.py
```

### 3. 배포
```bash
# Git 초기화
git init
git add .
git commit -m "Initial commit"

# Hugging Face Spaces에 푸시
git remote add hf https://huggingface.co/spaces/USERNAME/SPACE_NAME
git push -u hf main
```

## 확장 가능성

### 새로운 분석 항목 추가
1. `kakao_tool.py`에 새 함수 추가
2. `get_location_profile()` 함수에서 호출
3. `gradio_app.py`의 HTML 포맷팅 업데이트

### 다른 API 통합
1. `src/tools/`에 새 도구 파일 추가
2. MCP 서버에 새 도구 등록
3. Gradio 앱에 새 기능 추가

### UI 커스터마이징
- `gradio_app.py`의 테마 변경
- CSS 스타일 수정
- 컴포넌트 레이아웃 조정

## 보안 고려사항

### API 키 관리
- `.env` 파일 사용 (Git에서 제외)
- Hugging Face Secrets 사용
- 코드에 하드코딩 금지

### Rate Limiting
- 카카오 API 호출 제한 고려
- 필요시 캐싱 구현

### CORS
- Gradio는 자동으로 CORS 처리
- 필요시 `app.launch(allowed_paths=...)`로 제한

## 라이선스

MIT License - 상업적 사용 가능
