# Stack: Next.js + Supabase

- Next.js App Router, TypeScript strict
- Supabase (Postgres) via the JS client; all queries respect RLS
- RLS: every new table gets policies written and tested before use. Never disable RLS to "get something working"
- Migrations live in supabase/migrations and are the only way schema changes happen. No dashboard-only changes
- Styling: Tailwind, no CSS modules
- Env vars documented in .env.example; never hardcode keys
- API calls go through a lib/api layer, never inline fetch in components

## Components and data flow

- Server Components by default; add "use client" only for state, effects, or browser APIs
- Data fetching happens in Server Components, route handlers, or Server Actions, not in client components
- Mutations via Server Actions; call revalidatePath/revalidateTag after writes
- Every route segment that fetches data gets loading.tsx and error.tsx
- Use next/image for images, next/link for navigation; no raw img or a tags for internal routes

## Supabase specifics

- Use @supabase/ssr for cookie-based auth in the App Router; the deprecated auth-helpers package is not allowed
- The service-role key never reaches client code or NEXT_PUBLIC_ vars; server-side only
- Generate types with supabase gen types typescript after every migration; queries are typed, no untyped .from() calls
- Auth checks in middleware or layouts, plus RLS as the real enforcement layer; UI checks are convenience, not security

## Validation and safety

- Validate at every boundary with zod: form input, route handler params, webhook payloads
- NEXT_PUBLIC_ prefix means public; anything secret stays unprefixed and server-side

## References

- OpenCut (https://github.com/OpenCut-app/OpenCut): large production App Router codebase; consult for project structure and API-layer patterns
- Sections below the first were drafted from general knowledge of PatrickJS/awesome-cursorrules Next.js+Supabase rules; verify against the live repo before treating as final
