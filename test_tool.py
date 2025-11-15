"""
카카오 입지 분석 도구 테스트 스크립트

이 스크립트를 실행하여 API가 정상적으로 작동하는지 확인할 수 있습니다.
"""

import sys
from pathlib import Path
import json

# src 경로 추가
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.tools.kakao_tool import get_location_profile, get_coordinates


def test_coordinates():
    """좌표 변환 테스트"""
    print("=" * 60)
    print("테스트 1: 주소 → 좌표 변환")
    print("=" * 60)

    test_address = "서울시 강남구 역삼동"
    print(f"입력 주소: {test_address}")

    coords = get_coordinates(test_address)
    if coords:
        print(f"[성공]")
        print(f"   경도: {coords['longitude']}")
        print(f"   위도: {coords['latitude']}")
        return True
    else:
        print("[실패] 좌표를 찾을 수 없습니다.")
        return False


def test_location_profile():
    """입지 분석 테스트"""
    print("\n" + "=" * 60)
    print("테스트 2: 입지 분석")
    print("=" * 60)

    test_address = "서울시 강남구 도곡동 527"
    test_radius = 3000
    print(f"입력 주소: {test_address}")
    print(f"검색 반경: {test_radius}m")

    result = get_location_profile(test_address, test_radius)

    if "메시지" in result and result.get("좌표") is None:
        print(f"[실패] {result['메시지']}")
        return False

    print("[성공]")
    print("\n[분석 결과]")
    print(f"주소: {result['주소']}")
    print(f"좌표: 위도 {result['좌표']['latitude']:.6f}, 경도 {result['좌표']['longitude']:.6f}")

    # 교육환경
    print("\n[교육환경]")
    print(f"  학교: {len(result['교육환경']['학교'])}개")
    print(f"  학원: {len(result['교육환경']['학원'])}개")

    # 교통여건
    print(f"\n[교통여건] {len(result['교통여건'])}개")

    # 편의여건
    print(f"\n[편의여건]")
    print(f"  대형마트: {len(result['편의여건']['대형마트'])}개")
    print(f"  병원: {len(result['편의여건']['병원'])}개")

    # 자연환경
    print(f"\n[자연환경] {len(result['자연환경'])}개 공원")

    # 미래가치
    print(f"\n[미래가치] {len(result['미래가치'])}개 재건축 정보")

    # 상세 결과 (선택사항)
    print("\n" + "=" * 60)
    print("상세 JSON 결과를 보시겠습니까? (y/n): ", end="")
    response = input().strip().lower()
    if response == 'y':
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))

    return True


def main():
    """메인 테스트 함수"""
    print("\n")
    print("부동산 입지 분석 도구 테스트")
    print("=" * 60)
    print("이 스크립트는 카카오 API 연동이 정상적으로 작동하는지 테스트합니다.")
    print("=" * 60)

    try:
        # 테스트 1: 좌표 변환
        coords_ok = test_coordinates()

        # 테스트 2: 입지 분석
        profile_ok = test_location_profile()

        # 결과 요약
        print("\n" + "=" * 60)
        print("테스트 결과 요약")
        print("=" * 60)
        print(f"좌표 변환: {'[통과]' if coords_ok else '[실패]'}")
        print(f"입지 분석: {'[통과]' if profile_ok else '[실패]'}")

        if coords_ok and profile_ok:
            print("\n모든 테스트를 통과했습니다!")
            print("\n다음 단계:")
            print("1. Gradio 웹 앱 실행: python app.py")
            print("2. MCP 서버 실행: python src/mcp_server.py")
            return 0
        else:
            print("\n일부 테스트가 실패했습니다.")
            print("\n문제 해결:")
            print("1. .env 파일에 KAKAO_REST_API_KEY가 올바르게 설정되어 있는지 확인")
            print("2. 인터넷 연결 확인")
            print("3. 카카오 API 키가 유효한지 확인")
            return 1

    except Exception as e:
        print(f"\n[오류 발생] {str(e)}")
        print("\n가능한 원인:")
        print("1. KAKAO_REST_API_KEY가 설정되지 않음")
        print("2. 네트워크 연결 문제")
        print("3. 의존성 패키지 누락")
        print("\n해결 방법:")
        print("1. .env 파일 생성: cp .env.example .env")
        print("2. .env 파일에 API 키 입력")
        print("3. 의존성 설치: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
