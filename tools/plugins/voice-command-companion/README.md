# Voice Command Companion

Windows용 로컬 companion 플러그인입니다. 웨이크워드와 음성 커맨드를 감지한 뒤 ChatGPT/Codex 데스크톱의 접근성 버튼을 Windows UI Automation으로 실행합니다.

## 실행

PowerShell에서 다음을 실행합니다.

    powershell -ExecutionPolicy Bypass -File .\scripts\companion.ps1

진단:

    powershell -ExecutionPolicy Bypass -File .\scripts\companion.ps1 -Diagnose

기본 커맨드는 챗GPT, 오버, 스톱, 그만입니다. 대상 앱의 접근성 버튼 이름이 다르면 companion.ps1의 버튼 이름 목록을 추가해야 합니다.

이 구성은 ChatGPT/Codex 데스크톱의 공식 내부 Voice API를 사용하지 않습니다. UI Automation을 사용하므로 창 크기와 위치가 바뀌어도 요소를 다시 찾지만, 앱의 접근성 이름이 바뀌면 진단이 필요합니다.
