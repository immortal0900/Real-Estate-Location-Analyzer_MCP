# MCP 서버 설정 가이드

이 문서는 부동산 입지 분석 MCP 서버를 다양한 AI 에이전트와 연동하는 방법을 설명합니다.

## 목차
- [Claude Desktop 연동](#claude-desktop-연동)
- [Cline (VS Code) 연동](#cline-vs-code-연동)
- [MCP Inspector로 테스트](#mcp-inspector로-테스트)
- [문제 해결](#문제-해결)

## 사전 준비

1. **Python 3.8 이상** 설치
2. **uv 설치** (패키지 관리자):
   ```bash
   pip install uv
   ```
3. **카카오 REST API 키** 발급 ([발급 방법](#카카오-api-키-발급))
4. **의존성 설치**:
   ```bash
   cd C:\real_estate_location_mcp
   uv venv
   .venv\Scripts\activate  # macOS/Linux: source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

## Claude Desktop 연동

### 1. 설정 파일 위치

Windows: `%APPDATA%\Claude\claude_desktop_config.json`
macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

### 2. 설정 추가

```json
{
  "mcpServers": {
    "real-estate-location": {
      "command": "python",
      "args": [
        "C:/real_estate_location_mcp/src/mcp_server.py"
      ],
      "env": {
        "KAKAO_REST_API_KEY": "your_kakao_rest_api_key_here"
      }
    }
  }
}
```

**주의사항:**
- 경로는 절대 경로를 사용하세요
- Windows에서는 백슬래시(`\`) 대신 슬래시(`/`) 사용
- `KAKAO_REST_API_KEY`를 실제 API 키로 교체

### 3. Claude Desktop 재시작

설정 후 Claude Desktop을 완전히 종료하고 다시 시작합니다.

### 4. 사용 방법

Claude Desktop에서 다음과 같이 요청하세요:

```
서울시 강남구 역삼동의 입지를 분석해줘
```

또는

```
도곡동 527번지 주변 5km 반경의 교육환경을 조사해줘
```

## Cline (VS Code) 연동

### 1. Cline 설치

VS Code에서 Cline 확장 프로그램을 설치합니다.

### 2. MCP 서버 설정

Cline 설정에서 MCP 서버를 추가합니다:

```json
{
  "mcpServers": {
    "real-estate-location": {
      "command": "python",
      "args": ["C:/real_estate_location_mcp/src/mcp_server.py"],
      "env": {
        "KAKAO_REST_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 3. 사용 방법

Cline 채팅에서 부동산 입지 분석을 요청할 수 있습니다.

## MCP Inspector로 테스트

MCP 서버가 제대로 작동하는지 테스트하려면 MCP Inspector를 사용하세요:

```bash
# MCP Inspector 설치
npm install -g @modelcontextprotocol/inspector

# 서버 테스트
mcp-inspector python C:/real_estate_location_mcp/src/mcp_server.py
```

브라우저에서 `http://localhost:5173`으로 접속하여 도구를 테스트할 수 있습니다.

## 카카오 API 키 발급

1. [카카오 Developers](https://developers.kakao.com/) 접속
2. 로그인 후 **내 애플리케이션** 메뉴 선택
3. **애플리케이션 추가하기** 클릭
4. 애플리케이션 정보 입력 후 생성
5. 생성된 앱의 **앱 키** 탭에서 **REST API 키** 복사
6. 복사한 키를 MCP 설정의 `KAKAO_REST_API_KEY`에 입력

## 문제 해결

### 서버가 시작되지 않음

**증상:** Claude Desktop에서 MCP 서버를 찾을 수 없음

**해결방법:**
1. Python이 PATH에 등록되어 있는지 확인
   ```bash
   python --version
   ```
2. 의존성이 설치되어 있는지 확인
   ```bash
   uv pip list | findstr mcp
   ```
3. 경로가 올바른지 확인 (절대 경로 사용)

### API 키 오류

**증상:** "카카오 REST API 키가 없습니다" 오류

**해결방법:**
1. API 키가 올바르게 입력되었는지 확인
2. API 키에 공백이나 따옴표가 포함되지 않았는지 확인
3. 카카오 Developers에서 앱이 활성화되어 있는지 확인

### 좌표를 찾을 수 없음

**증상:** "좌표를 찾지 못했습니다" 메시지

**해결방법:**
1. 주소 형식이 정확한지 확인 (예: "서울시 강남구 역삼동")
2. 도로명 주소 또는 지번 주소 시도
3. 상세 주소 없이 동/읍/면 단위로 시도

### 데이터가 없음

**증상:** 주변에 시설이 없다고 나옴

**해결방법:**
1. 검색 반경(radius)을 늘려보세요 (기본 3000m → 5000m)
2. 실제로 해당 지역에 시설이 없을 수 있습니다
3. 다른 주소로 테스트해보세요

## 추가 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [FastMCP 문서](https://github.com/jlowin/fastmcp)
- [카카오 로컬 API 문서](https://developers.kakao.com/docs/latest/ko/local/common)

## 사용 예시

### 예시 1: 기본 입지 분석
```
User: 서울시 강남구 역삼동의 입지를 분석해줘

Claude: analyze_location 도구를 사용하여 분석하겠습니다.
[분석 결과 표시]
```

### 예시 2: 맞춤 반경 설정
```
User: 도곡동 527번지 주변 5km 이내의 교통 및 교육 환경을 조사해줘

Claude: analyze_location 도구를 radius=5000으로 사용하겠습니다.
[분석 결과 표시]
```

### 예시 3: 좌표 변환
```
User: 테헤란로 427의 좌표를 알려줘

Claude: get_address_coordinates 도구를 사용하겠습니다.
결과: 위도 37.xxxxx, 경도 127.xxxxx
```

---

문제가 계속되면 GitHub Issues에 제보해주세요.
