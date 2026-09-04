# Examples

Before and after pairs. Ponytail builds the minimal correct version and cites
the ladder rung and the guardrails it applied.

## Example 1 — One-product factory (rungs 2, 5 + abstraction test)

Before (AI-generated, over-built):

```ts
interface UserNamer {
  getName(user: User): string;
}
class DefaultUserNamer implements UserNamer {
  getName(user: User): string {
    return `${user.first} ${user.last}`;
  }
}
const namer: UserNamer = new DefaultUserNamer();
const display = namer.getName(user);
```

After (ponytail, full):

```ts
const displayName = `${user.first} ${user.last}`;
```

`→ skipped: UserNamer interface + DefaultUserNamer class, add when a second naming
strategy is actually required.`

## Example 2 — New cache dependency (rungs 3, 5 + stdlib)

Before:

```py
from mycache import Cache  # new dependency

class ResponseCache:
    def __init__(self):
        self._c = Cache()
    def get(self, key, fetch):
        if self._c.has(key):
            return self._c.get(key)
        val = fetch()
        self._c.set(key, val)
        return val
```

After (ponytail, full):

```py
from functools import lru_cache

@lru_cache(maxsize=1000)
def fetch_response(key):
    return _do_fetch(key)
```

`→ skipped: ResponseCache class and mycache dependency, add when lru_cache
measurably falls short (per-entry TTL, distributed).`

## Example 3 — Bloated helper with weak test (rungs 1, 6 + tests)

Before:

```ts
function normalizeAndValidateAndProcess(items: Item[]): Item[] {
  const out: Item[] = [];
  for (const it of items) {
    if (it && it.value != null) {
      out.push({ ...it, value: Math.max(0, it.value) });
    }
  }
  return out;
}
// test only asserts the function was called
expect(spy).toHaveBeenCalled();
```

After (ponytail, full):

```ts
const positiveItems = (items: Item[]) =>
  items.filter(it => it.value != null).map(it => ({ ...it, value: Math.max(0, it.value) }));
```

```ts
test("drops null values and clamps negatives", () => {
  expect(positiveItems([{ value: -1 }, { value: 2 }, { value: null }]))
    .toEqual([{ value: 0 }, { value: 2 }]);
});
```

`→ skipped: normalizeAndValidateAndProcess name (vague), add focused contract
test instead of a call assertion.`

## Example 4 — Misleading comment (ponytail fixes code, not prose)

Before:

```py
# This function securely validates the token
def check(token):
    return token == ADMIN  # hardcoded comparison, no signature
```

Ponytail action:

```py
# ponytail: fixed constant-time comparison and added expiry check
def check(token):
    return hmac.compare_digest(token, ADMIN) and not expired(token)
```

`→ skipped: comment wording polish (delegate to human-writing), fixed the code
the comment misdescribed instead.`
