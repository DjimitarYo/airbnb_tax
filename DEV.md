# Development Guide

## Project Purpose

This project is a Bulgarian-market marketplace for connecting Airbnb and short-term rental hosts with verified cleaners.

The MVP should let hosts post one cleaning or a month of cleaning jobs, let verified cleaners apply, let both sides agree on price outside the platform, share calendar availability, and collect two-way feedback after completed work.

## MVP Scope

The first production version should include:

- Host, cleaner, and admin user roles.
- Host property management.
- Single cleaning job posting.
- Monthly cleaning batch creation from reservations or manual dates.
- Cleaner verification before marketplace access.
- Cleaner applications to individual jobs or monthly batches.
- Assignment workflow after host approval.
- Agreed price tracking in EUR without in-app payments.
- Internal calendar as the source of truth.
- Google Calendar sync plus iCal import/export.
- Email, in-app, and SMS notifications for important workflow events.
- Two-way reviews after completed jobs.
- Admin moderation for cleaners, reviews, disputes, and marketplace activity.

Out of scope for v1 unless explicitly requested:

- In-app payments, payouts, invoices, platform fees, or wallet balances.
- Native mobile apps.
- Property management system integrations such as Guesty or Hostaway.
- Advanced operations such as supplies inventory, photo inspections, or damage claim workflows.

## Expected Stack

Use this baseline stack unless the architecture document is intentionally updated:

- Backend: Python, Django, Django REST Framework.
- Frontend: React with Next.js as a responsive web/PWA.
- Database: PostgreSQL.
- Cache and broker: Redis.
- Background jobs: Celery.
- Object storage: EU-hosted S3-compatible storage for future uploaded assets.
- Hosting: EU managed cloud infrastructure.
- Timezone: `Europe/Sofia`.
- Currency: EUR.
- Languages: Bulgarian and English.

## Repository State

This repository contains the first application scaffold:

- `backend/`: Django project, Django REST Framework APIs, domain apps, service-layer workflows, initial migrations, and tests.
- `frontend/`: Next.js responsive web/PWA dashboard shell.
- `docker-compose.yml`: PostgreSQL, Redis, backend, Celery worker, and frontend local stack.
- `.env.example`: local environment defaults.

## Local Development Conventions

Current layout:

```text
backend/
  config/
  apps/
frontend/
  app/
  lib/
docker-compose.yml
.env.example
```

Keep the backend modular even before services are split. Each backend domain should own its models, serializers, services, permissions, tests, and migrations.

Prefer explicit service-layer functions for business workflows such as accepting applications, assigning cleaners, completing jobs, and submitting reviews. Avoid putting marketplace state transitions directly inside views.

## Environment Setup

Copy the example environment file before using Docker Compose:

```powershell
Copy-Item .env.example .env
```

The Docker environment uses PostgreSQL and Redis. When running the backend directly without `DATABASE_URL`, Django falls back to local SQLite for lightweight development checks.

## Docker Development

Run the full local stack:

```powershell
docker compose up --build
```

Useful service URLs:

- Frontend: `http://localhost:3000`
- Backend health check: `http://localhost:8000/api/health/`
- Django admin: `http://localhost:8000/admin/`

Run backend commands through Docker:

```powershell
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py createsuperuser
docker compose run --rm backend python manage.py test
```

## Backend Local Commands

From `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run tests and checks:

```powershell
python manage.py check
python manage.py test
python -m compileall .
```

Run a Celery worker after Redis is available and dependencies are installed:

```powershell
celery -A config worker --loglevel=info
```

## Frontend Local Commands

From `frontend/`:

```powershell
npm install
npm run dev
```

Run frontend checks:

```powershell
npm run typecheck
npm run lint
npm run build
```

## Git Setup Note

This workspace has reported a Git safe-directory ownership warning. If Git commands fail locally with `detected dubious ownership`, the developer or agent may need to run:

```powershell
git config --global --add safe.directory C:/Users/35987/Desktop/airbnb_tax
```

Only run that command after confirming it is appropriate for the current machine and user account.

## Testing Expectations

When code exists, test coverage should focus on:

- Job lifecycle transitions.
- Cleaner verification and permissions.
- Application and assignment rules.
- Calendar conflict detection.
- Google Calendar and iCal sync behavior.
- Notification triggers.
- Review eligibility and two-way review constraints.
- Admin moderation actions.

Every change to business logic, data models, API permissions, migrations, or background tasks should include tests or a clear explanation for why tests were not added.

## Documentation Expectations

Update documentation in the same change when modifying:

- Business strategy, target users, marketplace assumptions, monetization hypotheses, launch strategy, or success metrics.
- Architecture boundaries.
- User workflows.
- Data model concepts.
- API behavior.
- Local development commands.
- Deployment assumptions.
- External integrations.

Documentation roles:

- `BUSINESS.md` defines the business strategy, target market, value proposition, marketplace model, monetization hypotheses, success metrics, risks, and open business questions.
- `architecture.md` defines technical architecture, domain boundaries, data concepts, integrations, and future service extraction.
- `DEV.md` defines developer setup, project conventions, expected stack, and maintenance expectations.
- `AGENT.md` defines how AI and developer agents should work in the repository.
