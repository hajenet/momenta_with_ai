# 대화형 Blogger 콘텐츠 기술 설계

## 1. 기술 목표

Codex와 사용자의 대화를 발행 가능한 Blogger 글로 변환한다.

## 핵심 제작 이유

이 프로젝트는 대화를 자동으로 수집하거나 한 번에 완성된 글을 생성하기 위한 프로그램이 아니다. 사용자가 Codex와 대화를 시작하고, 대화가 진행되는 동안 다음과 같이 원하는 작업을 지시할 수 있게 하는 것이 목적이다.

- 지금까지의 대화를 그대로 Blogger용 글로 정리
- 지금까지의 내용을 요약
- 특정 내용을 표로 변환
- 질문과 답변을 대화 형식으로 누적
- 다음 회차로 이어질 부분을 현재 콘텐츠에 추가

대화의 방향은 미리 고정하지 않는다. 자유롭게 확장하되, 마지막에는 결론·요약·다음 단계 중 하나로 글을 마무리한다.

기술적으로 필요한 결과는 다음과 같다.

- 대화 raw 기록과 Blogger용 정리 콘텐츠를 분리한다.
- 대화 중간중간 요청한 내용만 콘텐츠 파일에 추가한다.
- 필요할 때 여러 `NNN.md` 파일로 이어지는 글·시리즈를 만든다.
- Blogger가 표시할 수 있는 HTML·CSS로 변환한다.
- 이미지·YouTube 링크와 글 하단 출처 URL을 정확히 포함한다.
- 기존 Blogger 비공개 초안·승인·게시 기능을 재사용한다.

## 2. 현재 프로젝트 구조

현재 `momenta_with_ai`는 대화형 Blogger 콘텐츠 기능을 설계하는 초기 저장소다.

```text
momenta_with_ai/
├─ README.md
├─ anal.md
├─ tech.md
└─ docs/
   └─ ai-news-and-service-ideas.md
```

현재는 발행 콘텐츠를 보관하는 `contents/` 폴더가 아직 없다. `docs/`에는 프로젝트의 목적과 아이디어 문서가 있으며, 앞으로 기술 문서와 운영 문서를 추가할 수 있다.

참고 대상인 `google_side_job`은 다음 영역을 이미 가지고 있다.

```text
google_side_job/
├─ src/sidejob/              # Python 애플리케이션
├─ scripts/                  # 실행·스케줄 등록 스크립트
├─ tests/                    # 테스트
├─ data/                     # SQLite·로그·스냅샷
├─ docs/
│  ├─ skills/                # 글쓰기·검수 규칙
│  ├─ reference/             # 외부 자료·트렌드 기록
│  ├─ publish_content/       # Blogger 발행 원문
│  ├─ work_hist/             # 작업 이력
│  └─ src_run_deploy/        # 실행·배포 문서
└─ README.md
```

`google_side_job`은 현재 Google Trends 기반 일반 정보 글 생성에 맞춰져 있으므로, 대화형 콘텐츠 기능을 추가할 때 발행 콘텐츠와 프로젝트 문서를 같은 `docs/` 영역에 계속 섞지 않는 것이 좋다.

## 3. `contents/`와 `docs/` 영역 분리

대화형 Blogger 콘텐츠는 `contents/`에 보관하고, 프로젝트를 설명·운영하는 문서는 `docs/`에 보관한다.

```text
momenta_with_ai/
├─ README.md                         # 프로젝트 진입점과 사용법
├─ contents/                         # 실제 발행 대상 콘텐츠
│  └─ YYYY/MM/topic/
│     ├─ 000.md                      # Blogger에 올릴 정리된 콘텐츠
│     ├─ 000.html                    # Blogger용 HTML/CSS
│     └─ 000.png                     # 해당 콘텐츠의 이미지
├─ docs/                             # 프로젝트 설명·설계·운영 문서
│  ├─ analysis/                      # 요구사항·정책·검토
│  ├─ design/                        # 기술 설계
│  ├─ operations/                    # Blogger 게시·검수 절차
│  ├─ content_hist/                  # Codex 대화 raw 콘텐츠
│  │  └─ YYYYMMDD_topic.md
│  ├─ history/                       # 작업 결정과 변경 이력
│  └─ reference/                     # 외부 공식 문서·참고 자료
├─ anal.md                           # 현재 핵심 분석 문서
└─ tech.md                           # 현재 핵심 기술 문서
```

