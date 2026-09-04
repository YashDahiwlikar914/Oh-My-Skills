# Node And Express

Read this guide for Node.js services and Express applications. Inspect the
middleware order, error handler, request types, package scripts, and deployment
runtime before editing.

## Middleware And Routes

Keep authentication, authorization, validation, parsing, business logic, and
serialization in the layers already used by the project. Do not create a
controller, service, repository, adapter, and factory for one route without a
real boundary.

Make async failures reach the project's error middleware. Do not send a success
response and then continue with work that can fail unless the contract is an
explicit background job.

```ts
app.get("/users/:id", requireUser, validateUserId, async (req, res, next) => {
  try {
    const user = await users.findById(req.params.id);
    if (!user) {
      res.sendStatus(404);
      return;
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

Use the project's async wrapper if one exists. Validate request body, query,
params, headers, and content type at the boundary. Do not trust a TypeScript
request cast as runtime validation.

## Security

Keep helmet or equivalent security headers, request size limits, rate limits,
CSRF protections where relevant, secure cookie settings, origin policy, and
authorization checks. Check ownership after authentication. Do not treat a
valid user ID as proof that the caller may access that user.

Use parameterized database queries. Avoid `eval`, dynamic require paths,
unbounded body parsing, shell interpolation, and logging `req.headers` or full
request bodies.

## Errors And Responses

Keep one error response shape if the project has one. Do not expose stack
traces, SQL errors, internal paths, or provider responses in production. Log
server-side context with redaction and correlation IDs when the project uses
them.

Return after sending a response. Check status codes from upstream services and
bound request timeouts. Retry only idempotent operations or operations with a
deduplication key.

## Verification

Run `npm test`, `npm run lint`, `npm run typecheck`, and the scripts declared in
`package.json`. Test malformed input, missing resources, unauthorized access,
upstream failure, duplicate requests, and response serialization where relevant.

## Sources

- https://expressjs.com/en/guide/error-handling.html
- https://nodejs.org/api/http.html
- https://owasp.org/www-project-top-ten/
