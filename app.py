import os
import shutil
import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

upstage_api_key = os.getenv("UPSTAGE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not upstage_api_key:
    raise ValueError("UPSTAGE api key가 없습니다")
if not openai_api_key:
    raise ValueError("OpenAI api key가 없습니다")

input_dir = "./docs/input"
parsed_dir = "./docs/parsed"
os.makedirs(input_dir, exist_ok=True)
os.makedirs(parsed_dir, exist_ok=True)

url = "https://api.upstage.ai/v1/document-ai/document-parse"
headers = {"Authorization": f"Bearer {upstage_api_key}"}

client = OpenAI(api_key=openai_api_key)

def parse_pdf_and_summarize(file_path):
    file_name = os.path.basename(file_path)
    saved_file_path = os.path.join(input_dir, file_name)
    shutil.copy(file_path, saved_file_path)
    
    with open(saved_file_path, "rb") as f:   
        files = {"document": f}
        data = {
            "ocr": "force",
            "output_formats": "['markdown']",
            "coordinates": "true",
            "model": "document-parse-250116"
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        result = response.json()
    
    markdown_content = result["content"]["markdown"]
    markdown_file_path = os.path.join(parsed_dir, file_name.replace(".pdf", "_parsed.md"))
    with open(markdown_file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    prompt = f"""이 단계를 따라 문서를 요약해줘.
    
    ## 요약 단계
    1. 문서의 제목과 저자, 작성 날짜를 확인한다. 확인이 불가능하면 찾지 않고 다음 단계로 넘어간다.
    2. 문서의 전체 구조를 파악한다.
    3. 파악한 구조별로 핵심 내용을 추출한다.
    4. 전체 구조와 구조별 핵심 내용이 직관적으로 보이도록 정리하여 제시한다.
    5. 전체 내용을 3줄로 요약하여 덧붙인다.
    
    {markdown_content[:4000]}""" 
    # API 제한을 고려하여 첫 4000자 사용
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "당신은 문서를 요약하는 전문가입니다. 문서를 잘 확인하고, 사용자가 전체적인 내용을 쉽게 파악할 수 있도록 요약하세요."},
                  {"role": "user", "content": prompt}]
    )

    summary = completion.choices[0].message.content
    return summary

with gr.Blocks() as demo:
    with gr.Row():
        pdf_upload = gr.File(label="📂 PDF 파일 업로드", type="filepath")
    with gr.Row():
        upload_btn = gr.Button("📤 업로드 & 요약")
    with gr.Row():
        output_text = gr.Textbox(label="📌 요약 결과", lines=50)

    upload_btn.click(parse_pdf_and_summarize, inputs=[pdf_upload], outputs=[output_text])

# 🔹 실행
if __name__ == "__main__":
    demo.launch()