# demo-devsecops

A small learning sandbox that walks a tiny web API through GitLab's DevSecOps
stages: plan, create, verify, package, secure, release, configure and monitor.
It was built as a warm-up for the GitLab Transcend hackathon (October 2026),
before the main entry.

The application itself is deliberately trivial. The interesting part is the
`.gitlab-ci.yml` pipeline around it: lint, tests against a real Postgres,
six security scanners, a Docker image in the Container Registry, an automatic
staging deploy and a manual production deploy over Tailscale. One feature
(`GET /ping`) was implemented end to end by the GitLab Duo Developer agent,
from issue to merged merge request.

## The app

A [FastAPI](https://fastapi.tiangolo.com/) service with four endpoints:

| Endpoint | Returns |
|---|---|
| `GET /hello` | `{"message": "hello"}` |
| `GET /ping` | `{"pong": true}` |
| `GET /db-check` | `{"db": true}` when Postgres answers `SELECT 1` |
| `GET /version` | the running commit (`APP_VERSION`) and environment (`APP_ENV`) |

The database connection string comes from `DATABASE_URL`
(default `postgresql://app:app@localhost:5432/app`).

## Run locally

Requires Python 3.12 and, for the database endpoints and tests, Postgres.

```sh
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt

# Postgres for /db-check and the database tests
docker run -d --name demo-pg -p 5432:5432 \
  -e POSTGRES_DB=app -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app \
  postgres:16-alpine

uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

Or run the container image:

```sh
docker build -t demo-devsecops .
docker run --rm -p 8000:8000 demo-devsecops
```

## Tests and lint

```sh
ruff check .
pytest --cov=app            # needs Postgres, see above
pytest tests/test_hello.py  # endpoint tests only, no database needed
```

## CI/CD pipeline

`.gitlab-ci.yml` runs for merge requests and for the default branch only.

| Stage | Jobs |
|---|---|
| lint | `ruff`, with a Code Quality report on the merge request |
| test | `pytest` against a Postgres service with JUnit and coverage reports; Secret Detection, SAST, IaC SAST and Dependency Scanning from GitLab templates |
| build | builds the image, checks that it imports, pushes `:<short sha>` (and `:latest` on `main`) to the Container Registry |
| scan | Container Scanning of the image just built |
| dast | DAST against the image started as a CI service |
| staging | automatic deploy after every merge to `main` |
| production | manual deploy from the pipeline |

At the last commit the lint, test and scanner jobs are switched off by
variables at the top of `.gitlab-ci.yml` (`VERIFY_DISABLED` and the
`*_DISABLED` flags) to keep the pipeline fast. Delete those lines to switch
them back on.

### Deploy

Both environments run on a private machine that is reachable only over
[Tailscale](https://tailscale.com/). The deploy job joins the tailnet as a
short-lived node, then connects over SSH with a key that the target machine
restricts to a single script taking `<environment> <image tag>`. The compose
file and that script live on the target machine, not in this repository, so
whoever can push here decides which image runs but not how it runs. See
[deploy/README.md](deploy/README.md) for the full flow, the CI/CD variables it
needs (`TS_AUTHKEY`, `DEPLOY_SSH_KEY_B64`, `KIMLAB_KNOWN_HOSTS`, `KIMLAB_IP`)
and how to roll back.

To deploy somewhere else, replace the `.deploy` job template with your own
target; the rest of the pipeline does not depend on it.

The pipeline is written for GitLab CI/CD. On GitHub it is kept as reference;
it does not run there.

## License

[MIT](LICENSE)
