# Node Backends

Covers Express, Fastify, Hono and Koa services in JavaScript or TypeScript. NestJS has its own section at the end.

## Layout

Small service:

```
src/
  routes/
  db.ts
  server.ts
```

Growing service:

```
src/
  modules/
    orders/
      orders.routes.ts      # HTTP wiring
      orders.service.ts     # business logic, once routes grow too long
      orders.repository.ts  # data access, once queries grow too long
      orders.schema.ts      # request validation
      orders.test.ts
    users/
  lib/                      # db client, logger, mailer, queue client
  middleware/               # auth, error handler, request logging
  config/                   # env parsing, one place
  app.ts                    # builds the app, no listen()
  server.ts                 # entry, calls listen()
scripts/                    # one-off and maintenance scripts
migrations/                 # or the ORM's default folder
```

- Start a module as one file. Split it into routes, service and repository files when the single file gets too long to read.
- Separate `app.ts` from `server.ts` only if tests already import the app without starting a server.

## Boundaries

- Modules never import another module's repository. They call the other module's service or exported functions.
- `lib/` and `middleware/` never import from `modules/`.
- Read environment variables in `config/` and nowhere else.

## Naming

- kebab-case or dot-separated file names, matching what the repo uses most. `orders.service.ts` and `orders-service.ts` are both common. Pick one.
- Name modules after the domain in plural or singular, consistently.

## Tests

- Unit tests beside the file.
- Integration tests that hit a real database go in a root `tests/` or `test/integration/` folder if the project separates them already.

## ESM and Imports

- Projects with `"type": "module"` and `moduleResolution` set to `NodeNext` need the `.js` extension in relative imports, even in TypeScript. Keep the extensions when you rewrite paths.
- TypeScript `paths` aliases do not work at runtime on their own. Check whether the project uses `tsc-alias`, `tsx`, or a bundler before adding or changing aliases.

## Moving Files Safely

- Run `tsc --noEmit` after each batch.
- Start the server and hit one route per moved module. Dynamic `require()` and route auto-loading by folder do not show up in the compiler.

## Path References to Update

- `package.json` `main`, `exports`, `bin` and script paths
- `tsconfig.json` `rootDir`, `outDir`, `include` and `paths`
- `nodemon.json`, `tsx watch` or `ts-node` entry paths
- `Dockerfile` `COPY` and `CMD` lines
- ORM config, such as Prisma `schema` path, TypeORM `entities` and `migrations` globs, and Drizzle `schema` and `out`
- Test config `testMatch`, `roots` or `include`
- Route auto-loaders such as `@fastify/autoload` folder options
- Process manager config such as `ecosystem.config.js`

## NestJS

- Follow Nest's convention of one module per domain, as in `src/orders/orders.module.ts` with its controller, service and DTOs beside it.
- Shared providers go in `src/common/` or a `SharedModule`, only when two modules use them.
- `nest-cli.json` `sourceRoot` and the TypeORM or Prisma entity paths need updates after moves.
- Use `nest g module` for new modules so files land where the CLI expects them.
