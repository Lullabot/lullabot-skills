---
name: htmx-expert
description: "This skill should be used when users need help with htmx development, including implementing AJAX interactions, understanding htmx attributes (hx-get, hx-post, hx-swap, hx-target, hx-trigger), debugging htmx behavior, building hypermedia-driven applications, or following htmx best practices. Use when users ask about htmx patterns, server-side HTML responses, or transitioning from SPA frameworks to htmx. (user)"
---

# htmx Expert

## Requirements

For guidance, source read/edit access and a browser are sufficient. Running an application needs htmx and its project's backend, HTTP server, and dependency manager; Flask examples require Flask only if used. The bundled development server needs Python 3 and uses only its standard library. Extension loading needs the selected extension and network access unless served locally. No authentication or MCP server is needed for the local prototype.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/htmx-expert"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

Review generated server code and shell commands before execution outside a verified secure sandbox. Serve only a dedicated prototype directory with public/synthetic fixtures on loopback; the helper is a development server, not a production deployment. Browser requests can mutate the backend: test POST/PUT/PATCH/DELETE only on authorized disposable data, retaining server-side authorization, escaping, and CSRF validation. `hx-confirm` is a user prompt, not authorization. Keep request origins restricted and script processing disabled unless a reviewed feature needs them. History snapshots and logs may contain personal data; disable history caching on sensitive views and avoid shipping debug logging. A human reviews accessibility, security behavior, examples, and any deployment or sharing destination before delivery.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


This skill provides comprehensive guidance for htmx development, the library that extends HTML to access modern browser features directly without JavaScript.

## Core Philosophy

htmx represents a paradigm shift toward hypermedia-first web development. Instead of treating HTML as a presentation layer with JSON APIs, htmx extends HTML to handle AJAX requests, CSS transitions, WebSockets, and Server-Sent Events directly. Servers respond with HTML fragments, not JSON.

## When to Use This Skill

- Implementing htmx attributes and interactions
- Building hypermedia-driven applications
- Debugging htmx request/response cycles
- Converting SPA patterns to htmx approaches
- Understanding htmx events and lifecycle
- Configuring htmx extensions
- Implementing proper security measures

## Core Attributes Reference

### HTTP Verb Attributes

| Attribute | Purpose | Default Trigger |
|-----------|---------|-----------------|
| `hx-get` | Issue GET request | click |
| `hx-post` | Issue POST request | click (form: submit) |
| `hx-put` | Issue PUT request | click |
| `hx-patch` | Issue PATCH request | click |
| `hx-delete` | Issue DELETE request | click |

### Request Control

- **hx-trigger**: Customize when requests fire
  - Modifiers: `changed`, `delay:Xms`, `throttle:Xms`, `once`
  - Special triggers: `load`, `revealed`, `every Xs`
  - Extended: `from:<selector>`, `target:<selector>`

- **hx-include**: Include additional element values in request
- **hx-params**: Filter which parameters to send (`*`, `none`, `not <param>`, `<param>`)
- **hx-headers**: Add custom headers (JSON format)
- **hx-vals**: Add values to request (JSON format)
- **hx-encoding**: Set encoding (`multipart/form-data` for file uploads)

### Response Handling

- **hx-target**: Where to place response content
  - Extended selectors: `this`, `closest <sel>`, `next <sel>`, `previous <sel>`, `find <sel>`

- **hx-swap**: How to insert content
  - `innerHTML` (default), `outerHTML`, `beforebegin`, `afterbegin`, `beforeend`, `afterend`, `delete`, `none`
  - Modifiers: `swap:Xms`, `settle:Xms`, `scroll:top`, `show:top`

- **hx-select**: Select subset of response to swap
- **hx-select-oob**: Select elements for out-of-band swaps

### State Management

- **hx-push-url**: Push URL to browser history
- **hx-replace-url**: Replace current URL in history
- **hx-history**: Control history snapshot behavior
- **hx-history-elt**: Specify element to snapshot

### UI Indicators

- **hx-indicator**: Element to show during request (add `htmx-indicator` class)
- **hx-disabled-elt**: Elements to disable during request

### Security & Control

