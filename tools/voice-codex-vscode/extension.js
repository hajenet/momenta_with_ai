const vscode = require("vscode");

function activate(context) {
  const provider = new VoicePanelProvider();
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("voiceCodex.panel", provider),
    vscode.commands.registerCommand("voiceCodex.open", () =>
      vscode.commands.executeCommand("workbench.view.extension.voiceCodex")
    ),
    vscode.commands.registerCommand("voiceCodex.start", () => provider.post({ type: "start" })),
    vscode.commands.registerCommand("voiceCodex.stop", () => provider.post({ type: "stop" }))
  );
}

class VoicePanelProvider {
  constructor() {
    this.view = undefined;
  }

  resolveWebviewView(view) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = this.html(view.webview);
    view.webview.onDidReceiveMessage(async (message) => {
      if (message.type === "send") await this.sendToChat(message.text);
    });
  }

  post(message) {
    if (this.view) this.view.webview.postMessage(message);
    else vscode.window.showInformationMessage("먼저 Voice Codex 패널을 여세요.");
  }

  async sendToChat(text) {
    const prompt = String(text || "").trim();
    if (!prompt) return;
    try {
      await vscode.commands.executeCommand("workbench.action.chat.open", { query: prompt });
    } catch (_) {
      await vscode.env.clipboard.writeText(prompt);
      vscode.window.showInformationMessage("음성 문장을 클립보드에 복사했습니다. Codex 입력창에 붙여 넣으세요.");
    }
  }

  html(webview) {
    const nonce = String(Date.now());
    const lines = [
      "<!doctype html>",
      "<html lang=\"ko\"><head><meta charset=\"UTF-8\">",
      "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-" + nonce + "'\">",
      "<style>body{font-family:var(--vscode-font-family);color:var(--vscode-foreground);padding:10px}button{width:100%;margin:4px 0;padding:7px;color:var(--vscode-button-foreground);background:var(--vscode-button-background);border:0;border-radius:3px}#status{margin:10px 0;color:var(--vscode-descriptionForeground)}#transcript{min-height:90px;white-space:pre-wrap;border:1px solid var(--vscode-input-border);padding:8px}</style>",
      "</head><body>",
      "<button id=\"start\">듣기 시작</button><button id=\"stop\">스톱</button>",
      "<div id=\"status\">대기 중</div><div id=\"transcript\"></div>",
      "<button id=\"send\">올려 (Codex로 보내기)</button>",
      "<small>올려: 전송 · 스톱: 중지 · 그만: 초기화</small>",
      "<script nonce=\"" + nonce + "\">",
      "const vscode=acquireVsCodeApi();const SR=window.SpeechRecognition||window.webkitSpeechRecognition;const status=document.getElementById('status');const box=document.getElementById('transcript');let recognition;let finalText='';",
      "function stop(){if(recognition)recognition.stop();status.textContent='중지됨'}",
      "function send(){const text=finalText.trim();if(!text)return;vscode.postMessage({type:'send',text});status.textContent='Codex로 전송했습니다.';finalText='';box.textContent=''}",
      "function start(){if(!SR){status.textContent='이 VS Code 환경은 음성 인식을 지원하지 않습니다.';return}recognition=new SR();recognition.lang='ko-KR';recognition.continuous=true;recognition.interimResults=true;recognition.onstart=()=>status.textContent='듣는 중…';recognition.onerror=e=>status.textContent='음성 인식 오류: '+e.error;recognition.onresult=e=>{let interim='';for(let i=e.resultIndex;i<e.results.length;i++){const value=e.results[i][0].transcript.trim();if(e.results[i].isFinal)finalText+=value+' ';else interim+=value}const all=(finalText+interim).trim();box.textContent=all;if(/스톱|중지|멈춰/.test(all)){stop()}if(/그만|종료/.test(all)){stop();finalText='';box.textContent=''}if(/올려|보내|전송/.test(all)){finalText=all.replace(/올려|보내|전송/g,'').trim();send()}};recognition.start()}",
      "document.getElementById('start').onclick=start;document.getElementById('stop').onclick=stop;document.getElementById('send').onclick=send;window.addEventListener('message',e=>{if(e.data.type==='start')start();if(e.data.type==='stop')stop()});",
      "</script></body></html>"
    ];
    return lines.join("");
  }
}

function deactivate() {}
module.exports = { activate, deactivate };
