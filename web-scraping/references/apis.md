# Observed Web APIs

How to find the JSON endpoints that sit behind a site's interface, and how to
call them safely once found. Many sites load their data from clean public APIs
that are far more reliable to consume than scraped HTML.

## Finding Public Endpoints

Use browser developer tools to discover APIs:

1. **Open developer tools** (right-click, then Inspect, or F12)
2. **Go to the Network tab** to monitor all requests
3. **Filter by Fetch/XHR** to show only API calls
4. **Trigger the action** you want to capture (search, scroll, click)
5. **Analyze the response**, usually JSON with key-value pairs
6. **Copy as cURL** (right-click the request)
7. **Convert to code** using [curlconverter.com](https://curlconverter.com/)

## Stripping Down API Requests

When you copy a request from developer tools, it may contain credentials and
unrelated browser state. Rebuild the smallest safe request:

1. **Remove all cookies, authorization headers, CSRF tokens, and tracking
   identifiers.** Never paste them into code or agent context.
2. **Confirm the endpoint is intended for public access.** If authentication
   is required, use official documentation and credentials supplied under
   documented authorization.
3. **Identify the minimum input parameters** needed for the public request.
4. **Add timeouts, response-size limits, and schema validation.** Treat
   returned fields as untrusted data.

## Example: Calling An Observed Public Autocomplete Endpoint

```python
import requests
import time

def search_suggestions(keyword: str) -> dict:
    """
    Get autocomplete suggestions from an observed public endpoint.
    The request contains no copied browser credentials or session state.
    """
    headers = {
        'User-Agent': 'ResearchScraper/1.0 (+https://example.org/contact)',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    params = {
        'prefix': keyword,
        'suggestion-type': ['WIDGET', 'KEYWORD'],
        'alias': 'aps',
        'plain-mid': '1',
    }

    response = requests.get(
        'https://completion.amazon.com/api/2017/suggestions',
        params=params,
        headers=headers,
        timeout=15
    )
    response.raise_for_status()
    return response.json()

# Collect suggestions for multiple keywords
keywords = ['a', 'b', 'cookie', 'sock']
data = []

for keyword in keywords:
    suggestions = search_suggestions(keyword)
    suggestions['search_word'] = keyword  # track seed keyword
    time.sleep(1)  # rate limit yourself
    data.extend(suggestions.get('suggestions', []))
```

*Source: [Leon Yin, "Finding Undocumented APIs," Inspect Element](https://inspectelement.org/apis.html), 2023*
