# Ruby on Rails

Rails fixes most of the layout. Follow it.

## Layout

```
app/
  models/
  controllers/
    admin/          # namespaced controllers
  views/
  jobs/
  mailers/
  helpers/
  javascript/
  assets/
  services/         # only if the project already uses it
config/
  routes.rb
db/
  migrate/
  schema.rb
lib/
  tasks/            # rake tasks
spec/ or test/
```

- Every folder under `app/` autoloads. Adding `app/services/` or `app/queries/` works without config, but add one only if the codebase already has code of that kind spread elsewhere.
- Code with no Rails dependency goes in `lib/`.
- Shared model or controller behavior goes in `app/models/concerns/` and `app/controllers/concerns/`.

## Zeitwerk Rules

Rails loads code with Zeitwerk, and file paths must match constant names.

- `app/services/billing/invoice_creator.rb` must define `Billing::InvoiceCreator`.
- Moving a file into a subfolder therefore renames its constant. Treat that as a symbol rename and ask before doing it.
- Moving a file between top-level `app/` folders, such as from `app/models/` to `app/services/`, keeps the constant name. That move is safe.
- Run `bin/rails zeitwerk:check` after each batch.

## Grouping by Domain

- For large apps, namespace inside the Rails folders, as in `app/models/billing/`, `app/controllers/billing/`. This keeps Rails conventions and groups by domain.
- Namespaced models need `self.table_name` or a `table_name_prefix` if the table name should stay the same.
- Packwerk from Shopify enforces boundaries between packs. Offer it for large apps and add it only on a yes.
- Rails engines split a large app into gems. That is an architecture change, beyond this skill.

## Naming

- Files in `snake_case`, matching the constant.
- Controllers plural, as in `OrdersController`. Models singular.

## Tests

- RSpec mirrors `app/` under `spec/`, as in `spec/models/order_spec.rb`. Minitest mirrors it under `test/`.
- Move a spec whenever you move its file.
- System and request tests stay in `spec/system/` and `spec/requests/`.

## Path References to Update

- `config/routes.rb` when controllers move into namespaces
- View paths, since `app/views/` mirrors controller namespaces
- `config/application.rb` `autoload_paths` and `eager_load_paths`
- Polymorphic `*_type` columns and STI `type` columns store class names in the database. Renaming such a class needs a data migration. Leave those classes in place unless the user asks.
- Serialized YAML, job arguments in a queue and cache keys that hold class names