분리 원칙:

- `contents/`는 독자에게 공개할 수 있는 콘텐츠와 그 제작 원본을 둔다.
- `docs/`는 개발자·운영자가 프로젝트를 이해하기 위한 문서를 둔다.
- 대화 raw 기록은 `docs/content_hist/YYYYMMDD_topic.md`에 저장한다.
- Blogger용 정리 콘텐츠는 `contents/YYYY/MM/topic/000.md`에 대화 중간중간 추가한다.
- 같은 콘텐츠의 HTML과 이미지는 `000.html`, `000.png`처럼 같은 폴더에 둔다.
- API 키, OAuth 토큰, 개인 대화의 민감정보는 어느 영역에도 저장하지 않는다.
- Blogger 게시 상태와 URL은 기존 `google_side_job`의 게시 기능에서 관리하고, 실제 비밀 인증정보는 환경변수로 관리한다.
- `google_side_job/docs/publish_content/`의 기존 원문은 Blogger 게시 어댑터 재사용을 위한 참고 자료로만 본다.

## 4. 별도 프로그램 필요성

별도의 공개 웹사이트나 상시 서버를 새로 만들 필요는 없다. Codex를 대화·콘텐츠 작성 인터페이스로 사용하고 Blogger를 공개 채널로 사용한다. 이 프로젝트에서 새로 필요한 것은 복잡한 자동화 프로그램이 아니라, 누적 콘텐츠를 Blogger 형식으로 전달하는 간단한 규칙과 기존 게시 기능의 재사용이다.

기능별 판단은 다음과 같다.

| 기능 | 별도 제작 필요성 | 역할 |
|---|---|---|
| 대화 입력·수집 어댑터 | 불필요 | 사용자가 현재 Codex 대화를 콘텐츠의 시작점으로 지정한다. |
| 대화 파서·화자 정규화 | 거의 불필요 | 사용자가 그때그때 “그대로”, “요약”, “표”, “대화 형식” 등을 지시하고 콘텐츠에 누적한다. |
| 편집·시리즈 구성기 | 불필요 | 대화의 흐름과 회차 결정은 사용자와 Codex가 대화 중 정한다. |
| 사실·출처 검수기 | 별도 불필요 | 첫 출처는 반드시 제공한다. 이후 오류 지적은 댓글 등 공개 피드백으로 받는다. |
| 대화형 HTML·CSS 형식 | 단순 기능 필요 | 텔레그램·카카오톡 같은 좌우 말풍선 형태로 콘텐츠를 표시한다. |
| 자동 스크롤·TTS | 선택 기능 | 읽기 보조 기능으로 검토하되, 기본 콘텐츠와 분리한다. |
| 로컬 미리보기 | 불필요 | Blogger에 초안으로 올린 뒤 기존 검수 흐름을 사용한다. |
| Blogger 게시 어댑터 | 기존 기능 재사용 가능, 수정 필요 | HTML·메타데이터를 Blogger 비공개 초안으로 등록하고 게시 상태 기록 |
| 콘텐츠 아카이버 | 별도 불필요 | Git의 커밋 이력과 `contents/` 파일 자체가 보관 역할을 한다. |
| 승인·게시 상태 관리자 | 기존 기능 재사용 | 기존 `google_side_job`의 Blogger 초안·승인 흐름을 재사용한다. |
| 알림 채널 | 현재 불필요 | Telegram·Slack 연동은 초기 범위에 넣지 않는다. |

여기서 필요한 HTML·CSS 기능은 별도 웹사이트를 만드는 뜻이 아니다. Blogger 본문에 포함할 간단한 표현 형식이며, 게시 어댑터가 전달할 HTML 콘텐츠의 일부로 처리한다.

