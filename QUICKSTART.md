# 빠른 시작 가이드

부동산 입지 분석 시스템을 5분 안에 시작하는 방법입니다.

## 1단계: 설치

### Windows
```bash
# 1. 저장소 이동
cd C:\real_estate_location_mcp

# 2. 가상환경 생성 및 의존성 설치 (uv 사용)
# uv가 없다면 먼저 설치: pip install uv
uv venv
.venv\Scripts\activate

# 3. 의존성 설치
uv pip install -r requirements.txt
```

### macOS/Linux
```bash
# 1. 저장소 이동
cd /path/to/real_estate_location_mcp

# 2. 가상환경 생성 및 의존성 설치 (uv 사용)
# uv가 없다면 먼저 설치: pip install uv
uv venv
source .venv/bin/activate

# 3. 의존성 설치
uv pip install -r requirements.txt
```

## 2단계: API 키 설정

### 1. 카카오 API 키 발급
1. [카카오 Developers](https://developers.kakao.com/) 접속
2. 로그인 후 **내 애플리케이션** 클릭
3. **애플리케이션 추가하기** 클릭
4. 앱 정보 입력 후 생성
5. **앱 키** 탭에서 **REST API 키** 복사

### 2. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (메모장, VS Code 등)
# KAKAO_REST_API_KEY=여기에_복사한_API_키_붙여넣기
```

## 3단계: 테스트

```bash
python test_tool.py
```

성공하면 다음과 같은 메시지가 표시됩니다:
```
모든 테스트를 통과했습니다!
```

## 4단계: 실행

### 옵션 A: Gradio 웹 앱

```bash
python app.py
```

브라우저에서 `http://localhost:7860` 접속

### 옵션 B: MCP 서버

```bash
python src/mcp_server.py
```

Claude Desktop이나 다른 MCP 클라이언트에서 사용 가능

## 사용 예시

### Gradio 웹 앱에서
1. 주소 입력: `서울시 강남구 역삼동`
2. 검색 반경 선택: `3000m`
3. **입지 분석 시작** 버튼 클릭
4. 결과 확인!

### Claude Desktop (MCP)에서
```
서울시 강남구 도곡동 527 주변 입지를 분석해줘
```

## 문제 해결

### "카카오 REST API 키가 없습니다" 오류
- `.env` 파일이 생성되었는지 확인
- API 키가 올바르게 입력되었는지 확인

### "좌표를 찾지 못했습니다" 오류
- 주소 형식 확인 (예: "서울시 강남구 역삼동")
- 인터넷 연결 확인

### "ModuleNotFoundError" 오류
```bash
uv pip install -r requirements.txt
```

## 더 알아보기

- [MCP 서버 설정](docs/MCP_SETUP.md)
- [Gradio 배포 가이드](docs/GRADIO_DEPLOYMENT.md)
- [전체 README](README.md)

## 다음 단계

- 로컬에서 테스트 완료
- Hugging Face Spaces에 배포
- Claude Desktop과 연동
- UI 커스터마이징

---

문제가 있으시면 [GitHub Issues](https://github.com/YOUR_USERNAME/real_estate_location_mcp/issues)에 제보해주세요!
