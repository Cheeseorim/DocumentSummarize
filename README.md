## Document Summarize

### 📂 문서 요약 및 파싱
- Upstage Document Parse를 통해 pdf 문서를 markdown으로 변환하고, 변환된 문서를 gpt를 이용하여 요약합니다. (document-parse-250116, gpt-4o)
- 환경변수로 Upstage API key와 OpenAI API key가 필요합니다.
- 주로 짧은 논문 자료에 대한 한국어 요약문 생성을 고려하고 프롬프트를 작성하였고, 첫 4000자만 활용하도록 설정하였습니다.

Upstage Document Parse :
https://console.upstage.ai/docs/capabilities/document-parse#document-parse

---
### 🤖 HuggingFace Demo :
https://huggingface.co/spaces/Cheeseorim/DocumentSummarize
