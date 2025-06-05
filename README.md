make it PRD first, and we will have a better version of README after implementation

Product Requirements Document

Project: markitdown-ext (internal wrapper that saves PDF-embedded assets)
Author: Peter Hsu
Last updated: 5 Jun 2025

⸻

1. Purpose

Ship a drop-in replacement for MarkItDown that (a) persists extracted images/video to disk and (b) can be installed and executed by any employee through uv.

⸻

2. Goals & Success Metrics

Goal	Metric	Target
Universal availability	% of engineers who can uvx markitdownx` in ≤2 min on a clean machine	≥ 95 %
Correctness	Attachments from a 50-page mixed-media PDF are saved with byte-perfect fidelity	100 %
Maintainability	CI publishes a new tagged version in <5 min	100 % pass


⸻

3. Scope (Functional)
	1.	CLI parity – markitdownx must accept all upstream flags (--from, --format, etc.).
	2.	Asset export – save every result.attachments item to <basename>_assets/ and re-write the Markdown links accordingly.
	3.	PEP 621 packaging – deliver wheels + sdists via uv build.
	4.	Private distribution – publish to the org-wide GitHub Packages PyPI registry; resolve with uv pip … --index corp.
	5.	CI automation – GitHub Actions pipeline that triggers on version tags, runs uv build --no-sources, then uv publish --index corp.

Out-of-scope: multi-format output (DOCX, HTML), GUI, public PyPI release.

⸻

4. Technical Approach
	•	Code changes live in markitdown_ext/cli.py; wrap MarkItDown().convert() and iterate over attachments.
	•	Project layout:

markitdown_ext/
├─ markitdown_ext/__init__.py
├─ markitdown_ext/cli.py
├─ README.md
└─ pyproject.toml         # PEP 621 + setuptools backend


	•	Key pyproject.toml blocks

[project]
name = "markitdown-ext"
version = "0.1.0"
dependencies = ["markitdown>=1.4.0", "pillow>=10.3"]

[project.scripts]
markitdownx = "markitdown_ext.cli:main"

[build-system]
requires = ["setuptools>=78", "wheel>=0.45"]
build-backend = "setuptools.build_meta"


	•	uv tooling – leverage uv build, uv publish, and uvx for execution.﻿ ￼

⸻

5. Deliverables

ID	Deliverable	Owner	Acceptance criteria
D1	markitdown-ext source repo	Peter	passes pytest on push
D2	CI workflow (publish.yml)	Dev Infra	tag-triggered, publishes wheel
D3	Internal registry docs	Dev Rel	README snippet shows install + run
D4	Roll-out announcement	PM	sent on #topic-dev


⸻

6. Milestones & Timeline

Week	Milestone
W 0	Kick-off; confirm requirements
W 1	Feature complete code & unit tests
W 2	CI pipeline green; first wheel in registry
W 3	Pilot with five engineers; collect feedback
W 4	Org-wide release & documentation freeze


⸻

7. Risks & Mitigations

Risk	Impact	Mitigation
Large binaries clog registry	storage costs	enforce 100 MB per-asset cap; warn on exceed
uv tooling changes	build breaks	pin uv==latest-1 in CI
Cross-platform path issues	CLI fails on Windows	add Windows runner in CI matrix


⸻

8. Open Questions
	1.	Do we need an --assets-dir flag for custom destinations?
	2.	Should versioning follow CalVer or SemVer?
	3.	Is there a legal review needed before internal distribution?

⸻

Next action: approve this PRD or comment with changes by 10 Jun 2025 so implementation can start on schedule.
