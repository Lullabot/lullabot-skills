/**
 * input-overlay.js — visible-input overlay for demo recordings.
 *
 * WHY: a recorded browser video does not show the OS mouse cursor or keystrokes.
 * For a demo a viewer needs to SEE what is being clicked/typed. This overlay
 * draws a soft cursor that follows the real mouse, a ripple on click, on-screen
 * key badges, and provides a chapter title-card API for narration.
 *
 * HOW TO INJECT (must run before the first navigation so it auto-installs on
 * every page/frame):
 *   await page.addInitScript({ path: '/var/www/html/<repo-relative-path>/input-overlay.js' });
 * The path is resolved by the process running Playwright. With
 * e0ipso/ddev-playwright-cli that process is INSIDE the web container, so use the
 * container path (the repo is mounted at /var/www/html).
 *
 * CRITICAL: it visualizes ONLY real input events. Drive the page with
 *   page.mouse.move/down/up, locator.click(), locator.dragTo(),
 *   and type via locator.pressSequentially() / page.keyboard.type().
 * locator.fill() and page.evaluate(()=>el.click()) bypass real events and show
 * NOTHING — and also fail to demonstrate the genuine user workflow.
 *
 * TITLE CARDS (call from the top frame between steps):
 *   await page.evaluate((t) => window.__demoTitle(t, 2600), 'Step label');
 *
 * SINGLE CURSOR ACROSS IFRAMES: the top frame owns the one cursor/ripple/keys.
 * Same-origin child frames (e.g. a modal rendered in an iframe) forward their
 * real events up to the top frame, mapped into top-frame coordinates, so exactly
 * one cursor is ever visible. (Cross-origin frames can't forward; the cursor will
 * pause at the frame boundary — acceptable and still single.)
 */
(() => {
  if (window.__demoOverlay) return;
  window.__demoOverlay = true;

  let topWin = window;
  try { topWin = window.top; } catch (e) { topWin = window; }
  const isTop = (topWin === window);

  // ---- Top frame owns the single cursor + ripple + key badges + title card ----
  const installTop = () => {
    if (!document.body || document.getElementById('__demo_style')) return;
    const style = document.createElement('style');
    style.id = '__demo_style';
    style.textContent = `
      .__demo-cursor{position:fixed;z-index:2147483647;width:30px;height:30px;margin:-15px 0 0 -15px;
        border-radius:50%;background:rgba(20,120,255,.30);border:3px solid rgba(10,90,210,.95);
        box-shadow:0 1px 7px rgba(0,0,0,.4);pointer-events:none;left:50%;top:50%;opacity:0;
        transition:transform .07s ease,background .07s ease}
      .__demo-cursor.__down{transform:scale(.55);background:rgba(255,70,70,.55);border-color:rgba(200,0,0,.98)}
      .__demo-ripple{position:fixed;z-index:2147483646;width:16px;height:16px;margin:-8px 0 0 -8px;
        border-radius:50%;border:3px solid rgba(20,120,255,.85);pointer-events:none;
        animation:__demoR .55s ease-out forwards}
      @keyframes __demoR{from{transform:scale(1);opacity:.95}to{transform:scale(4.5);opacity:0}}
      .__demo-keys{position:fixed;z-index:2147483647;bottom:40px;left:50%;transform:translateX(-50%);
        display:flex;gap:8px;pointer-events:none}
      .__demo-key{background:rgba(18,18,20,.90);color:#fff;font:600 20px/1 -apple-system,system-ui,sans-serif;
        padding:13px 16px;border-radius:10px;box-shadow:0 3px 12px rgba(0,0,0,.5);
        animation:__demoK .12s ease-out}
      @keyframes __demoK{from{transform:scale(.7);opacity:0}to{transform:scale(1);opacity:1}}
      .__demo-title{position:fixed;z-index:2147483647;top:84px;left:50%;transform:translateX(-50%);
        background:rgba(8,42,92,.94);color:#fff;font:700 27px/1.25 -apple-system,system-ui,sans-serif;
        padding:15px 34px;border-radius:34px;box-shadow:0 5px 22px rgba(0,0,0,.5);
        opacity:0;transition:opacity .45s ease;pointer-events:none;max-width:78vw;text-align:center;
        letter-spacing:.2px}
    `;
    document.documentElement.appendChild(style);
    const cur = document.createElement('div');
    cur.className = '__demo-cursor';
    cur.id = '__demo_cursor';
    document.documentElement.appendChild(cur);
    let box;
    // Public API — used by THIS frame and forwarded from same-origin child frames.
    window.__demoCursor = (x, y) => { cur.style.opacity = '1'; cur.style.left = x + 'px'; cur.style.top = y + 'px'; };
    window.__demoDown = (x, y, down) => {
      if (down) {
        cur.classList.add('__down');
        const r = document.createElement('div'); r.className = '__demo-ripple';
        r.style.left = x + 'px'; r.style.top = y + 'px';
        document.documentElement.appendChild(r); setTimeout(() => r.remove(), 560);
      } else {
        cur.classList.remove('__down');
      }
    };
    window.__demoKey = (txt) => {
      if (!box) { box = document.createElement('div'); box.className = '__demo-keys'; document.documentElement.appendChild(box); }
      const k = document.createElement('div'); k.className = '__demo-key'; k.textContent = txt;
      box.appendChild(k); setTimeout(() => k.remove(), 750);
    };
    let titleEl, titleTo;
    window.__demoTitle = (txt, ms) => {
      if (!titleEl) { titleEl = document.createElement('div'); titleEl.className = '__demo-title'; document.documentElement.appendChild(titleEl); }
      titleEl.textContent = txt;
      titleEl.style.opacity = '1';
      clearTimeout(titleTo);
      titleTo = setTimeout(() => { titleEl.style.opacity = '0'; }, ms || 2600);
    };
  };

  // Offset of this frame inside the top frame (sum of ancestor frame rects).
  const topOffset = () => {
    let x = 0, y = 0, w = window;
    try {
      while (w !== window.top && w.frameElement) {
        const r = w.frameElement.getBoundingClientRect();
        x += r.left; y += r.top;
        w = w.parent;
      }
    } catch (e) { /* cross-origin ancestor: best effort */ }
    return { x, y };
  };

  const callTop = (fn, ...args) => { try { if (topWin[fn]) topWin[fn](...args); } catch (e) { /* ignore */ } };

  const wireEvents = () => {
    addEventListener('mousemove', e => { const o = topOffset(); callTop('__demoCursor', e.clientX + o.x, e.clientY + o.y); }, true);
    addEventListener('mousedown', e => { const o = topOffset(); callTop('__demoDown', e.clientX + o.x, e.clientY + o.y, true); }, true);
    addEventListener('mouseup', () => callTop('__demoDown', 0, 0, false), true);
    addEventListener('keydown', e => {
      let label = e.key === ' ' ? 'Space' : e.key;
      const mods = [];
      if (e.ctrlKey && e.key !== 'Control') mods.push('Ctrl');
      if (e.metaKey && e.key !== 'Meta') mods.push('Cmd');
      if (e.altKey && e.key !== 'Alt') mods.push('Alt');
      callTop('__demoKey', mods.length ? mods.join('+') + '+' + label : label);
    }, true);
  };

  const boot = () => { if (isTop) installTop(); wireEvents(); };
  if (document.body) boot();
  else addEventListener('DOMContentLoaded', boot);
})();
