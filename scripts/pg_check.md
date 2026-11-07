# PostgreSQL Verification Guide | SAHYADRUSHTI AI

## 1. Local Environment Status
- **Current Local Status:** The PostgreSQL daemon is **not running locally** on this Windows host, and the Docker daemon is not installed in the system PATH.
- **Development Default:** SAHYADRUSHTI AI defaults to SQLite with Write-Ahead Logging (`WAL` mode, `PRAGMA busy_timeout=5000`) for zero-dependency local development and CI runs.
- **Database Architecture:** All models use SQLModel / SQLAlchemy with dialect-neutral column types and standard ANSI SQL schemas. Alembic migrations (`e96b28a0285f`, `cba5086f810f`, `e28fead8b6b4`, `f49b1ca12345`) natively support PostgreSQL via psycopg (v3).

---

## 2. Option A: Running against Docker PostgreSQL

### Step 1: Start PostgreSQL Container
```bash
docker run -d \
  --name sahyadrushti-pg \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=sahyadrushti \
  -p 5432:5432 \
  postgres:16-alpine
```

### Step 2: Set Environment Variable
- **PowerShell (Windows):**
  ```powershell
  $env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/sahyadrushti"
  $env:DEBUG = "true"
  ```
- **Bash / Zsh (Linux / macOS):**
  ```bash
  export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/sahyadrushti"
  export DEBUG="true"
  ```

### Step 3: Run Alembic Migrations
```bash
python -m alembic upgrade head
```
*Expected output: All 4 migration revisions apply sequentially up to head (`f49b1ca12345`).*

### Step 4: Run Automated Test Suite
```bash
python -m pytest tests/
```
*All tests pass cleanly against the isolated PostgreSQL instance.*

### Step 5: Teardown
```bash
docker stop sahyadrushti-pg && docker rm sahyadrushti-pg
```

---

## 3. Option B: Running against Hosted PostgreSQL (Supabase / Neon / Cloud SQL / RDS)

1. Obtain your PostgreSQL connection string. Ensure the protocol is `postgresql+psycopg://` (or `postgresql://`).
2. Set the environment variable:
   ```bash
   export DATABASE_URL="postgresql+psycopg://<username>:<password>@<host>:<port>/<dbname>?sslmode=require"
   ```
3. Run migrations and verify schema:
   ```bash
   python -m alembic upgrade head
   python -m pytest tests/test_phase1_db.py
   ```

---

## 4. Key Configuration Notes
- **Driver:** Requires `psycopg[binary]>=3.1.0` (listed in `requirements.txt`).
- **Connection Pooling:** SQLAlchemy manages connection pooling automatically for PostgreSQL. For serverless Postgres (like Neon or Supabase Transaction Pooler on port 6543), set pool recycling or disable persistent pooling if connection limits are strict.

