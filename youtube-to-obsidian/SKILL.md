---
name: youtube-to-obsidian
description: Fetches YouTube subtitles/transcripts and converts them into a structured Obsidian Markdown note. Use when you need to summarize or archive YouTube videos as personal knowledge articles.
---

# YouTube to Obsidian Note Creator

This skill automates the process of extracting knowledge from YouTube videos and formatting it for Obsidian.

## Prerequisites

- `youtube-transcript-api` Python library must be installed: `pip install youtube-transcript-api`

## Workflow

1. **Extract Transcript**:
   - Extract the video ID from the URL.
   - Run the script: `python scripts/get_transcript.py <URL>`
   - If the script returns an error about the library missing, inform the user to install it.

2. **Generate Knowledge Article**:
   - Use the raw transcript to generate a structured summary, key points, and detailed notes.
   - If possible, fetch the video title and channel name using `web_fetch` or generic search tools.

3. **Apply Template**:
   - Use `references/obsidian_template.md` as the structural guide.
   - Replace placeholders (`{{TITLE}}`, `{{URL}}`, `{{SUMMARY}}`, etc.) with the generated content.

4. **Save File**:
   - Save the final content as `<title-slug>.md`.

## Example Interaction

**User**: "Create an Obsidian note from https://www.youtube.com/watch?v=dQw4w9WgXcQ"

**Agent**:
1. (Executes `scripts/get_transcript.py`)
2. (Analyzes transcript text)
3. (Formats into template)
4. (Saves `note.md`)
5. **Agent**: "I've created your Obsidian note based on the video transcript. You can find it at `note.md`."
