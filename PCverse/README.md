# PCVerse

PCVerse uses a React/Vite frontend and a Flask application that serves both
the JSON API and the existing Jinja pages. Recommendations and compatibility
checks are rule-based; no external AI service is required.

## Run locally

Prerequisites: Python 3.11 or newer, Node.js, and npm.

1. In `PCverse`, create and activate a virtual environment, then install the
   backend requirements:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r app\requirements.txt
   ```

2. Set a stable session secret and start Flask:

   ```powershell
   $env:PCVERSE_SECRET_KEY = "replace-with-a-long-random-secret"
   python run.py
   ```

   The default database URI is `sqlite:///site.db` (stored by
   Flask-SQLAlchemy under `instance`). Set `PCVERSE_DATABASE_URI` to use a
   different database. This repository does not currently include migrations
   or a database seeding command, so the configured database must already
   have the application tables and product data.

3. In `PCverse\frontend`, install frontend dependencies and start Vite:

   ```powershell
   npm install
   npm run dev
   ```

   The local API client currently targets `http://localhost:5000/api`.
   Configure `PCVERSE_CORS_ORIGINS` as a comma-separated list when using
   other frontend origins. For HTTPS deployments, set
   `PCVERSE_COOKIE_SECURE=true` and provide `PCVERSE_SECRET_KEY` through the
   deployment environment.

## Validation

From `PCverse`:

```powershell
python -m unittest discover -s tests -v
```

From `PCverse\frontend`:

```powershell
npm run lint
npm run build
```
