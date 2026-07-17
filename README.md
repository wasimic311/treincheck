# treincheck

Tracks NS (Nederlandse Spoorwegen) train disruptions over time and measures how accurate NS's own published resolution times really are.

NS shows what's broken _right now_ — but that page has no memory. When a disruption ends, it disappears, and nobody can answer: **how often does NS actually fix things by the time they promise?** treincheck polls the NS Disruptions API every 5 minutes, tracks every disruption as a case with a full lifecycle, and compares NS's published end times against observed reality.

> **Status: v1 in active development.** Data collection pipeline is being built; accuracy analysis and public dashboard follow once enough history has accumulated.

## How it works

Every disruption is a **case** with a lifecycle, not a snapshot:

```
open ──► resolving ──► resolved
  ▲          │
  └──────────┘  (reappears during grace period)
```

- **open** — disruption is active according to the NS API
- **resolving** — NS reports it ended; waiting out a grace period of 2–3 clean polls
- **resolved** — survived the grace period; case closed permanently

All status transitions are stored with timestamps — the history of how a delay evolved _is_ the data. Raw API responses are stored as well, so new questions can be answered later without re-collecting.

## Architecture

```
treincheck/
├── core/     # models, DB layer, business logic (shared)
├── api/      # FastAPI routes — thin read layer
└── worker/   # poller + case engine — writes to DB
```

| Component  | Choice                   | Why                                                       |
| ---------- | ------------------------ | --------------------------------------------------------- |
| Database   | Postgres                 | Source of truth; raw responses stored as JSONB            |
| ORM        | SQLAlchemy 2.0 + Alembic | Schema will evolve (v2), so migrations from day one       |
| API        | FastAPI                  | Thin read layer over `core/`                              |
| Worker     | Separate process         | Not inside FastAPI startup events; idempotent, crash-safe |
| Scheduling | asyncio loop             | One periodic task — Celery/Airflow would be overkill here |

### Design decisions

- **Grace period before closing a case.** NS sometimes drops a disruption from the feed and re-publishes it moments later. A case only closes after 2–3 consecutive polls without it — if it reappears, the same case flips back to `open`. No duplicate rows.
- **Crash-safe worker.** On restart, open cases are picked up from the database and tracking continues. The DB is the source of truth, not process memory.
- **Store raw, filter on read.** Every API response is stored untouched. The case engine only processes unplanned disruptions (`DISRUPTION`/`CALAMITY`), but planned maintenance stays queryable.
- **No task queue.** A single poll loop every 5 minutes doesn't justify Celery or Airflow. I'd reach for Celery with many concurrent independent jobs, and Airflow for multi-step batch dependencies — neither applies here.

## Local development

Requirements: Python 3.12+, Docker Desktop.

```bash
# 1. Start Postgres
docker compose up -d

# 2. Create a virtualenv and install dependencies
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt

# 3. Configure
copy .env.example .env        # then fill in your NS API key

# 4. Run migrations
alembic upgrade head

# 5. Start the poller
python -m worker
```

An NS API key is free via the [NS API portal](https://apiportal.ns.nl).

## Roadmap

- [x] Repo, Dockerized Postgres, NS API access
- [ ] Raw response storage + poll loop
- [ ] Case engine (open → resolving → resolved)
- [ ] Poll-cycle logging + gap/failure tracking
- [ ] FastAPI read endpoints
- [ ] Accuracy analysis: NS published times vs observed
- [ ] Public dashboard at [treincheck.nl](https://treincheck.nl)
- [ ] **v2:** refund eligibility checker for NS's ["Geld terug bij vertraging"](https://www.ns.nl/service-en-contact/geld-terug/geld-terug-bij-vertraging) policy (30+/60+ min delays)

## License

MIT
