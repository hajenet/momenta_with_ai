[CmdletBinding()]
param(
    [string]$WakeWord = ("{0}GPT" -f [char]0xCC57),
    [string]$SendCommand = (-join ([char]0xC624, [char]0xBC84)),
    [string]$StopCommand = (-join ([char]0xC2A4, [char]0xD1B1)),
    [string]$ExitCommand = (-join ([char]0xADF8, [char]0xB9CC)),
    [string]$Language = "ko-KR",
    [switch]$Diagnose
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Speech
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$script:State = "IDLE"
$script:LastCommandAt = [DateTime]::MinValue
$script:Shell = New-Object -ComObject WScript.Shell
$script:Root = [System.Windows.Automation.AutomationElement]::RootElement

function Write-State([string]$state, [string]$message) {
    $script:State = $state
    Write-Host ("[{0}] {1}" -f $state, $message)
}

function Get-TargetWindow {
    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Window)
    foreach ($window in $script:Root.FindAll([System.Windows.Automation.TreeScope]::Children, $condition)) {
        if ($window.Current.Name -match "ChatGPT|Codex") { return $window }
    }
    return $null
}

function Invoke-AccessibleButton([string[]]$Names) {
    $window = Get-TargetWindow
    if (-not $window) { Write-State "ERROR" "Target ChatGPT or Codex window not found."; return $false }
    try { $script:Shell.AppActivate($window.Current.ProcessId) | Out-Null } catch {}
    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Button)
    foreach ($button in $window.FindAll([System.Windows.Automation.TreeScope]::Descendants, $condition)) {
        $name = $button.Current.Name
        if ($Names | Where-Object { $name -and $name -match [regex]::Escape($_) }) {
            try {
                $pattern = $button.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
                $pattern.Invoke()
                Write-Host ("UIA Invoke: {0}" -f $name)
                return $true
            } catch { Write-Host ("UIA invoke failed: {0}" -f $name) }
        }
    }
    Write-State "ERROR" ("Accessible button not found: {0}" -f ($Names -join ", "))
    return $false
}

function Start-Voice {
    if (Invoke-AccessibleButton @("Voice", "Microphone", "Start voice")) {
        Write-State "LISTENING" "Voice started. Say the send command when finished."
    }
}

function Send-Voice {
    if (Invoke-AccessibleButton @("Send", "Submit")) {
        Write-State "IDLE" "Sent. Waiting for the wake word."
    }
}

function Stop-Voice {
    [void](Invoke-AccessibleButton @("Stop", "Cancel"))
    Write-State "IDLE" "Voice stopped."
}

function Handle-Transcript([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return }
    $now = Get-Date
    if (($now - $script:LastCommandAt).TotalMilliseconds -lt 1200) { return }
    $normalized = $text.Trim()
    if ($script:State -eq "IDLE" -and $normalized -match [regex]::Escape($WakeWord)) {
        $script:LastCommandAt = $now
        Start-Voice
    } elseif ($script:State -eq "LISTENING" -and $normalized -match [regex]::Escape($SendCommand)) {
        $script:LastCommandAt = $now
        Send-Voice
    } elseif ($normalized -match [regex]::Escape($StopCommand)) {
        $script:LastCommandAt = $now
        Stop-Voice
    } elseif ($normalized -match [regex]::Escape($ExitCommand)) {
        $script:LastCommandAt = $now
        Stop-Voice
    }
}

function Show-Diagnose {
    Write-Host "Installed speech cultures:"
    foreach ($info in [System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers()) {
        Write-Host ("- {0}: {1}" -f $info.Culture.Name, $info.Description)
    }
    $window = Get-TargetWindow
    if (-not $window) { Write-Host "Target ChatGPT or Codex window not found."; return }
    Write-Host ("Target window: {0}" -f $window.Current.Name)
    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Button)
    foreach ($button in $window.FindAll([System.Windows.Automation.TreeScope]::Descendants, $condition)) {
        Write-Host ("- {0}" -f $button.Current.Name)
    }
}

if ($Diagnose) { Show-Diagnose; exit 0 }

$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$installed = [System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers()
$selected = $installed | Where-Object { $_.Culture.Name -eq $Language } | Select-Object -First 1
if (-not $selected) {
    Write-State "ERROR" ("Speech recognizer not installed for {0}." -f $Language)
    exit 1
}
$recognizer.SelectVoice($selected.Name)
$recognizer.SetInputToDefaultAudioDevice()
$recognizer.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar))
$recognizer.add_SpeechRecognized({ param($sender, $event) Handle-Transcript $event.Result.Text })
Write-State "IDLE" ("Waiting for wake word: {0}" -f $WakeWord)
$recognizer.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)
try {
    while ($true) { Start-Sleep -Seconds 1 }
} finally {
    $recognizer.RecognizeAsyncCancel()
    $recognizer.Dispose()
}
