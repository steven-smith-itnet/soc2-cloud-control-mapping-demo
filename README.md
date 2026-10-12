# SOC 2 on AWS: service readiness, control testing and evidence engineering

An end-to-end teaching case study for a fictional AWS SaaS service, **Northstar Workspace**. Start with customer commitments, define the system, design risk-based controls, validate evidence flows, operate controls, remediate findings and support an independent examination.

**This is a work sample.** All organizations, records, findings and management deliverables are illustrative. No customer data, production deployment, issued CPA report or successful SOC 2 examination is represented. The public artifacts are synthetic. The optional live collector is read-only and intentionally narrow.

- [Interactive project](https://steven-smith-itnet.github.io/soc2-cloud-control-mapping-demo/)
- [Bright Ridge project page](https://www.brightridgellc.com/steven-smith-itnet/projects/soc2-cloud)

## What you can examine

| Deliverable | What it demonstrates |
|---|---|
| [34 beginner definitions](docs/01-foundations.md) | SOC 2, report types, criteria, populations, evidence, AWS services and key audit terms |
| [System and scope](docs/02-system-scope.md) | Commitments, six-account AWS boundary, two regions, people/procedures/data, carve-out and customer responsibilities |
| [36-control catalog](docs/04-control-catalog.md) | Risks, operators, frequency, populations, implementation, design and operating tests, artifacts and limits |
| [Risk and control design](docs/03-risk-control-design.md) | Traceability from commitment to risk to control to test to finding |
| [Runnable engineering lab](docs/05-automation-lab.md) | Four executable assertion types, immutable commit joins, access removal, Config evidence and recovery objectives |
| [Evidence and testing](docs/06-evidence-and-testing.md) | Source validation, population reconciliation, period coverage, provenance, restricted custody and hash verification |
| [Findings and corrective actions](docs/07-findings-and-remediation.md) | Five worked findings, root causes, owner actions, independent retests and executive/engineering communication |
| [Examination support](docs/08-examination-support.md) | PBC requests, description/assertion scaffolds, report anatomy, provider report review and CPA boundaries |
| [AWS operations runbooks](docs/09-aws-runbooks.md) | Identity, logging canaries, incident handling, releases and disaster recovery with failure-path validation |
| [Category extensions](docs/10-category-extensions.md) | Confidentiality versus Privacy, Processing Integrity, cautious common-control reuse |
| [Learner workshop](docs/11-workshop.md) | Exercises with worked reasoning and acceptance criteria |
| [Source register](docs/12-sources.md) | AICPA and official AWS references, reviewed 2026-10-03 |

The selected examination scenario includes **Security, Availability and Confidentiality**. CC1–CC9 are Common Criteria groupings, not nine categories. Processing Integrity and Privacy are optional learning extensions and are excluded from the scenario. Catalog mappings show contributions to criteria, not proof of criterion satisfaction.

## Run the offline lab

Python 3.10+ and the standard library are sufficient. No AWS account, credentials or paid services are required.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/evaluate.py --as-of 2026-09-30T15:00:00Z --out evidence/local-run
python3 scripts/verify_evidence.py evidence/local-run
```

Choose a **new output directory** for each run. Existing evidence is never overwritten. The fixed `--as-of` time deliberately matches the synthetic fixture; real runs use the current UTC time. The fixture yields **21 expected items, 20 source records, 5 PASS, 8 FAIL, 7 UNKNOWN and 1 approved NOT_APPLICABLE**. The dashboard’s 25% is the narrow-assertion pass rate, not a SOC 2 readiness or compliance score. UNKNOWN stays in the denominator. `--strict` writes artifacts and exits 2 if FAIL or UNKNOWN is present.

See [the live lab](docs/05-automation-lab.md) for optional AWS Config collection. The repository never deploys infrastructure or modifies AWS configuration.

## Run the website

The standalone site uses local HTML, CSS, JavaScript and JSON. No build step or CDN is required. Serve it over HTTP so module imports and JSON loads work:

```bash
python3 -m http.server 8088 --bind 127.0.0.1
```

Open `http://127.0.0.1:8088/`. GitHub Pages can continue serving the repository root, including `.nojekyll`, `web/`, `data/` and synthetic evidence. Do not publish local live evidence. If you later expose a local server to the LAN, check listeners and update the shared Ubuntu web-app inventory.

## Portfolio synchronization

The Bright Ridge React route mounts the same interactive renderer with bundled copies of the same program and baseline. To refresh that local copy after changing this repository:

```bash
python3 scripts/sync_portfolio.py --portfolio /home/ssmith/repos/portfolio-ssmith/portfolio
cd /home/ssmith/repos/portfolio-ssmith/portfolio
npm run build
npm run dev -- --host 127.0.0.1
```

This writes only the SOC 2 renderer/data/style directory and public SOC 2 downloadable resources. It does not change unrelated portfolio pages. Publishing GitHub/AWS remains a separate user action.

## Project boundaries

36 catalog controls are documented; **four narrow assertions are executable**, with one live Config adapter. Human governance, policy quality, legal review, supplier report review and CPA judgments require human assessment. The collector is scoped to a single approved account/region per run and cannot discover your whole organization. No production costs, live account posture or cross-LAN access have been validated by this work sample.

Test logic and parameters are versioned. A file digest helps detect changes relative to a trusted manifest; it does not establish origin or substitute for protected evidence custody.

## Revision validation, 2026-10-03

- 29 Python tests passed, including source identity, pagination, denied reads, unhealthy recorder, temporal consistency, seeded faults and custody tampering.
- The baseline was reproduced and both its manifest and an extracted runnable learning kit were verified.
- Bright Ridge's Vite production build passed. The SOC 2 guide bundle loads only on its project route; Vite still reports a size advisory for the main portfolio bundle.
- All nine interactive sections passed browser checks at 1440px and 390px in both the standalone site and built portfolio, including search, filters, keyboard expansion, guide readers, downloads and route navigation. No browser exceptions or page-width overflow were observed.
- Live AWS collection/deployment and independent CPA examination were not performed. The portfolio LAN URL was checked from the Ubuntu host; another LAN computer and the TCP 5173 firewall allowance remain unverified. The shared LAN inventory records this preview.
