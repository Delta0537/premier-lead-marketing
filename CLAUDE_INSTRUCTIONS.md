# Instructions for Working with Claude

## Preventing Lost Work

### Rule 1: Save Important Outputs Immediately
When Claude generates any of these, immediately ask: "Save that to a file"
- Bot prompts/personalities
- Configuration scripts
- Strategy documents
- Implementation plans
- Code snippets

### Rule 2: Commit Frequently
After every significant piece of work:
```
"Commit this to git with message: [describe what was done]"
```

### Rule 3: Update Session Log
At the end of each session, tell Claude:
```
"Update SESSION_LOG.md with what we accomplished today"
```

### Rule 4: Request Status Files
For complex projects, ask:
```
"Create a [PROJECT_NAME]_STATUS.md file tracking this project"
```

---

## Quick Phrases to Use

| Situation | Say This |
|-----------|----------|
| Claude generates a prompt | "Save that prompt to a file in the appropriate folder" |
| Completing a task | "Commit these changes to git" |
| Ending a session | "Update the session log and commit" |
| Starting a new session | "Read SESSION_LOG.md to see where we left off" |
| Complex bot config | "Export the full bot configuration to a markdown file" |

---

## Folder Structure for Saving Work

```
C:\Users\dezel\DigitalMarketing\
├── Tools_Scripts\AI Agents\     <- Bot configs, prompts, scripts
├── Business_Operations\PLM_Core\ <- Strategy docs, implementation guides
├── Active_Projects\             <- Current work in progress
├── SESSION_LOG.md               <- Track all sessions
└── CLAUDE_INSTRUCTIONS.md       <- This file
```

---

## Recovery Steps (If Session Fails)

1. Check git history: `git log --oneline -20`
2. Read SESSION_LOG.md
3. Search for recent files: Look in folders above
4. GHL configs are saved in GHL itself (check the platform)
