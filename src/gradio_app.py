"""
부동산 입지 분석 Gradio 웹 애플리케이션

카카오 API를 사용하여 부동산 입지를 분석하는 웹 인터페이스입니다.
"""

import os
import json
import gradio as gr
from typing import Dict, Tuple
import sys
from pathlib import Path

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent))
from tools.kakao_tool import get_location_profile, get_coordinates


def format_result_as_html(result: dict) -> str:
    """분석 결과를 보기 좋은 HTML로 포맷팅합니다."""

    if "메시지" in result and result.get("좌표") is None:
        return f"""
        <div style="padding: 20px; background-color: #fff3cd; border-radius: 8px; border: 1px solid #ffc107;">
            <h3 style="color: #856404;">알림</h3>
            <p>{result['메시지']}</p>
            <p>입력한 주소: <strong>{result['주소']}</strong></p>
        </div>
        """

    html = f"""
    <div style="font-family: 'Noto Sans KR', sans-serif; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">입지 분석 결과</h2>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #34495e;">기본 정보</h3>
            <p><strong>주소:</strong> {result['주소']}</p>
            <p><strong>좌표:</strong> 위도 {result['좌표']['latitude']:.6f}, 경도 {result['좌표']['longitude']:.6f}</p>
        </div>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #e74c3c;">교육환경</h3>
            <h4 style="color: #c0392b; margin-top: 10px;">학교</h4>
    """

    if result['교육환경']['학교']:
        for school in result['교육환경']['학교']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #fdecea; border-left: 3px solid #e74c3c; margin-bottom: 8px;">
                <strong>{school['이름']}</strong><br>
                주소: {school['주소']}<br>
                거리: {school['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 학교가 없습니다.</p>"

    html += "<h4 style='color: #c0392b; margin-top: 15px;'>학원</h4>"

    if result['교육환경']['학원']:
        for academy in result['교육환경']['학원']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #fdecea; border-left: 3px solid #e74c3c; margin-bottom: 8px;">
                <strong>{academy['이름']}</strong><br>
                주소: {academy['주소']}<br>
                거리: {academy['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 학원이 없습니다.</p>"

    html += """
        </div>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #3498db;">교통여건</h3>
    """

    if result['교통여건']:
        for transport in result['교통여건']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #ebf5fb; border-left: 3px solid #3498db; margin-bottom: 8px;">
                <strong>{transport['이름']}</strong><br>
                주소: {transport['주소']}<br>
                거리: {transport['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 대중교통이 없습니다.</p>"

    html += """
        </div>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #9b59b6;">편의여건</h3>
            <h4 style="color: #8e44ad; margin-top: 10px;">대형마트</h4>
    """

    if result['편의여건']['대형마트']:
        for mart in result['편의여건']['대형마트']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #f4ecf7; border-left: 3px solid #9b59b6; margin-bottom: 8px;">
                <strong>{mart['이름']}</strong><br>
                주소: {mart['주소']}<br>
                거리: {mart['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 대형마트가 없습니다.</p>"

    html += "<h4 style='color: #8e44ad; margin-top: 15px;'>병원</h4>"

    if result['편의여건']['병원']:
        for hospital in result['편의여건']['병원']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #f4ecf7; border-left: 3px solid #9b59b6; margin-bottom: 8px;">
                <strong>{hospital['이름']}</strong><br>
                주소: {hospital['주소']}<br>
                거리: {hospital['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 병원이 없습니다.</p>"

    html += """
        </div>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #27ae60;">자연환경</h3>
    """

    if result['자연환경']:
        for nature in result['자연환경']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #eafaf1; border-left: 3px solid #27ae60; margin-bottom: 8px;">
                <strong>{nature['이름']}</strong><br>
                주소: {nature['주소']}<br>
                거리: {nature['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 공원이 없습니다.</p>"

    html += """
        </div>

        <div style="background-color: white; padding: 15px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #f39c12;">미래가치</h3>
    """

    if result['미래가치']:
        for future in result['미래가치']:
            html += f"""
            <div style="margin-left: 20px; padding: 8px; background-color: #fef5e7; border-left: 3px solid #f39c12; margin-bottom: 8px;">
                <strong>{future['이름']}</strong><br>
                주소: {future['주소']}<br>
                거리: {future['거리(미터)']}m
            </div>
            """
    else:
        html += "<p style='margin-left: 20px; color: #7f8c8d;'>주변에 재건축 정보가 없습니다.</p>"

    html += """
        </div>
    </div>
    """

    return html


def analyze_location(address: str, radius: int) -> Tuple[str, str]:
    """
    입지를 분석하고 HTML 결과와 JSON 결과를 반환합니다.

    Args:
        address: 분석할 주소
        radius: 검색 반경 (미터)

    Returns:
        (HTML 결과, JSON 결과) 튜플
    """
    if not address or address.strip() == "":
        error_html = """
        <div style="padding: 20px; background-color: #f8d7da; border-radius: 8px; border: 1px solid #f5c6cb;">
            <h3 style="color: #721c24;">오류</h3>
            <p>주소를 입력해주세요.</p>
        </div>
        """
        return error_html, json.dumps({"error": "주소를 입력해주세요."}, ensure_ascii=False, indent=2)

    try:
        result = get_location_profile(address, radius)
        html_result = format_result_as_html(result)
        json_result = json.dumps(result, ensure_ascii=False, indent=2)
        return html_result, json_result
    except Exception as e:
        error_html = f"""
        <div style="padding: 20px; background-color: #f8d7da; border-radius: 8px; border: 1px solid #f5c6cb;">
            <h3 style="color: #721c24;">오류 발생</h3>
            <p>{str(e)}</p>
            <p><small>카카오 API 키가 설정되어 있는지 확인해주세요.</small></p>
        </div>
        """
        return error_html, json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


def create_gradio_interface():
    """Gradio 인터페이스를 생성합니다."""

    # 예시 주소 목록
    examples = [
        ["서울시 강남구 역삼동", 3000],
        ["서울시 강남구 도곡동 527", 5000],
        ["서울시 송파구 잠실동", 3000],
        ["서울시 서초구 반포동", 4000],
    ]

    with gr.Blocks(
        title="부동산 입지 분석",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: 'Noto Sans KR', sans-serif;
        }
        """
    ) as app:
        gr.Markdown(
            """
            # 부동산 입지 분석 시스템

            카카오 로컬 API를 활용하여 입력한 주소 주변의 입지 정보를 종합적으로 분석합니다.

            ### 분석 항목
            - **교육환경**: 학교, 학원
            - **교통여건**: 지하철역, 버스정류장
            - **편의여건**: 대형마트, 병원
            - **자연환경**: 공원
            - **미래가치**: 재건축 정보

            ---
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                address_input = gr.Textbox(
                    label="주소",
                    placeholder="예: 서울시 강남구 역삼동",
                    lines=1,
                    info="분석하고자 하는 부동산의 주소를 입력하세요"
                )

                radius_input = gr.Slider(
                    label="검색 반경 (미터)",
                    minimum=500,
                    maximum=10000,
                    value=3000,
                    step=500,
                    info="주변 시설을 검색할 반경을 설정하세요 (500m ~ 10km)"
                )

                analyze_btn = gr.Button(
                    "입지 분석 시작",
                    variant="primary",
                    size="lg"
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 분석 결과")
                html_output = gr.HTML(
                    label="분석 결과",
                    value="<p style='text-align: center; color: #7f8c8d; padding: 40px;'>주소를 입력하고 '입지 분석 시작' 버튼을 눌러주세요.</p>"
                )

        with gr.Accordion("JSON 결과 보기", open=False):
            json_output = gr.Code(
                label="JSON 형식 결과",
                language="json",
                lines=10
            )

        gr.Markdown("### 예시")
        gr.Examples(
            examples=examples,
            inputs=[address_input, radius_input],
            label="클릭하여 예시 주소로 시도해보세요"
        )

        gr.Markdown(
            """
            ---
            <div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
                <p>본 서비스는 <strong>카카오 로컬 API</strong>를 사용합니다.</p>
                <p>데이터는 실시간으로 제공되며, 정확도는 카카오 데이터베이스에 따라 달라질 수 있습니다.</p>
            </div>
            """
        )

        # 이벤트 핸들러
        analyze_btn.click(
            fn=analyze_location,
            inputs=[address_input, radius_input],
            outputs=[html_output, json_output]
        )

        # Enter 키로도 실행 가능
        address_input.submit(
            fn=analyze_location,
            inputs=[address_input, radius_input],
            outputs=[html_output, json_output]
        )

    return app


if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # 외부 접근을 위한 공개 URL 생성
    )
