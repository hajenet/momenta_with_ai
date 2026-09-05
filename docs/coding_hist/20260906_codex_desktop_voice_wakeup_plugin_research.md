# Codex Desktop Voice Wake-up Companion 조사 및 명명

- 작성일: 2026-09-06
- 조사 대상: Windows ChatGPT/Codex 데스크톱용 로컬 voice wake-up companion
- 조사 방식: 현재 저장소 문서·코드 검색 + 공개 공식 문서·GitHub README 검색

## 1. 최종 명칭

### 제품명

**Codex Desktop Voice Command Companion**

### 패키지 식별자

```text
codex-desktop-voice-command-companion
```

### 짧은 이름

```text
Codex Voice Companion
```

### 명칭을 이렇게 정한 이유

- `Codex Desktop`: VS Code 확장과 ChatGPT/Codex 데스크톱 대상을 구분한다.
- `Voice Command`: wake, send, stop 명령을 포함한다.
- `Companion`: 공식 Codex 내부 플러그인이나 비공개 Voice API가 아니라 외부 로컬 보조 프로그램임을 분명히 한다.
- `Wake-up`만 제품명에 넣으면 전송과 작업 취소 기능이 빠진 것처럼 보이므로 제품명에서는 제외하고 기능명으로 사용한다.

기능 설명에는 다음 표현을 사용한다.

```text
Codex Desktop Voice Wake-up Companion
Windows local companion for wake, send, and task-stop voice commands
```

## 2. 기본 명령과 상태

| 상태 | 허용 명령 | 동작 |
|---|---|---|
| `SLEEPING` | 사용자 wake 별칭, 예: `시리` | Codex Desktop Voice 시작 시도 |
| `ACTIVATING` | `고스톱` / `gostop` | 시작 절차 취소 및 대기 복귀 |
| `LISTENING` | `고고` / `gogo` | 발화 종료 후 전송 버튼 1회 실행 |
| `LISTENING` | `고스톱` / `gostop` | 녹음 취소, 전송하지 않음 |
| `SENDING` | `고스톱` / `gostop` | 전송 또는 후속 작업 취소 요청 |
| `WORKING` | `고스톱` / `gostop` | 현재 Codex 작업 취소 요청 |
| `ERROR` | wake 별칭, `고스톱` | 재시도 또는 안전한 대기 복귀 |

필수 내부 상태는 `SLEEPING → ACTIVATING → LISTENING → SENDING → WORKING`과 `CANCELING`, `ERROR`다. 명령 인식이 불확실하거나 버튼을 찾지 못하면 전송하지 않는 fail-closed를 기본으로 한다.

## 3. 현재 저장소 조사 결과

현재 저장소에는 이미 다음이 있다.

- `tools/보이스톡 코맨드.md`: 기존 `챗GPT/오버/스톱/그만` 명세
- `tools/voice-codex-vscode/`: VS Code webview 음성 패널 prototype
- `tools/plugins/voice-command-companion/`: Windows UI Automation companion scaffold
- `tools/voice-codex-vscode/voice-command-design.md`: `시리/고고/고스톱` 상태 설계

따라서 새 기능을 완전히 새로 만드는 것이 아니라, 기존 명세·VS Code prototype·companion scaffold의 명령 체계를 하나로 통합하는 작업이다.

## 4. 공개 자료 검색 결과

### 정확히 일치하는 구현

2026-09-06 기준으로 다음 조건을 모두 만족하는 공개 저장소는 확인하지 못했다.

```text
Windows + Codex/ChatGPT Desktop + 한국어 wake phrase
+ UI Automation + gogo 전송 + gostop Codex 작업 취소
```

### 가장 가까운 공개 저장소

[Fingolfin7/OkayCodex](https://github.com/Fingolfin7/OkayCodex)는 Windows tray에서 로컬 Windows Speech API로 wake phrase를 듣고, ChatGPT Desktop의 사용자가 설정한 Voice hotkey를 전송한다. 오디오를 외부 서비스에 보내거나 디스크에 저장하지 않는다고 README에 설명한다.

하지만 다음 기능은 없다.

- Voice/Send/Stop 버튼의 Windows UI Automation 탐색
- `gogo` 전송 명령
- `gostop`으로 현재 Codex 작업 취소
- ChatGPT가 단축키를 실제로 처리했는지 확인

[hyungchulc/voice-relay](https://github.com/hyungchulc/voice-relay)는 wake phrase, persistent task, stop, live progress를 다루지만 macOS 전용 공개 alpha이며, Windows UI Automation 구현의 직접 기반으로 사용하지 않는다.

OpenAI 공식 안내는 데스크톱 Codex에서 Voice가 작업 시작·중단·재지시를 지원한다고 설명하지만, 외부 companion이 사용할 공식 내부 Voice API나 버튼 자동화 계약을 제공한다는 의미는 아니다. [ChatGPT Work and Codex 공식 안내](https://help.openai.com/en/articles/20001275)

## 5. 보안 조사 기준

이번 조사에서는 공개 저장소를 clone하거나 실행하지 않았다. 다음 유형은 채택 대상에서 제외한다.

- API key를 코드나 설정에 직접 넣도록 요구하는 프로젝트
- 브라우저 로그인·쿠키·세션을 훔치거나 우회하는 방식
- 출처가 불명확한 prebuilt 실행 파일만 배포하는 프로젝트
- Codex/ChatGPT 내부 API를 역공학하거나 비공개 endpoint를 호출하는 프로젝트
- 관리자 권한, 보안 설정 변경, 원격 명령 실행을 기본으로 요구하는 프로젝트
- 코드와 권한 범위를 검토할 수 없는 설치 스크립트

참고 후보도 바이너리를 바로 설치하지 않고 소스, 라이선스, 권한, 네트워크 호출, 저장 데이터, 자동 실행 여부를 먼저 검토한다.

## 6. RAG형 설계 결론

정확한 공개 선례가 없으므로 다음 자료를 검색 근거로 결합했다.

1. 이 저장소의 `tools/보이스톡 코맨드.md`
2. 이 저장소의 `tools/voice-codex-vscode/extension.js`
3. 이 저장소의 `tools/plugins/voice-command-companion/scripts/companion.ps1`
4. 이 저장소의 `tools/voice-codex-vscode/voice-command-design.md`
5. Windows 공개 wake 유틸리티 OkayCodex의 로컬 인식·쿨다운·마이크 점유 방지 설계
6. OpenAI의 데스크톱 Work/Codex Voice 동작 설명

검색 결과를 종합하면 최종 구현 방향은 다음과 같다.

```text
로컬 wake detection
  → Codex Desktop Voice 시작
  → LISTENING
  → gogo 확인
  → UI Automation Send
  → WORKING 상태 표시
  → gostop 시 UI Automation Stop/취소
```

핵심은 공개 저장소를 그대로 가져오는 것이 아니라, 로컬 음성 인식·상태 머신·쿨다운·fail-closed·UI Automation 진단을 각각 검증 가능한 작은 계층으로 구현하는 것이다.
