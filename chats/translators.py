import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation API 클라이언트 생성
# set GOOGLE_APPLICATION_CREDENTIALS=경로
client = translate.Client()


# google_translate()함수를 작성
# 3개의 인자 필요 & 형식 지정
def google_translate(
    text: str,  # 우리가 번역할 대상 문자열
    source: str,  # 입력할 source
    target: str,  # 바꿔줄 target
):
    # 문자열 입력 이후 좌우 공백을 제거하고 빈 문자열인지 확인
    text = text.strip()
    if not text:
        return ""

    # 번역 요청
    translation = client.translate(text, source_language=source, target_language=target)

    # 번역된 텍스트 반환
    return translation["translatedText"]


"""
if __name__ == "__main__":
    text = "안녕하세요. 좋은 하루 보내세요."
    source_lang = "ko"
    target_lang = "en"

    translated_text = google_translate(text, source_lang, target_lang)
    print("Translated text:", translated_text)
"""
