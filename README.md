---
title: 부동산 입지 분석 시스템
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: mit
short_description: Space with tags for MCP 1st Birthday party
tags:
  - building-mcp-track-enterprise
---

# 부동산 입지 분석 시스템

카카오 로컬 API를 활용하여 부동산의 입지를 종합적으로 분석하는 시스템입니다.
**MCP(Model Context Protocol) 서버**와 **Gradio 웹 애플리케이션**을 모두 제공합니다.

## 주요 기능

### 분석 항목
- **교육환경**: 주변 학교, 학원 정보
- **교통여건**: 지하철역, 버스정류장
- **편의여건**: 대형마트, 병원
- **자연환경**: 공원
- **미래가치**: 재건축 정보

### 제공 형태
1. **Gradio 웹 앱**: 사용자 친화적인 웹 인터페이스
2. **MCP 서버**: AI 에이전트가 활용할 수 있는 도구 서버

## 사용 방법

### 1. Gradio 웹 앱 사용

Hugging Face Spaces에서 바로 사용하거나, 로컬에서 실행할 수 있습니다.

#### 로컬 실행
```bash
# 저장소 클론
git clone https://huggingface.co/spaces/MCP-1st-Birthday/real-estate-location-mcp
cd real-estate-location-mcp

# 가상환경 생성 및 의존성 설치 (uv 사용)
# uv가 없다면 먼저 설치: pip install uv
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 KAKAO_REST_API_KEY 입력

# 실행
python app.py
```

### 2. MCP 서버 사용

AI 에이전트(Claude Desktop, Cline 등)에서 사용할 수 있는 MCP 서버를 제공합니다.

#### 방법 A: 원격 MCP Endpoint (권장)

별도 설치 없이 Hugging Face Spaces에서 호스팅되는 MCP 서버에 바로 연결할 수 있습니다.

`claude_desktop_config.json` 파일에 다음을 추가:

```json
{
  "mcpServers": {
    "real-estate-analyzer": {
      "url": "https://immortal0900-real-estate-location-analyzer-mcp.hf.space/gradio_api/mcp/sse"
    }
  }
}
```

#### 방법 B: 로컬 MCP 서버

```bash
# 서버 실행
python src/mcp_server.py
```

`claude_desktop_config.json` 파일에 다음을 추가:

```json
{
  "mcpServers": {
    "real-estate-location": {
      "command": "python",
      "args": [
        "C:/real_estate_location_mcp/src/mcp_server.py"
      ],
      "env": {
        "KAKAO_REST_API_KEY": "your_kakao_api_key_here"
      }
    }
  }
}
```

## API 키 발급

1. [카카오 Developers](https://developers.kakao.com/) 접속
2. 애플리케이션 생성
3. **REST API 키** 복사
4. `.env` 파일에 `KAKAO_REST_API_KEY` 설정

## 프로젝트 구조

```
real_estate_location_mcp/
├── app.py                          # Hugging Face Spaces 메인 파일
├── requirements.txt                # Python 의존성
├── .env.example                    # 환경 변수 예시
├── README.md                       # 프로젝트 문서
├── src/
│   ├── __init__.py
│   ├── mcp_server.py              # MCP 서버
│   ├── gradio_app.py              # Gradio 웹 앱
│   └── tools/
│       ├── __init__.py
│       └── kakao_tool.py          # 카카오 API 도구
└── docs/
    ├── MCP_SETUP.md               # MCP 서버 설정 가이드
    └── GRADIO_DEPLOYMENT.md       # Gradio 배포 가이드
```

## MCP 도구

MCP 서버는 다음 도구들을 제공합니다:

### `analyze_location`
주소의 종합 입지 분석을 수행합니다.

**파라미터:**
- `address` (str): 분석할 주소
- `radius` (int, optional): 검색 반경(미터, 기본값: 3000)

**예시:**
```python
{
  "address": "서울시 강남구 역삼동",
  "radius": 5000
}
```

### `get_address_coordinates`
주소를 위도/경도 좌표로 변환합니다.

**파라미터:**
- `address` (str): 변환할 주소

**예시:**
```python
{
  "address": "서울시 강남구 테헤란로 427"
}
```

## 배포

### Hugging Face Spaces 배포

1. [Hugging Face Spaces](https://huggingface.co/spaces) 에서 새 Space 생성
2. SDK로 **Gradio** 선택
3. 저장소에 코드 푸시:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/real-estate-location-mcp
   git push -u origin main
   ```
4. Space Settings에서 **Secrets** 설정:
   - Name: `KAKAO_REST_API_KEY`
   - Value: 카카오 API 키

## 라이선스

MIT License

## 감사의 말

이 프로젝트는 [카카오 로컬 API](https://developers.kakao.com/docs/latest/ko/local/common)를 사용합니다.

## 문의

이슈나 질문이 있으시면 GitHub Issues에 등록해주세요.

---

Made with Gradio and FastMCP

