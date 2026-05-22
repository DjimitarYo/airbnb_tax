# Host Cleaner Marketplace

Marketplace for Bulgarian short-term rental hosts, verified cleaners, and cleaning agencies.

The MVP focuses on job posting, monthly cleaning batches, cleaner applications, assignment, shared calendar coordination, notifications, and two-way feedback. Payments are intentionally out of scope for v1.

## Documentation

- `BUSINESS.md`: business strategy, target market, monetization hypotheses, risks, and open questions.
- `architecture.md`: technical architecture and domain boundaries.
- `DEV.md`: development setup and operating guide.
- `AGENT.md`: instructions for AI and developer agents.

## Stack

- Backend: Django, Django REST Framework, PostgreSQL, Redis, Celery.
- Frontend: Next.js responsive web/PWA.
- Local infrastructure: Docker Compose with PostgreSQL, Redis, backend, worker, and frontend services.

## Quick Start

Copy environment defaults:

```powershell
Copy-Item .env.example .env
```

Run the full local stack:

```powershell
docker compose up --build
```

Default URLs:

- Frontend: `http://localhost:3000`
- Backend health check: `http://localhost:8000/api/health/`
- Django admin: `http://localhost:8000/admin/`

## Current Implementation Status

The repository now contains the first implementation scaffold:

- Django project and domain apps.
- Initial database models and migrations.
- REST API route groups.
- Session-cookie signup, login, logout, and current-user APIs.
- Manual account approval states and admin approval actions.
- Agency profiles, invitations, memberships, and delegated cleaner assignments.
- Cookie consent records for optional analytics and marketing cookies.
- Marketplace service functions for publishing jobs, applying, accepting, completing, and reviewing.
- Notification records and placeholder Celery tasks.
- Calendar conflict API and placeholder sync tasks.
- Next.js landing page, login/signup pages, protected app entry, and cookie consent banner.
- Docker Compose local infrastructure.
