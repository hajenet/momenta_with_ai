---
name: voice-command-companion
description: Operate the local Voice Command Companion for ChatGPT/Codex desktop voice control.
---

# Voice Command Companion

Use the companion when the user asks to start, stop, or diagnose hands-free voice control for the ChatGPT/Codex desktop app.

The companion is local Windows automation. It listens for a configurable wake word, activates the target desktop window, and invokes accessible Voice or Send buttons through Windows UI Automation. It does not claim access to an internal OpenAI desktop Voice API.

Run the companion from the plugin scripts directory with PowerShell:

    powershell -ExecutionPolicy Bypass -File .\companion.ps1

Use the Diagnose switch to list installed speech cultures and accessible buttons found in the foreground window.
