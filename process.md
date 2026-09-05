# 대화형 Blogger 콘텐츠 작성 프로세스

## 1. 시작

Codex에서 하나의 주제로 대화를 시작한다. 처음부터 완성된 글을 작성하지 않고, 대화 중 필요한 내용을 `contents/`에 계속 추가한다.

```text
이 대화를 Astro 출시 요금 비교 시리즈 1편으로 시작해줘.
raw 대화는 docs/content_hist/20260906_astro_go.md에 추가해줘.
콘텐츠 경로는 contents/2026/09/astro_go/astro_ai_launch_pricing.md로 해줘.
```

## 2. 콘텐츠 추가

대화가 진행될 때마다 원하는 작업을 요청한다.

```text
지금까지의 대화를 contents/2026/09/astro_go/astro_ai_launch_pricing.md에 이어서 추가해줘.
이 부분은 질문과 답변 형식으로 정리해줘.
지금까지의 내용을 표로 요약해서 추가해줘.
이 내용을 다음 회차로 넘기지 말고 현재 글에 추가해줘.
```

내용이 길어지면 사용자가 회차를 결정한다.

```text
여기까지를 1편으로 마무리하고, 다음 내용은 2편으로 이어가자.
다음 편 경로는 contents/2026/09/astro_go/001.md로 해줘.
```

## 3. 이미지·YouTube 추가

글이 텍스트만 이어지지 않도록 주제에 맞는 이미지와 영상을 넣는다. 링크는 실제로 열리고 내용과 일치하는지 확인한다.

```text
이 글에 필요한 이미지를 만들어 contents/2026/09/astro_go/astro_ai_launch_pricing.png로 저장하고 추가해줘.
관련 YouTube 영상도 실제 영상인지 확인해서 넣어줘.
확인되지 않거나 주제와 맞지 않는 링크는 사용하지 마.
```

## 4. 출처와 마무리

가격, 요금, 출시일, 정책, 기능처럼 변할 수 있는 내용은 출처를 확인한다. 사용한 사실·이미지·YouTube의 원본 URL은 글 마지막에 모은다.

```text
본문의 사실과 링크를 다시 확인해줘.
글 맨 아래에 `## 출처`를 만들고 사용한 원본 URL을 모두 추가해줘.
지금까지의 대화를 독자가 이해할 수 있는 결론으로 마무리해줘.
```

## 5. Blogger 형식 변환

게시 전에 대화를 Blogger용 HTML로 변환한다.

```text
contents/2026/09/astro_go/astro_ai_launch_pricing.md를 Blogger용 astro_ai_launch_pricing.html로 변환해줘.
질문은 왼쪽, 답변은 오른쪽 말풍선으로 표시해줘.
표·이미지·YouTube·출처가 본문에서 정상적으로 보이게 해줘.
본문 마지막에는 출처 URL 영역을 유지해줘.
```

## 6. Blogger 게시

기존 Blogger 게시 기능을 사용해 먼저 비공개 초안으로 등록한다.

```text
이 콘텐츠를 Blogger 비공개 초안으로 올려줘.
제목, 본문, 이미지, YouTube, 출처 URL이 모두 포함됐는지 확인해줘.
```

Blogger 화면에서 말풍선, 이미지, 영상, 링크와 출처를 확인한 뒤 공개한다.

```text
검수 완료했어. 승인된 Blogger 초안을 공개 게시해줘.
```

## 7. 전체 순서

```text
주제 대화 시작
  → docs/content_hist/YYYYMMDD_topic.md에 raw 대화 추가
  → contents/YYYY/MM/topic/content-related-name.md 생성 또는 내용 추가
  → 대화·요약·표를 계속 추가
  → 이미지·YouTube 링크 추가
  → 사실·링크 확인
  → 글 하단에 출처 URL 추가
  → 결론 또는 다음 회차 안내
  → Blogger용 HTML 변환
  → Blogger 비공개 초안
  → 화면 검수
  → 승인 후 공개
```

## 8. 금지 사항

- 확인되지 않은 이미지·YouTube URL 사용
- 본문에 사용한 출처를 생략
- AI 답변을 사실 확인 없이 그대로 공개
- 개인정보·비공개 대화·API 키 게시
- 검수 전 자동 공개
