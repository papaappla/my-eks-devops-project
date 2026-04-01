import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents="Explain how AI works in a long words as you can make"
)

# Warning 없이 텍스트 파트만 추출하기
# parts 리스트 중에서 text 속성이 있는 요소만 합칩니다.
full_text = "".join([part.text for part in response.candidates[0].content.parts if part.text])

print("--- Gemini의 답변 ---")
print(full_text.strip())