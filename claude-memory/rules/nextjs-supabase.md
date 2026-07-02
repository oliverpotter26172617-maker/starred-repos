# Stack: Next.js + Supabase

- Next.js App Router, TypeScript strict
- Supabase (Postgres) via the JS client; all queries respect RLS
- RLS: every new table gets policies written and tested before use. Never disable RLS to "get something working"
- Migrations live in supabase/migrations and are the only way schema changes happen. No dashboard-only changes
- Styling: Tailwind, no CSS modules
- Env vars documented in .env.example; never hardcode keys
- API calls go through a lib/api layer, never inline fetch in components
