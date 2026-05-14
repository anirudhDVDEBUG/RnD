(function () {
  'use strict';

  const editor = document.getElementById('editor');
  const iframe = document.getElementById('preview');
  const allowListContainer = document.getElementById('allow-list-tags');
  const originInput = document.getElementById('origin-input');
  const cspDisplay = document.getElementById('csp-display');
  const logOutput = document.getElementById('log-output');

  const STORAGE_KEY = 'csp-allow-list';

  const DEFAULT_HTML = `<h2>CSP Sandbox Demo</h2>
<p>This code tries to fetch from two origins. Open DevTools console to see details.</p>
<script>
async function run() {
  const el = document.getElementById('output');
  el.textContent = 'Fetching...\\n';

  // Allowed by default in the demo allow-list
  try {
    const r = await fetch('https://httpbin.org/get?demo=allowed');
    const j = await r.json();
    el.textContent += '\\nhttpbin.org => ' + j.url;
  } catch (e) {
    el.textContent += '\\nhttpbin.org => BLOCKED: ' + e.message;
  }

  // Not in the allow-list initially
  try {
    const r2 = await fetch('https://jsonplaceholder.typicode.com/todos/1');
    const j2 = await r2.json();
    el.textContent += '\\njsonplaceholder => ' + JSON.stringify(j2).slice(0, 80);
  } catch (e) {
    el.textContent += '\\njsonplaceholder => BLOCKED: ' + e.message;
  }
}
run();
<\/script>
<pre id="output" style="background:#1e1e2e;color:#cdd6f4;padding:12px;border-radius:6px;"></pre>`;

  // --- Allow-list persistence ---

  function getAllowedOrigins() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch {
      return [];
    }
  }

  function saveAllowedOrigins(list) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  }

  function addToAllowList(origin) {
    const list = getAllowedOrigins();
    if (!list.includes(origin)) {
      list.push(origin);
      saveAllowedOrigins(list);
      renderAllowListUI();
      log('Added to allow-list: ' + origin);
    }
  }

  function removeFromAllowList(origin) {
    const list = getAllowedOrigins().filter(o => o !== origin);
    saveAllowedOrigins(list);
    renderAllowListUI();
    log('Removed from allow-list: ' + origin);
  }

  function clearAllowList() {
    saveAllowedOrigins([]);
    renderAllowListUI();
    log('Allow-list cleared');
  }

  // --- UI rendering ---

  function renderAllowListUI() {
    const origins = getAllowedOrigins();
    allowListContainer.innerHTML = '';
    origins.forEach(origin => {
      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = origin;
      const btn = document.createElement('button');
      btn.textContent = '\u00d7';
      btn.title = 'Remove ' + origin;
      btn.onclick = () => {
        removeFromAllowList(origin);
        refreshPreview();
      };
      tag.appendChild(btn);
      allowListContainer.appendChild(tag);
    });
    updateCSPDisplay();
  }

  function updateCSPDisplay() {
    cspDisplay.textContent = buildCSP(getAllowedOrigins());
  }

  function log(msg) {
    const ts = new Date().toLocaleTimeString();
    logOutput.textContent = '[' + ts + '] ' + msg + '\n' + logOutput.textContent;
  }

  // --- CSP builder ---

  function buildCSP(allowedOrigins) {
    const connectSrc = allowedOrigins.length
      ? 'connect-src ' + allowedOrigins.join(' ')
      : '';
    return [
      "default-src 'none'",
      "script-src 'unsafe-inline'",
      "style-src 'unsafe-inline'",
      connectSrc
    ].filter(Boolean).join('; ');
  }

  // --- Preview ---

  function refreshPreview() {
    const html = editor.value;
    const origins = getAllowedOrigins();
    const csp = buildCSP(origins);

    // Revoke previous blob URL
    if (iframe._blobUrl) {
      URL.revokeObjectURL(iframe._blobUrl);
    }

    const wrapped = '<!DOCTYPE html><html><head>' +
      '<meta http-equiv="Content-Security-Policy" content="' + escapeAttr(csp) + '">' +
      '<script>' +
      // Patch fetch to report blocked requests to parent
      'const _fetch = window.fetch;' +
      'window.fetch = async function(url, opts) {' +
      '  try { return await _fetch(url, opts); }' +
      '  catch (err) {' +
      '    try {' +
      '      var origin = new URL(url).origin;' +
      '      window.parent.postMessage({ type: "fetch-blocked", url: String(url), origin: origin }, "*");' +
      '    } catch(e) {}' +
      '    throw err;' +
      '  }' +
      '};' +
      // Also listen for securitypolicyviolation events
      'document.addEventListener("securitypolicyviolation", function(e) {' +
      '  try {' +
      '    var origin = new URL(e.blockedURI).origin;' +
      '    window.parent.postMessage({ type: "csp-violation", blockedURI: e.blockedURI, origin: origin, directive: e.violatedDirective }, "*");' +
      '  } catch(ex) {}' +
      '});' +
      '<\/script>' +
      '</head><body>' + html + '</body></html>';

    const blob = new Blob([wrapped], { type: 'text/html' });
    const blobUrl = URL.createObjectURL(blob);
    iframe._blobUrl = blobUrl;
    iframe.src = blobUrl;
    updateCSPDisplay();
    log('Preview refreshed with CSP: ' + csp);
  }

  function escapeAttr(s) {
    return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  }

  // --- Message listener ---

  window.addEventListener('message', function (e) {
    if (!e.data || typeof e.data !== 'object') return;

    if (e.data.type === 'fetch-blocked') {
      log('BLOCKED fetch to: ' + e.data.url);
      promptAllowOrigin(e.data.origin);
    }

    if (e.data.type === 'csp-violation') {
      log('CSP violation: ' + e.data.blockedURI + ' (directive: ' + e.data.directive + ')');
      promptAllowOrigin(e.data.origin);
    }
  });

  function promptAllowOrigin(origin) {
    if (!origin || origin === 'null') return;
    if (getAllowedOrigins().includes(origin)) return;

    const allow = confirm(
      'The sandbox tried to connect to:\n\n  ' + origin + '\n\n' +
      'Add this origin to the CSP connect-src allow-list and refresh?'
    );
    if (allow) {
      addToAllowList(origin);
      refreshPreview();
    }
  }

  // --- Validate & add origin ---

  function addOriginFromInput() {
    const raw = originInput.value.trim();
    if (!raw) return;
    try {
      const url = new URL(raw.includes('://') ? raw : 'https://' + raw);
      addToAllowList(url.origin);
      originInput.value = '';
      refreshPreview();
    } catch {
      alert('Invalid origin. Enter a valid URL like https://api.example.com');
    }
  }

  // --- Wire up buttons ---

  document.getElementById('btn-refresh').onclick = refreshPreview;

  document.getElementById('btn-reset').onclick = function () {
    editor.value = DEFAULT_HTML;
    refreshPreview();
  };

  document.getElementById('btn-clear-list').onclick = function () {
    clearAllowList();
    refreshPreview();
  };

  document.getElementById('btn-add-origin').onclick = addOriginFromInput;

  originInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') addOriginFromInput();
  });

  // --- Init ---

  editor.value = DEFAULT_HTML;
  renderAllowListUI();
  refreshPreview();
})();
