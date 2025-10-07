# Sample Project

This is a sample project demonstrating IDE Context Porter usage.

## Setup

1. Initialize canonical context:
   ```bash
   ide-context-porter init
   ```

2. Edit `ai/context/rules.md` with your project-specific AI instructions

3. Export to your IDE:
   ```bash
   # For Cursor
   ide-context-porter export --to cursor

   # For VS Code
   ide-context-porter export --to vscode

   # For Continue
   ide-context-porter export --to continue
   ```

## Converting Between IDEs

If you're switching from Cursor to VS Code:

```bash
ide-context-porter convert --from cursor --to vscode
```

## Validation

Check your canonical context is valid:

```bash
ide-context-porter validate
```