## 5. 제작 우선순위

1. 사용자가 원하는 방식으로 대화 콘텐츠를 계속 누적
2. 필요할 때 제목·요약·표·회차·출처를 콘텐츠에 추가
3. 간단한 말풍선 HTML·CSS 형태로 Blogger 본문 생성
4. 기존 Blogger 비공개 초안 등록
5. 기존 승인 절차를 거쳐 공개 게시

초기 범위에서는 실시간 대화 수집, 별도 파서, 시리즈 자동 구성기, 로컬 미리보기, 다중 사용자 계정, 알림 서비스, 상시 서버, GitHub Pages를 제작하지 않는다.

## 6. 권장 시스템 경계

별도 웹 서버를 기본 구성으로 만들지 않는다.

```text
[Codex 대화]
      │ raw 대화 기록을 content_hist에 추가
      ▼
[콘텐츠 추가 요청]
      │
      ├─ contents/YYYY/MM/topic/NNN.md에 내용 추가
      ├─ 필요 시 NNN.html·NNN.png 생성
      ├─ 기존 Blogger 기능으로 비공개 초안 등록
      └─ 사람이 확인 후 공개
```

Codex 대화 자체가 raw 콘텐츠의 시작점이다. 대화의 방향을 미리 정하지 않으며, 사용자가 요청하는 시점에만 `contents/`에 정리 내용을 추가한다.

## 7. 저장 구조 제안

```text
docs/
  content_hist/
    20260906_astro_go.md           # raw 대화
contents/
  2026/09/astro_go/
    000.md                         # Blogger용 정리 콘텐츠
    000.html                       # Blogger용 HTML·CSS
    000.png                        # 글에 사용하는 이미지
    001.md                         # 다음 글 또는 다음 회차
```

### `docs/content_hist/YYYYMMDD_topic.md`

Codex와 나눈 대화 전체를 저장하는 raw 콘텐츠다. 나중에 `contents/`의 내용이 어떤 대화에서 나왔는지 확인하는 근거로 사용한다. 대화가 진행되는 동안 계속 추가하며 요약본으로 덮어쓰지 않는다.

### `contents/YYYY/MM/topic/NNN.md`

사용자가 “지금까지를 콘텐츠에 추가해”, “요약해서 추가해”, “표로 만들어 추가해”라고 요청할 때 만드는 Blogger용 정리 콘텐츠다. 처음부터 하나의 완성된 글로 다시 쓰지 않고, 대화 중 필요한 시점에 내용을 추가한다.

같은 topic 폴더에 `000.md`, `001.md`를 둘 수 있으므로 별도의 `series/` 폴더는 사용하지 않는다.

```markdown
user: Astro 출시 요금은 어떻게 비교돼?

assistant: 먼저 무료 플랜과 유료 플랜을 나누어 보겠습니다.

요약: Astro의 요금 구조를 독자가 빠르게 비교할 수 있도록 정리한다.

| 구분 | 내용 |
|---|---|
| 무료 | 기본 기능 |
| 유료 | 추가 기능과 사용량 기준 |

출처: 공식 가격 페이지
```

이미지와 YouTube는 설명만 적지 않고 실제 링크를 콘텐츠에 넣는다. 링크는 주제와 일치하고 실제로 열리는지 확인한 뒤 사용한다.

```markdown
![Astro 요금 화면](https://example.com/astro-pricing.png)

<iframe src="https://www.youtube.com/embed/VIDEO_ID" title="Astro 소개 영상" loading="lazy" allowfullscreen></iframe>

## 출처

- Astro 공식 가격 페이지: https://astro.build/pricing
- 참고 영상: https://www.youtube.com/watch?v=VIDEO_ID
```

본문 마지막에는 사용한 사실·이미지·영상에 대응하는 `## 출처` 영역과 원본 URL을 반드시 둔다. 확인되지 않은 이미지·영상 링크, 검색 결과 URL, 주제와 무관한 링크는 사용하지 않는다. 글이 텍스트만 길게 이어지지 않도록 주제에 맞는 이미지, 표, 영상 또는 대화 요소를 적절히 섞는다.