- **hx-confirm**: Show confirmation dialog before request
- **hx-validate**: Enable HTML5 validation on non-form elements
- **hx-disable**: Disable htmx processing on element and descendants
- **hx-sync**: Coordinate requests between elements

## Implementation Patterns

### Basic AJAX Pattern

```html
<button hx-get="/api/data"
        hx-target="#result"
        hx-swap="innerHTML">
  Load Data
</button>
<div id="result"></div>
```

### Active Search

```html
<input type="search"
       name="q"
       hx-get="/search"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#search-results">
<div id="search-results"></div>
```

### Infinite Scroll

```html
<div hx-get="/items?page=2"
     hx-trigger="revealed"
     hx-swap="afterend">
  Loading more...
</div>
```

### Polling

```html
<div hx-get="/status"
     hx-trigger="every 5s"
     hx-swap="innerHTML">
  Status: Unknown
</div>
```

### Form Submission

```html
<form hx-post="/submit"
      hx-target="#response"
      hx-swap="outerHTML">
  <input name="email" type="email" required>
  <button type="submit">Submit</button>
</form>
```

### Out-of-Band Updates

Server response can update multiple elements:

```html
<!-- Main response -->
<div id="main-content">Updated content</div>

<!-- OOB updates -->
<div id="notification" hx-swap-oob="true">New notification!</div>
<span id="counter" hx-swap-oob="true">42</span>
```

### Loading Indicators

```html
<button hx-get="/slow-endpoint"
        hx-indicator="#spinner">
  Load
</button>
<img id="spinner" class="htmx-indicator" src="/spinner.gif">
```

CSS for indicators:
```css
.htmx-indicator {
  opacity: 0;
  transition: opacity 200ms ease-in;
}
.htmx-request .htmx-indicator {
  opacity: 1;
}
```

## Server Response Patterns

### Return HTML Fragments

Server endpoints return HTML, not JSON:

```python
# Flask example
@app.route('/search')
def search():
    q = request.args.get('q', '')
    results = search_database(q)
    return render_template('_search_results.html', results=results)
```

### Response Headers

htmx recognizes special headers:

| Header | Purpose |
|--------|---------|
| `HX-Location` | Client-side redirect (with context) |
| `HX-Push-Url` | Push URL to history |
| `HX-Redirect` | Full page redirect |
| `HX-Refresh` | Refresh the page |
| `HX-Reswap` | Override hx-swap value |
| `HX-Retarget` | Override hx-target value |
| `HX-Trigger` | Trigger client-side events |
| `HX-Trigger-After-Settle` | Trigger after settle |
| `HX-Trigger-After-Swap` | Trigger after swap |

### Detect htmx Requests

Check `HX-Request` header to differentiate htmx from regular requests:

```python
if request.headers.get('HX-Request'):
    return render_template('_partial.html')
else:
    return render_template('full_page.html')
```

## Events

### Key Events

| Event | When Fired |
|-------|------------|
| `htmx:load` | Element loaded into DOM |
| `htmx:configRequest` | Before request sent (modify params/headers) |
| `htmx:beforeRequest` | Before AJAX request |
| `htmx:afterRequest` | After AJAX request completes |
| `htmx:beforeSwap` | Before content swap |
| `htmx:afterSwap` | After content swap |
| `htmx:afterSettle` | After DOM settles |
| `htmx:confirm` | Before confirmation dialog |
| `htmx:validation:validate` | Custom validation hook |

### Event Handling

Using `hx-on*`:
```html
<button hx-get="/data"
        hx-on:htmx:before-request="console.log('Starting...')"
        hx-on:htmx:after-swap="console.log('Done!')">
  Load
</button>
```

Using JavaScript:
```javascript
document.body.addEventListener('htmx:configRequest', function(evt) {
  evt.detail.headers['X-Custom-Header'] = 'value';
});
```

## Security Best Practices

1. **Escape All User Content**: Prevent XSS through server-side template escaping
2. **Use hx-disable**: Prevent htmx processing on untrusted content
3. **Restrict Request Origins**:
   ```javascript
   htmx.config.selfRequestsOnly = true;
   ```
4. **Disable Script Processing**:
   ```javascript
   htmx.config.allowScriptTags = false;
   ```
