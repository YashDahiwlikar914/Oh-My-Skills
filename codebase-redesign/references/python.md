# Python

Covers libraries, CLIs, Django and FastAPI or Flask services.

## Libraries and Packages

Use the `src/` layout for anything you publish or install.

```
pyproject.toml
src/
  mypkg/
    __init__.py
    core.py
    io/
      __init__.py
      readers.py
tests/
  conftest.py
  test_core.py
  io/
    test_readers.py
docs/
```

- The `src/` layout forces tests to import the installed package, so a file missing from the build fails locally before it fails for users.
- Develop with an editable install, `pip install -e .` or `uv pip install -e .`.
- Small scripts and single-file CLIs can stay flat, with the package folder at the root.

## Django

```
manage.py
config/                  # settings, urls.py, wsgi.py, asgi.py
  settings/
    base.py
    local.py
    production.py
orders/                  # one Django app per domain
  models.py
  views.py
  urls.py
  admin.py
  apps.py
  migrations/
  templates/orders/
  tests/
billing/
templates/               # project-wide templates
static/
```

- One app per domain. Split `models.py` or `views.py` into a package with `__init__.py` once the file grows too long, and import the names in `__init__.py` so Django finds them.
- Add a `services.py` or `selectors.py` only if the project already uses that pattern.

### Django Risks

- Moving or renaming an app changes its app label. The label names database tables, migration dependencies, content types and permissions. Set `label` in the app's `AppConfig` to the old label, or leave the app where it is.
- Migrations reference other apps by label. Grep `migrations/` for every label you touch.
- `INSTALLED_APPS`, `ROOT_URLCONF`, `AUTH_USER_MODEL`, `TEMPLATES` `DIRS` and `STATICFILES_DIRS` name paths and modules in strings.

## FastAPI and Flask

```
app/
  main.py               # creates the app, includes routers
  core/                 # settings, security, logging
  db/                   # session, base model
  orders/
    router.py           # or routes.py
    models.py
    schemas.py
    service.py          # once router.py grows too long
  users/
tests/
alembic/
```

- Flask uses one blueprint per domain in the same shape.
- Read settings in `core/config.py` with Pydantic settings or the project's existing tool, and nowhere else.

## Naming

- Modules and packages in `snake_case`, short, no hyphens.
- Avoid a module named the same as a standard library module, such as `logging.py` or `types.py`. It shadows the real one.
- `utils.py` holds small generic helpers. Domain logic goes in its domain package.

## Tests

- pytest convention puts tests in a root `tests/` folder mirroring the package. Keep that unless the repo already colocates.
- Name files `test_<module>.py`.
- Shared fixtures go in `conftest.py` at the level that needs them.
- If two test files share a base name in different folders, either add `__init__.py` to the test folders or set `--import-mode=importlib`.

## Moving Files Safely

- PyCharm's Move refactor and the `rope` library update imports. From the terminal, `git mv` and then grep for the old dotted path.
- Python resolves many paths from strings that no tool checks. Grep for the old dotted module path everywhere, including:
  - `mock.patch("pkg.module.name")` targets in tests
  - Celery task names and `include` lists
  - Logging config `handlers` and `loggers`
  - Django settings and `urls.py` `include()` strings
  - `importlib.import_module` and plugin entry points
- Run `python -m compileall -q src` and the full test suite after each batch.

## Path References to Update

- `pyproject.toml` `[project.scripts]`, package discovery such as `[tool.setuptools.packages.find] where`, and `[tool.pytest.ini_options] testpaths`
- `setup.cfg`, `setup.py`, `MANIFEST.in`
- `alembic.ini` `script_location` and `alembic/env.py` model imports
- Coverage `source` and `omit`
- `mypy`, `ruff` and `pyright` `include`, `exclude` and per-file settings
- `Dockerfile` `COPY` and `CMD`, `Procfile`, gunicorn or uvicorn module paths such as `app.main:app`
- Boundaries can be enforced with `import-linter`. Offer it and add it only on a yes.
