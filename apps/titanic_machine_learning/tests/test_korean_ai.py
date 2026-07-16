"""
Andrew 캐릭터 — 한국어 AI 파이프라인 검증.
kiwipiepy(형태소 분석) + ollama(EEVE-Korean 모델) 통합 테스트.

pytest 실행 (ollama 서버 필요):
    cd backend
    python -m pytest apps/titanic_machine_learning/tests/test_korean_ai.py -m ollama -v -s

직접 실행:
    python apps/titanic_machine_learning/tests/test_korean_ai.py
"""
import sys
from pathlib import Path

import pytest

# 직접 실행 시 sys.path 보정
_here = Path(__file__).resolve().parent
_apps_dir = str(_here.parent.parent.parent)
if _apps_dir not in sys.path:
    sys.path.insert(0, _apps_dir)


def _require_kiwi():
    """kiwipiepy 미설치 시 ImportError 대신 skip."""
    try:
        from kiwipiepy import Kiwi  # noqa: F401
    except ImportError:
        pytest.skip("kiwipiepy 미설치 — pip install kiwipiepy")


def _require_ollama():
    """ollama 미설치 시 ImportError 대신 skip."""
    try:
        import ollama  # noqa: F401
    except ImportError:
        pytest.skip("ollama 미설치 — pip install ollama")


def run_korean_ai(user_text: str) -> str:
    """kiwipiepy 전처리 → EEVE-Korean(ollama) 추론 파이프라인."""
    from kiwipiepy import Kiwi
    import ollama

    kiwi = Kiwi()
    kiwi.global_config.space_tolerance = 2

    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    cleaned_text = kiwi.space(user_text)
    print(f"원본 문장: {user_text}")
    print(f"정제된 문장: {cleaned_text}")

    tokens = kiwi.tokenize(cleaned_text)
    nouns = [t.form for t in tokens if t.tag.startswith("NN")]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] EEVE-Korean 모델 추론 중... ---")
    response = ollama.chat(
        model="anpigon/eeve-korean-10.8b:latest",
        messages=[{"role": "user", "content": cleaned_text}],
    )
    return response["message"]["content"]


@pytest.mark.ollama
def test_korean_ai_pipeline():
    _require_kiwi()
    _require_ollama()

    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer) > 0


if __name__ == "__main__":
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)
    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)
