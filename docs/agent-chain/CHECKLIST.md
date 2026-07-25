# Verification and audit checklist

Use this for every `*a-verify*` / `*a-audit*` / `99` / `META` run. Write evidence to `docs/agent-chain/audits/<phase>-audit.md`.

## Per-phase Done-when check

- [ ] Diff against the implementation phase **Done when** checklist
- [ ] All **Steps** verify commands re-run and recorded
- [ ] New public functions / routes have tests
- [ ] CI-equivalent local commands pass (backend + frontend as applicable)
- [ ] No secrets committed
- [ ] `HANDOFF.md` updated for the next phase

## Citations

- [ ] Every new grant/agency/tax claim links a URL listed in `SOURCES.md` or added there after live fetch
- [ ] Spot-check: HTTP HEAD or GET succeeds for cited URLs
- [ ] No `UNVERIFIED` items appear in user-facing README/UI copy

## Claims vs reality

- [ ] README “Supported grant sources” matches agencies actually present in `data/all_grants.json` (or successor store)
- [ ] Home/About/marketing copy does not promise features that are stubs (scrape, deadline alerts, LLM, accounts) unless implemented
- [ ] Frontend mock fallback is documented or removed once backend is reliable

## Security / hygiene

- [ ] CORS and auth appropriate for the phase
- [ ] Scrapers respect rate limits; User-Agent identifies the tool
- [ ] No API keys in git history of this PR

## Chain-level (META / 99)

- [ ] `phases.json` lists every prompt file and dependency edge
- [ ] Every implement phase has a paired verify/audit phase
- [ ] Roadmap items in root `README.md` map to at least one phase
- [ ] Automation wiring docs match prompt paths
