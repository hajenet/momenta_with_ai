# Voice Command Companion PowerShell 실행 기록

- 실행일: 2026-09-06
- 대상: tools/plugins/voice-command-companion/scripts/companion.ps1
- 목적: -Diagnose 옵션으로 음성 인식 문화권과 ChatGPT/Codex UI Automation 버튼 확인

## 1. 최초 실행 결과

현재 PowerShell 위치가 C:\Windows\System32인 상태에서 다음 상대경로를 실행하려 했다.

    powershell -ExecutionPolicy Bypass -File .\tools\plugins\voice-command-companion\scripts\companion.ps1 -Diagnose

결과:

    -File 매개 변수에 대한 인수 '.\tools\plugins\voice-command-companion\scripts\companion.ps1'이(가) 없습니다.
    기존 '.ps1' 파일의 경로를 -File 매개 변수의 인수로 제공하십시오.

원인:

- .\tools\...는 현재 폴더인 C:\Windows\System32를 기준으로 해석된다.
- 프로젝트의 실제 위치는 E:\Users\kimsong\projects\momenta_with_ai이다.

## 2. 붙여넣기 오류

이후 PowerShell 프롬프트(PS system32>), 기존 오류 메시지, Markdown 코드 블록 표시까지 명령 입력창에 함께 붙여넣었다.

그 결과 다음과 같은 부수 오류가 발생했다.

- Get-Process : 'powershell' 인수를 허용하는 위치 매개 변수를 찾을 수 없습니다.
- Windows, Copyright, 새로운 등을 명령으로 해석하려는 오류
- 프롬프트 문자열 PS system32>를 프로세스 이름으로 해석하려는 오류

이 내용은 스크립트 오류가 아니라 터미널에 출력 내용을 다시 명령으로 입력한 결과다.

## 3. 확인된 올바른 실행 방법

절대경로를 사용하면 현재 위치와 관계없이 실행할 수 있다.

    powershell -ExecutionPolicy Bypass -File "E:\Users\kimsong\projects\momenta_with_ai\tools\plugins\voice-command-companion\scripts\companion.ps1" -Diagnose

또는 먼저 프로젝트 폴더로 이동한다.

    cd "E:\Users\kimsong\projects\momenta_with_ai"
    powershell -ExecutionPolicy Bypass -File ".\tools\plugins\voice-command-companion\scripts\companion.ps1" -Diagnose

## 4. 파일 존재 확인

프로젝트 경로의 스크립트 파일은 존재하는 것으로 확인했다.

    E:\Users\kimsong\projects\momenta_with_ai\tools\plugins\voice-command-companion\scripts\companion.ps1

다음 실행부터는 PS system32>를 입력하지 않고, powershell부터 시작하는 명령 한 줄만 실행한다.

## 5. 재실행 결과

프로젝트 폴더로 이동한 뒤 절대경로 기준의 정상적인 상대경로 명령으로 컴패니언을 다시 실행했다.

    cd "E:\Users\kimsong\projects\momenta_with_ai"
    powershell -ExecutionPolicy Bypass -File ".\tools\plugins\voice-command-companion\scripts\companion.ps1"

출력:

    APeX TDD Environment: Red color disabled.
    [ERROR] Speech recognizer not installed for ko-KR.

판정:

- PowerShell 명령과 스크립트 경로는 정상이다.
- APeX TDD 메시지는 컴패니언 오류와 무관하다.
- Windows의 ko-KR 음성 인식 구성 요소가 여전히 설치되지 않아 음성 대기 상태로 진입하지 못했다.
- 한국어 음성 기능을 사용하려면 Windows 설정에서 한국어 음성 인식 구성 요소를 먼저 설치해야 한다.