### `contents/YYYY/MM/topic/NNN.html`

`NNN.md`를 Blogger에 전달할 HTML·CSS 결과물이다. 질문·답변 말풍선, 이미지, YouTube, 표와 하단 출처 영역을 포함한다.

### `contents/YYYY/MM/topic/NNN.png`

해당 콘텐츠를 위해 만든 이미지 파일이다. 이미지가 여러 장이면 같은 topic 폴더에 추가한다.

### Blogger 게시 상태

게시 상태와 Blogger post ID는 기존 `google_side_job`의 게시·승인 기능을 재사용한다. 별도 아카이버나 별도 상태 관리 프로그램은 만들지 않는다.

## 8. 변환 파이프라인

```text
현재 대화를 `docs/content_hist/YYYYMMDD_topic.md`에 추가
  → 사용자가 원하는 방식으로 콘텐츠 추가
  → `contents/YYYY/MM/topic/NNN.md`에 내용 추가
  → 필요 시 `NNN.html`·`NNN.png` 생성
  → 이미지·YouTube 링크 확인
  → 글 하단에 출처 URL 추가
  → 기존 Blogger 기능으로 비공개 초안 등록
  → 사람 검수
  → 공개 전환
```

### Codex 사용 명령

고정된 별도 앱 명령어가 아니라 현재 대화에서 다음과 같이 요청한다.

```text
이 대화를 Astro 출시 요금 비교 글로 만들어줘.
raw 대화는 docs/content_hist/20260906_astro_go.md에 추가해줘.
정리된 내용은 contents/2026/09/astro_go/astro_ai_launch_pricing.md에 추가해줘.
질문과 답변은 좌우 말풍선으로 표시해줘.
텍스트만 이어지지 않게 주제에 맞는 이미지를 만들어 contents/2026/09/astro_go/astro_ai_launch_pricing.png로 저장해줘.
관련 YouTube 링크도 실제로 확인해서 넣어줘.
본문 마지막에 사용한 사실·이미지·영상의 출처 URL을 반드시 모아줘.
Blogger에는 비공개 초안으로 올려줘.
```

대화 중에는 다음처럼 이어서 요청할 수 있다.

```text
지금까지의 내용을 표로 요약해서 contents/2026/09/astro_go/astro_ai_launch_pricing.md 뒤에 추가해줘.
이 이미지와 YouTube 링크가 실제 내용과 맞는지 확인해줘.
출처 URL을 글 맨 아래에 추가해줘.
현재 글을 결론까지 마무리해줘.
```

AI가 작성한 답변은 사실로 취급하지 않는다. 가격, 출시일, 정책, 법률, 금융, 건강, 제품 사양은 게시 시점의 출처를 확인하고 본문 주장과 연결한다.

## 9. Blogger HTML 설계

Blogger에는 Markdown 원문을 전송하지 않고 HTML 문자열을 전송한다. 대화 한 단위는 의미가 드러나는 HTML 요소로 만든다.

```html
<article class="conversation-post">
  <header class="series-header">
    <p class="series-name">Astro 출시 요금 비교 · 2화</p>
    <h1>Astro 출시 요금 비교</h1>
  </header>

  <div class="chat-row chat-row--user">
    <div class="chat-bubble chat-bubble--user">
      <p>Astro 출시 요금은 어떻게 비교돼?</p>
    </div>
  </div>

  <div class="chat-row chat-row--assistant">
    <div class="chat-bubble chat-bubble--assistant">
      <p>무료 플랜과 유료 플랜을 나누어 비교해보겠습니다.</p>
    </div>
  </div>

  <aside class="editor-note">
    게시일 기준 공식 가격 페이지를 확인했습니다.
  </aside>
</article>
```

CSS는 Blogger 테마와 충돌하지 않도록 글 전용 접두사(`conversation-post`, `chat-row` 등)를 사용한다. 외부 JavaScript와 자동 스크롤은 기본 의존성으로 두지 않는다.

## 10. 렌더링 규칙

