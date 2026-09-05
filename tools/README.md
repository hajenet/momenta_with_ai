# Project tools

이 폴더는 별도 서버가 아니라 Codex가 콘텐츠를 Blogger 형식으로 준비할 때 사용하는 보조 도구다.

## 대화형 HTML 변환

```powershell
python tools/conversation_renderer.py `
  contents/2026/09/astro_go/000.md `
  contents/2026/09/astro_go/000.html
```

생성 HTML은 `.conversation-post` 아래로 CSS를 한정하고, 사용자 질문은 왼쪽, AI 답변은 오른쪽 말풍선으로 렌더링한다. 외부 JavaScript와 자동 스크롤은 사용하지 않는다.

## 기존 Blogger 기능 재사용

게시 인증·Blogger API·DB·승인 흐름은 `E:/Users/kimsong/projects/google_side_job/src/sidejob`를 재사용한다.

연결 전 확인 사항:

- 기존 `src/sidejob/publishing.py`의 `BloggerPublisher` 재사용
- 현재 `publish_private()`는 `isDraft=false`를 보내므로 비공개 초안 목적에 맞게 수정 필요
- 현재 기존 변환기는 일반 Markdown용이므로, 대화형 콘텐츠에는 이 폴더의 renderer 결과를 사용
- OAuth 토큰과 API 키는 이 저장소에 복사하지 않음

