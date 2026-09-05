# Desktop Codex Voice Companion 명령어 설계

## 결론

기본 명령어는 다음 세 가지로 고정한다.

| 명령어 | 별칭 | 동작 | 허용 상태 |
|---|---|---|---|
| 깨우기 | 사용자 설정 별칭, 예: `시리` | Codex 창을 찾고 Voice/마이크 시작 | `SLEEPING`, `ERROR` |
| 전송 | `고고`, `gogo` | 현재 발화를 끝내고 전송 버튼을 한 번 실행 | `LISTENING`, `READY_TO_SEND` |
| 작업중지 | `고스톱`, `gostop` | 녹음·전송·실행 중인 작업을 취소하고 안전 상태로 복귀 | `ACTIVATING`, `LISTENING`, `SENDING`, `WORKING` |

## 필수 상태

```text
SLEEPING
  └─ wake alias → ACTIVATING
ACTIVATING
  ├─ Voice 버튼 확인 → LISTENING
  ├─ timeout/failure → ERROR
  └─ gostop → SLEEPING
LISTENING
  ├─ gogo → SENDING
  ├─ gostop → CANCELING → SLEEPING
  └─ timeout → SLEEPING 또는 ERROR
SENDING
  ├─ 전송 확인 → WORKING
  ├─ gostop → CANCELING
  └─ failure → ERROR
WORKING
  ├─ gostop → CANCELING
  ├─ 작업 완료 → SLEEPING
  └─ 상태/진행 이벤트 → WORKING
CANCELING
  └─ 중지 확인 → SLEEPING
ERROR
  ├─ wake alias → ACTIVATING
  └─ gostop → SLEEPING
```

## 왜 추가 상태가 필요한가

- `SLEEPING`: 대기 중에는 깨우기 별칭만 인식해야 오인 전송을 막을 수 있다.
- `ACTIVATING`: Voice 버튼 탐색·창 활성화가 끝나기 전에 명령을 중복 실행하지 않는다.
- `LISTENING`: 일반 질문과 `gogo`/`gostop`을 구분한다.
- `SENDING`: 전송 버튼을 한 번만 누르고 중복 전송을 막는다.
- `WORKING`: 음성 입력 종료와 Codex 작업 실행을 분리한다. `gostop`은 이 상태에서 현재 Codex 작업 취소를 요청해야 한다.
- `CANCELING`: 취소 요청이 실제로 반영되었는지 확인하기 전에는 대기 상태로 거짓 복귀하지 않는다.
- `ERROR`: 버튼·창·마이크를 찾지 못했을 때 안전하게 멈춘다.

## 권장 보조 명령어

세 가지 기본 명령어 외에 다음은 실제 사용에 필요한 안전 명령어다.

| 명령어 | 별칭 | 동작 |
|---|---|---|
| 대기 | `잠자기`, `대기` | Voice를 종료하거나 companion을 대기 상태로 전환 |
| 상태 | `상태`, `지금 뭐해` | 현재 상태만 음성·트레이로 알림 |
| 도움말 | `도움말`, `명령어` | 사용 가능한 명령을 알림 |
| 다시듣기 | `다시`, `재시작` | 현재 입력을 버리고 LISTENING 재시작 |

보조 명령어는 1차 구현에서 `상태`와 `잠자기`부터 넣는 것을 권장한다. `gostop`은 모든 활성 상태에서 작동하는 비상 정지 명령으로 유지한다.

## 인식·안전 규칙

- `gogo`와 `gostop`은 발화 끝부분의 독립된 명령으로만 인정한다. 예: “고고마켓”은 전송 명령이 아니다.
- 한 번 인식한 명령은 `commandCooldownMs` 동안 다시 처리하지 않는다.
- 전송은 `gogo` 인식, 현재 입력 존재, Voice 상태 확인의 세 조건이 모두 맞을 때만 실행한다.
- `gostop`은 취소 대상이 불명확하거나 UI 상태를 읽지 못하면 fail-closed로 멈추고 사용자에게 상태를 알린다.
- 음성 원본·질문 전문·토큰·인증정보를 로그에 저장하지 않는다.
- 마이크를 이미 Codex가 점유한 상태에서는 wake를 재실행하지 않는다.

## 현재 코드와의 차이

- `tools/보이스톡 코맨드.md`는 기존에 `챗GPT/오버/스톱/그만`을 정의했다.
- `tools/voice-codex-vscode/extension.js`는 `올려/보내/전송`, `스톱/중지/멈춰`, `그만/종료`를 인식한다.
- 이 문서는 사용자가 정한 `시리` 별칭, `고고`, `고스톱`을 새 기본 설계로 정리한 것이다. 실제 동작 변경은 상태 머신과 UI Automation 진단을 함께 검증한 뒤 적용한다.

## 공개 구현 조사 결과

가장 가까운 Windows 공개 저장소는 [Fingolfin7/OkayCodex](https://github.com/Fingolfin7/OkayCodex)다. 로컬 Windows Speech API로 정확한 wake phrase를 듣고, ChatGPT Desktop에서 사용자가 설정한 Voice hotkey를 보낸다. 오디오를 외부 서비스로 보내거나 디스크에 저장하지 않는다고 README에 명시되어 있다.

하지만 이 저장소는 다음을 제공하지 않는다.

- UI Automation으로 Voice/Send/Stop 버튼을 찾는 기능
- `gogo` 전송 커맨드
- `gostop` 작업 취소 커맨드
- ChatGPT가 실제로 명령을 받았는지 확인하는 기능

따라서 코드를 가져오기보다 상태·쿨다운·fail-closed 원칙만 참고한다. 공개 바이너리 설치나 자동 실행은 사용하지 않고, 필요하면 소스와 라이선스를 먼저 검토한다.
