# Laravel

Laravel fixes most of the layout. Follow it.

## Layout

```
app/
  Http/
    Controllers/
    Middleware/
    Requests/       # form request validation
  Models/
  Providers/
  Jobs/
  Events/
  Listeners/
  Policies/
  Services/         # only if the project already uses it
config/
database/
  migrations/
  factories/
  seeders/
resources/
  views/
  js/
  css/
routes/
  web.php
  api.php
  console.php
tests/
  Feature/
  Unit/
```

- Use `php artisan make:*` commands to create files so they land where Laravel expects them.
- Add folders such as `app/Actions/` or `app/Services/` only if code of that kind already exists in the repo.

## Grouping by Domain

- For large apps, group inside the Laravel folders, as in `app/Http/Controllers/Billing/` and `app/Models/Billing/`.
- A full domain layout such as `app/Domain/Billing/` changes many namespaces and fights the `make:*` commands. Propose it only for large apps and only if the team asks.
- Split `routes/web.php` into files per domain once it grows too long, and require them from the main file or register them in a service provider.

## PSR-4 Rules

Composer autoloads with PSR-4, so namespaces must match folder paths.

- Moving `app/Models/Invoice.php` to `app/Models/Billing/Invoice.php` changes the class from `App\Models\Invoice` to `App\Models\Billing\Invoice`. Treat that as a symbol rename and ask first.
- Update the `namespace` line and every `use` statement, then run `composer dump-autoload`.
- PhpStorm's Move refactor updates namespaces and imports.

## Naming

- Classes and files in PascalCase. Controllers singular with a suffix, as in `InvoiceController`.
- Views in kebab-case or snake_case folders under `resources/views/`, matching the repo.

## Tests

- `tests/Feature/` for HTTP and integration tests, `tests/Unit/` for isolated classes.
- Mirror the `app/` folder you moved, as in `tests/Unit/Billing/`.

## Path References to Update

- `routes/*.php` controller class references
- Service providers that bind classes or register policies
- `config/*.php` files that name classes
- Polymorphic relation `*_type` columns store class names in the database. Add `Relation::enforceMorphMap` aliases or a data migration before moving those models, or leave them in place.
- Queued jobs serialize their class name. Drain the queue or keep the old class until it empties.
- `composer.json` `autoload` and `autoload-dev`