- 질문과 답변의 텍스트는 HTML escape 후 출력한다.
- 링크는 검증된 HTTPS URL만 `<a>`로 변환한다.
- 이미지는 권리와 안정적인 호스팅 위치를 확인한 뒤 사용한다.
- Markdown 표·코드·목록은 변환 규칙을 명시하고, 미지원 문법은 소스가 그대로 노출되지 않도록 처리한다.
- 인용 출처는 대화 말풍선과 분리해 본문 하단에 표시한다.
- 제목은 글 전체에 하나의 `<h1>`만 사용한다.
- 다음 편과 이전 편은 시리즈 메타데이터로 생성한다.

## 11. 게시 상태 모델

```text
captured
  → edited
  → fact_checked
  → rendered
  → blogger_draft
  → approved
  → published
```

자동화 경로는 `blogger_draft`에서 멈추는 것을 기본값으로 한다. 공개 게시에는 별도의 명시적 요청과 사람이 확인한 승인 상태가 필요하다.

기존 `google_side_job`을 재사용할 경우 게시 함수의 이름과 동작을 먼저 정리해야 한다. 현재 `publish_private`라는 이름의 함수가 Blogger API에 `isDraft=false`를 전달하는 경로가 있으므로, 비공개 초안과 공개 게시를 기술적으로 분리해야 한다.

## 12. 인터페이스 선택

### 1순위: Codex 대화

긴 대화, 편집 지시, 시리즈 구성에 가장 적합하다. README에는 자연어 발행 요청 형식과 필요한 결과물을 명시한다.

### 2순위: 기존 Blogger 게시 기능

생성된 `NNN.html`을 기존 `google_side_job`의 Blogger 게시·승인 흐름으로 전달한다.

## 13. 보안·품질 제약

- API 키와 OAuth 토큰은 Git에 저장하지 않는다.
- 대화 원본에 포함된 개인정보와 비공개 정보를 게시 전 제거한다.
- 사용자와 AI의 역할을 독자가 혼동하지 않도록 표시한다.
- AI의 오류를 편집 없이 게시하지 않는다.
- 출처 URL, 확인 날짜, 편집 상태를 저장한다.
- 자동 게시보다 초안 등록을 기본으로 한다.
- 공개된 글의 URL과 회차 식별자를 임의로 변경하지 않는다.
- 페이지 자동 이동, 클릭 유도, 숨은 광고 영역을 사용하지 않는다.

## 14. 구현 전 결정 사항

다음 사항은 개발 전에 확정해야 한다.

1. 대화를 Codex에서 어떤 파일 형식으로 넘길 것인가
2. 원본 대화에 대한 보존 기간과 민감정보 제거 방식
3. 한 회차의 권장 길이와 시리즈 분할 기준
4. 사용자·AI 말풍선의 시각 디자인
5. Blogger 테마 또는 본문에 대화·미디어 CSS를 넣는 방식
6. 비공개 초안 등록 후 메타데이터를 확인하는 방식
7. 공개 승인 주체와 명령 형식
8. 출처가 없는 일반 대화와 최신 정보 대화를 어떻게 구분할 것인가

## 15. 기술 결론

첫 구현은 다음 범위가 가장 안전하다.

- Codex 대화에서 사용자가 발행 대상을 지정
- raw 대화를 `docs/content_hist/YYYYMMDD_topic.md`에 저장
- 질문·답변·요약·표·이미지·YouTube·출처를 `contents/YYYY/MM/topic/NNN.md`에 누적
- CSS 기반 말풍선·미디어 HTML 생성
- Blogger 비공개 초안 등록
- Blogger 화면에서 링크·레이아웃을 확인한 뒤 사람 승인 후 공개

상시 서버, 실시간 Slack 이벤트 서버, 다중 사용자 계정은 첫 단계에 포함하지 않는다. 자동 스크롤과 TTS는 말풍선·미디어 표시 이후 선택 기능으로 검토한다. 이 기능의 핵심 가치는 서버 기술이 아니라 대화의 편집 품질과 Blogger에서의 읽기 경험에 있다.
