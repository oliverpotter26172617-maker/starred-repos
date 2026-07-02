# Stack: Power Platform

## Solutions and ALM

- All customizations live in solutions with a consistent publisher prefix; nothing built naked in the default environment
- Unmanaged solutions in dev only; managed solutions in test and production
- Connection references and environment variables in solutions; never hardcode connection details, environment URLs, or IDs
- Export/unpack solutions with pac cli into source control; deploys via pipelines, not manual imports

## Power Automate

- Every flow has error handling: scoped try/catch pattern using configure-run-after
- Trigger conditions on every trigger that could loop or fire on its own updates
- Service accounts with least privilege for production flows, not personal accounts
- Name actions descriptively; a flow should be readable without opening each step

## Power Apps (canvas)

- Delegable queries only against large data sources; treat delegation warnings as errors
- Shared logic in App.Formulas (named formulas), not duplicated across control properties
- Dataverse over SharePoint lists for anything relational or beyond trivial scale

## Documentation

- Each app and flow documents its connectors, data sources, and owner
- Environment strategy (dev/test/prod) written down per project

## References

- github/awesome-copilot (https://github.com/github/awesome-copilot): community instruction files for Microsoft stacks; this draft is from general knowledge, verify and enrich against the live repo's Power Platform / Dataverse instruction files
