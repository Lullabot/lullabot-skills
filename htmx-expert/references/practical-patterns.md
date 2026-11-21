# Practical htmx patterns

## Contents

- Loading indicators
- Search inputs
- Polling
- Row updates
- Event attributes
- Multiple triggers
- Form submission


### Loading Indicators with CSS Spinner

Use CSS-only spinners instead of image files for better performance:

```html
<button hx-get="/api/slow"
        hx-indicator="#spinner">
    Load
    <span id="spinner" class="spinner htmx-indicator"></span>
</button>

<style>
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline-block; }

.spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3d72d7;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
```

### Input Search with Proper Trigger

Use `input changed` instead of `keyup changed` for better UX (catches paste, autofill):

```html
<input type="search"
       name="q"
       hx-get="/api/search"
       hx-trigger="input changed delay:300ms, search"
       hx-target="#results">
```

The `search` trigger handles the search input's clear button (X).

### Self-Targeting with Polling

For elements that replace themselves (polling), use `hx-target="this"`:

```html
<div hx-get="/api/time"
     hx-trigger="load, every 2s"
     hx-target="this"
     hx-swap="innerHTML">
    Loading...
</div>
```

### Row Updates with closest

For list items where each row has its own update button:

```html
<li id="item-1">
    <span>Item 1</span>
    <button hx-get="/api/update-item/1"
            hx-target="closest li"
            hx-swap="outerHTML">
        Update
    </button>
</li>
```

Server returns complete `<li>` element with new htmx attributes intact.

### Event Attribute Syntax

The `hx-on::` syntax uses double colons for htmx events:

```html
<!-- Correct -->
<button hx-on::before-request="console.log('starting')">

<!-- Also correct (older syntax) -->
<button hx-on:htmx:before-request="console.log('starting')">
```

### Combining Multiple Triggers

Separate triggers with commas:

```html
<div hx-get="/api/data"
     hx-trigger="load, every 5s, click from:#refresh-btn">
```

### Form POST with Loading State

Combine `hx-indicator` and `hx-disabled-elt` for complete UX:

```html
<form hx-post="/api/submit"
      hx-target="#result"
      hx-indicator="#spinner"
      hx-disabled-elt="find button">
    <input name="email" required>
    <button type="submit">
        Submit
        <span id="spinner" class="spinner htmx-indicator"></span>
    </button>
</form>
```
