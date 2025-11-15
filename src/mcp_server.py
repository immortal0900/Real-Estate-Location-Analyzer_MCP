"""
Real Estate Location Analysis MCP Server

카카오 API를 사용하여 부동산 입지 분석을 제공하는 MCP 서버입니다.
"""

import os
import json
from typing import Optional
from mcp.server.fastmcp import FastMCP

# src.tools 모듈을 import
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tools.kakao_tool import get_location_profile, get_coordinates

# FastMCP 서버 초기화
mcp = FastMCP("부동산 입지 분석 서버")


@mcp.tool()
def analyze_location(address: str, radius: Optional[int] = 3000) -> dict:
    """
    주소의 입지 분석을 수행합니다.

    주어진 주소를 기준으로 주변의 교육환경, 교통여건, 편의시설,
    자연환경, 미래가치 등을 종합적으로 분석합니다.

    Args:
        address: 분석할 주소 (예: "서울시 강남구 역삼동")
        radius: 검색 반경 (미터, 기본값: 3000)

    Returns:
        입지 분석 결과 딕셔너리
    """
    try:
        result = get_location_profile(address, radius)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "주소": address,
            "메시지": "입지 분석 중 오류가 발생했습니다."
        }


@mcp.tool()
def get_address_coordinates(address: str) -> dict:
    """
    주소를 위도/경도 좌표로 변환합니다.

    Args:
        address: 변환할 주소

    Returns:
        {"longitude": 경도, "latitude": 위도} 또는 None
    """
    try:
        coords = get_coordinates(address)
        if coords:
            return coords
        return {"error": "좌표를 찾을 수 없습니다.", "주소": address}
    except Exception as e:
        return {"error": str(e), "주소": address}


@mcp.resource("config://api-info")
def get_api_info() -> str:
    """MCP 서버 API 정보를 제공합니다."""
    info = {
        "서버명": "부동산 입지 분석 서버",
        "버전": "1.0.0",
        "설명": "카카오 로컬 API를 활용한 부동산 입지 분석 도구",
        "도구": [
            {
                "이름": "analyze_location",
                "설명": "주소의 종합 입지 분석",
                "파라미터": {
                    "address": "분석할 주소",
                    "radius": "검색 반경(미터, 기본 3000m)"
                }
            },
            {
                "이름": "get_address_coordinates",
                "설명": "주소를 좌표로 변환",
                "파라미터": {
                    "address": "변환할 주소"
                }
            }
        ],
        "분석항목": {
            "교육환경": ["학교", "학원"],
            "교통여건": ["지하철역", "버스정류장"],
            "편의여건": ["대형마트", "병원"],
            "자연환경": ["공원"],
            "미래가치": ["재건축"]
        }
    }
    return json.dumps(info, ensure_ascii=False, indent=2)


@mcp.resource("config://usage-examples")
def get_usage_examples() -> str:
    """사용 예시를 제공합니다."""
    examples = {
        "예시1": {
            "설명": "강남역 주변 입지 분석 (기본 반경 3km)",
            "도구": "analyze_location",
            "입력": {
                "address": "서울시 강남구 역삼동"
            }
        },
        "예시2": {
            "설명": "도곡동 주변 5km 반경 입지 분석",
            "도구": "analyze_location",
            "입력": {
                "address": "서울시 강남구 도곡동 527",
                "radius": 5000
            }
        },
        "예시3": {
            "설명": "주소 좌표 변환",
            "도구": "get_address_coordinates",
            "입력": {
                "address": "서울시 강남구 테헤란로 427"
            }
        }
    }
    return json.dumps(examples, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run()
