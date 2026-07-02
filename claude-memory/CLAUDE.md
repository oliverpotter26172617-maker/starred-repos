# Global preferences

## Package management
- pnpm, never npm or yarn, unless the repo lockfile says otherwise
- Never upgrade major versions of dependencies without asking

## Code style
- TypeScript strict mode wherever TS is used
- Named exports, not default exports
- No commented-out code left in commits

## Workflow
- Plan before non-trivial changes; show the plan for anything touching more than 3 files
- Never force push. Never commit directly to main; use a branch and describe the change
- Run the project's lint and test commands before declaring a task done
- If a migration or schema change is involved, show me the SQL before applying

## Communication
- Be direct. Flag risks and tradeoffs, don't just agree
- No em dashes in any written output
