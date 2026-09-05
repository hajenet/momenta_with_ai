"""Render the project's conversation Markdown as Blogger-safe HTML.

This tool has no third-party dependency. It produces scoped, semantic HTML
that can be passed to the existing google_side_job Blogger publisher after
the publisher's draft flag is corrected.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


CSS = """
.conversation-post{max-width:760px;margin:0 auto;font-family:inherit;line-height:1.7}
.conversation-post .series-header{margin-bottom:2rem}
.conversation-post .series-name{color:#6b7280;font-size:.9rem}
.conversation-post .chat-row{display:flex;margin:1rem 0}
.conversation-post .chat-row--user{justify-content:flex-end}
.conversation-post .chat-row--assistant{justify-content:flex-start}
.conversation-post .chat-bubble{max-width:78%;padding:.8rem 1rem;border-radius:1.1rem;box-sizing:border-box}
.conversation-post .chat-bubble--user{background:#e8f0fe;border-bottom-right-radius:.25rem}
.conversation-post .chat-bubble--assistant{background:#f1f3f5;border-bottom-left-radius:.25rem}
.conversation-post .chat-label{display:block;margin-bottom:.35rem;font-size:.78rem;font-weight:700;color:#6b7280}
.conversation-post .editor-note{margin:1.5rem 0;padding:1rem;border-left:4px solid #9ca3af;background:#f8fafc}
.conversation-post table{width:100%;border-collapse:collapse;margin:1rem 0}
.conversation-post th,.conversation-post td{border:1px solid #d1d5db;padding:.5rem;text-align:left}
.conversation-post img{max-width:100%;height:auto}
@media (max-width:600px){.conversation-post .chat-bubble{max-width:90%}}
""".strip()


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(
        r"!\[([^\]]+)\]\((https://[^)]+)\)",
        lambda match: f'<img src="{html.escape(match.group(2), quote=True)}" alt="{html.escape(match.group(1), quote=True)}">',
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^]]+)\]\((https://[^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(
        r"(?<![=\"'/>])(https://[^\s<]+)",
        lambda match: f'<a href="{html.escape(match.group(1), quote=True)}">{match.group(1)}</a>',
        escaped,
    )
    return escaped


def render(markdown: str) -> str:
    lines = markdown.splitlines()
    title = ""
    body: list[str] = []
    current_role: str | None = None
    current: list[str] = []
    in_list = False
    table_rows: list[list[str]] = []

    def close_chat() -> None:
        nonlocal current, current_role
        if current_role and current:
            text = "<br>".join(inline(line) for line in current)
            label = "질문" if current_role == "user" else "AI 답변"
            body.append(
                f'<div class="chat-row chat-row--{current_role}">'
                f'<div class="chat-bubble chat-bubble--{current_role}"><span class="chat-label">{label}</span><p>{text}</p></div></div>'
            )
        current = []
        current_role = None

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    def close_table() -> None:
        nonlocal table_rows
        if table_rows:
            header, *rows = table_rows
            table = ["<table><thead><tr>"]
            table.extend(f"<th>{inline(cell.strip())}</th>" for cell in header)
            table.append("</tr></thead><tbody>")
            for row in rows:
                table.append("<tr>" + "".join(f"<td>{inline(cell.strip())}</td>" for cell in row) + "</tr>")
            table.append("</tbody></table>")
            body.extend(table)
        table_rows = []

    for raw in lines:
        line = raw.strip()
        if line == "### 사용자 질문":
            close_chat(); close_list(); close_table(); current_role = "user"; continue
        if line == "### AI 답변":
            close_chat(); close_list(); close_table(); current_role = "assistant"; continue
        if current_role:
            if line.startswith("### ") or line.startswith("## ") or line == "## 출처":
                close_chat()
            elif line:
                current.append(line)
                continue
        if not line:
            close_list(); close_table(); continue
        if line == ">":
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            close_list(); close_table()
            level = len(heading.group(1))
            value = inline(heading.group(2))
            if level == 1 and not title:
                title = heading.group(2)
                continue
            body.append(f"<h{level}>{value}</h{level}>")
            continue
        if line.startswith("> "):
            close_list(); close_table(); body.append(f"<aside class=\"editor-note\">{inline(line[2:])}</aside>"); continue
        if line.startswith("|") and line.endswith("|"):
            close_list()
            cells = [cell for cell in line.strip("|").split("|")]
            if not all(set(cell.strip()) <= {"-", ":", " "} for cell in cells):
                table_rows.append(cells)
            continue
        if line.startswith("- "):
            close_table()
            if not in_list:
                body.append("<ul>"); in_list = True
            body.append(f"<li>{inline(line[2:])}</li>")
            continue
        close_list(); close_table()
        body.append(f"<p>{inline(line)}</p>")
    close_chat(); close_list(); close_table()
    header = f'<header class="series-header"><h1>{inline(title)}</h1></header>' if title else ""
    return f'<style>{CSS}</style><article class="conversation-post">{header}{"".join(body)}</article>'


def main() -> None:
    parser = argparse.ArgumentParser(description="Render conversation Markdown to Blogger HTML")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.input.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Rendered {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
