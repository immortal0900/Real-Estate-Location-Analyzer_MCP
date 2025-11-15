"""
Hugging Face Spaces용 메인 애플리케이션 파일

이 파일은 Hugging Face Spaces에서 실행됩니다.
"""

import sys
from pathlib import Path

# src 경로를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.gradio_app import create_gradio_interface

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()
