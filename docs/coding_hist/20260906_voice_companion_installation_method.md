# Voice Command Companion 설치방법

## 핵심 확인

- 컴패니언 PowerShell 스크립트와 실행 경로는 정상이다.
- 현재 Windows에는 한국어 Text-to-Speech(TTS)만 설치되어 있다.
- TTS는 컴퓨터가 글을 읽어주는 기능이며, 음성을 듣고 인식하는 기능이 아니다.
- 현재 확인된 상태:

      Language.TextToSpeech~~~ko-KR~0.0.1.0  Installed

- 한국어 음성 인식에 필요한 다음 항목은 확인되지 않았다.

      Language.Speech~~~ko-KR~0.0.1.0

- 따라서 현재 상태에서는 컴패니언이 챗GPT, 오버, 스톱 음성 명령을 인식할 수 없다.

## Windows 설정 설치 방법

1. Windows 설정을 연다.
2. 시간 및 언어 → 언어로 이동한다.
3. 설치된 한국어의 언어 옵션을 연다.
4. 음성 인식 또는 음성 항목이 있으면 다운로드·설치한다.
5. 설치 후 Windows를 재시작한다.

음성 항목 자체가 없거나 비활성화되어 있으면 현재 Windows 이미지에서 한국어 오프라인 음성 인식 구성 요소를 제공하지 않는 상태일 수 있다.

## PowerShell 확인 방법

관리자 PowerShell에서 다음 명령을 실행한다. PS ...> 프롬프트와 출력 결과는 입력하지 않는다.

    Get-WindowsCapability -Online | Where-Object { $_.Name -match "Speech|ko-KR" } | Select-Object Name, State

정상적으로 사용할 수 있으려면 다음 항목이 Installed여야 한다.

    Language.Speech~~~ko-KR~0.0.1.0

설치 항목이 제공되는 Windows 환경에서는 관리자 PowerShell에서 다음 명령을 시도할 수 있다.

    Add-WindowsCapability -Online -Name "Language.Speech~~~ko-KR~0.0.1.0"

명령이 Online : True, RestartNeeded : False만 출력하고 해당 항목이 목록에 나타나지 않으면 실제 설치가 된 것이 아니다.

## 컴패니언 실행 방법

한국어 음성 인식 설치가 확인된 뒤 일반 PowerShell에서 실행한다.

    cd "E:\Users\kimsong\projects\momenta_with_ai"
    powershell -ExecutionPolicy Bypass -File ".\tools\plugins\voice-command-companion\scripts\companion.ps1"

진단만 실행하려면 다음을 사용한다.

    powershell -ExecutionPolicy Bypass -File ".\tools\plugins\voice-command-companion\scripts\companion.ps1" -Diagnose

## 현재 환경의 결론

현재 확인된 Windows 환경에서는 한국어 TTS만 설치되어 있고 한국어 Speech 항목이 제공되지 않았다. 따라서 Windows 기본 System.Speech 기반 컴패니언은 아직 한국어 음성 명령을 실행할 수 없다. Windows 기능 설치가 불가능하면 Whisper 또는 Vosk 같은 별도 한국어 음성 인식 엔진으로 컴패니언을 수정해야 한다.