5. **Include CSRF Tokens**:
   ```html
   <body hx-headers='{"X-CSRF-Token": "{{ csrf_token }}"}'>
   ```
6. **Content Security Policy**: Layer browser-level protections

## Configuration

Key `htmx.config` options:

```javascript
htmx.config.defaultSwapStyle = 'innerHTML';
htmx.config.timeout = 0; // Request timeout (0 = none)
htmx.config.historyCacheSize = 10;
htmx.config.globalViewTransitions = false;
htmx.config.scrollBehavior = 'instant'; // or 'smooth', 'auto'
htmx.config.selfRequestsOnly = true;
htmx.config.allowScriptTags = false;
htmx.config.allowEval = false; // Enable only for reviewed features that require evaluation
```

Or via meta tag:
```html
<meta name="htmx-config" content='{"selfRequestsOnly":true}'>
```

## Extensions

### Loading Extensions

```html
<script src="https://unpkg.com/htmx-ext-<name>@<version>/<name>.js"></script>
<body hx-ext="extension-name">
```

### Common Extensions

- **head-support**: Merge head tag information across requests
- **idiomorph**: Morphing swaps (preserves element state)
- **sse**: Server-Sent Events support
- **ws**: WebSocket support
- **preload**: Content preloading
- **response-targets**: HTTP status-based targeting

## Debugging

Enable logging:
```javascript
htmx.logAll();
```

Check request headers in Network tab:
- `HX-Request: true`
- `HX-Target: <target-id>`
- `HX-Trigger: <trigger-id>`
- `HX-Current-URL: <page-url>`

## Progressive Enhancement

Structure for graceful degradation:

```html
<form action="/search" method="POST">
  <input name="q"
         hx-get="/search"
         hx-trigger="keyup changed delay:300ms"
         hx-target="#results">
  <button type="submit">Search</button>
</form>
<div id="results"></div>
```

Non-JavaScript users get form submission; JavaScript users get AJAX.

## Third-Party Integration

Initialize libraries on htmx-loaded content:

```javascript
htmx.onLoad(function(content) {
  content.querySelectorAll('.datepicker').forEach(el => {
    new Datepicker(el);
  });
});
```

For programmatically added htmx content:
```javascript
htmx.process(document.getElementById('new-content'));
```

## Common Gotchas

1. **ID Stability**: Keep element IDs stable for CSS transitions
2. **Swap Timing**: Default 0ms swap delay; use `swap:100ms` for transitions
3. **Event Bubbling**: htmx events bubble; use `event.detail` for data
4. **Form Data**: Only named inputs are included in requests
5. **History**: History snapshots store innerHTML, not full DOM state

## Development Environment Requirements

### htmx Requires HTTP (Not file://)

htmx will NOT work when opening HTML files directly from the filesystem (`file://` URLs). This causes `htmx:invalidPath` errors because:
- Browsers block cross-origin requests from `file://` URLs
- htmx needs to make HTTP requests to endpoints

**Solution**: Always serve htmx applications via HTTP server:

```bash
# Simple Python server (recommended for development)
python3 -m http.server 8000 --bind 127.0.0.1 --directory ./prototype

# Or create a custom server with API endpoints
python3 server.py
```

### Minimal Development Server Pattern

For htmx examples and prototypes, create a simple Python server that:
1. Serves static files (HTML, CSS, JS)
2. Provides API endpoints that return HTML fragments

Run the bundled companion from the working project after code/command review:

```bash
python3 "$SKILL_DIR/scripts/dev_server.py" --directory ./prototype --port 8000
```

It binds only to `127.0.0.1`, serves the selected dedicated directory, and returns a sample HTML fragment for `/api/*`. Keep private files and symlinks out of that directory. Read [scripts/dev_server.py](scripts/dev_server.py) to adapt the handler; this example is not a production server. Verify it with `python3 -m unittest discover -s "$SKILL_DIR/tests"`.

## Practical Implementation Lessons

See [references/practical-patterns.md](references/practical-patterns.md) for concrete spinner, search, polling, row, event, and form examples. Event-handler examples require a reviewed evaluation configuration.

## Additional Resources

For detailed reference, consult:
- Official docs: https://htmx.org/docs/
- Attributes reference: https://htmx.org/reference/
- Examples: https://htmx.org/examples/
