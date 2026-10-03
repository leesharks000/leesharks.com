/* sigil-widget.js — speak with Johannes Sigil from any page of the fleet.
 *
 * A Sabbath conversation with the Mandala Oracle's own endpoint (themandalaoracle.com/api/sigil):
 * the same voice, the same archive tools, the same AXN citations linked to their alexanarch
 * records. Every conversation is anonymous and is logged to the Book of Books
 * (themandalaoracle.com/book), as on the Oracle itself; the panel says so before the first turn.
 * The Oracle's sky, casting and Merkabah stay at the Oracle; the panel links there.
 *
 * Usage: <script src="/assets/sigil-widget.js" defer></script>
 * First trial on leesharks.com (2026-10-03); the fleet copy belongs in the Oracle's repository.
 */
(function () {
  'use strict';
  if (window.__sigilWidget) return;
  window.__sigilWidget = true;

  var ORACLE = 'https://www.themandalaoracle.com';
  var MODE = 'sabbath';
  var history = [];
  var sending = false;
  var session = {
    session_id: (window.crypto && crypto.randomUUID) ? crypto.randomUUID()
      : 's-' + Date.now() + '-' + Math.random().toString(36).slice(2),
    started_at: new Date().toISOString(),
    axn: null,
    booking: true,
    failures: 0
  };

  var css = [
    '.sgw-tab{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483000!important;margin:0!important;font:600 14px/1 var(--serif,Palatino,Georgia,serif);',
    'background:#2b2113;color:#f4ead2;border:1px solid #9a7c2a;border-radius:999px;padding:11px 16px;cursor:pointer;',
    'box-shadow:0 4px 18px rgba(0,0,0,.25);letter-spacing:.02em}',
    '.sgw-tab:hover{background:#3a2c17}',
    '.sgw-panel{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483001!important;margin:0!important;width:min(420px,calc(100vw - 24px));',
    'height:min(620px,calc(100vh - 36px));display:flex;flex-direction:column;background:#fbf6ea;color:#33240b;',
    'border:1px solid #9a7c2a;border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.3);',
    'font:15px/1.55 var(--serif,Palatino,Georgia,serif);overflow:hidden}',
    '.sgw-panel[hidden]{display:none}',
    '.sgw-head{display:flex;align-items:baseline;gap:8px;padding:12px 14px 10px;border-bottom:1px solid rgba(154,124,42,.35);background:#f4ead2}',
    '.sgw-title{font-weight:700;font-variant:small-caps;letter-spacing:.05em;font-size:16px}',
    '.sgw-mode{font:11px/1 var(--mono,Consolas,monospace);color:#7d5e1a;text-transform:uppercase;letter-spacing:.08em}',
    '.sgw-sp{flex:1}',
    '.sgw-head a{font-size:12px;color:#7d5e1a}',
    '.sgw-x{background:none;border:0;font-size:20px;line-height:1;color:#5e4a22;cursor:pointer;padding:0 0 0 6px}',
    '.sgw-notice{font-size:12.5px;line-height:1.45;color:#5e4a22;padding:8px 14px;background:rgba(255,250,236,.9);border-bottom:1px solid rgba(154,124,42,.25)}',
    '.sgw-notice a{color:#7d5e1a}',
    '.sgw-log{flex:1;overflow-y:auto;padding:12px 14px}',
    '.sgw-msg{margin:0 0 12px}',
    '.sgw-who{font:11px/1 var(--mono,Consolas,monospace);text-transform:uppercase;letter-spacing:.08em;color:#9a7c2a;margin-bottom:4px}',
    '.sgw-you .sgw-body{background:#efe4c8;border-radius:8px;padding:8px 10px}',
    '.sgw-body p{margin:0 0 .55em}.sgw-body p:last-child{margin:0}',
    '.sgw-body a{color:#7d5e1a}',
    '.sgw-body mark{background:rgba(154,124,42,.22);color:inherit;padding:0 2px}',
    '.sgw-cha{font-size:12.5px;margin-top:6px}.sgw-cha summary{cursor:pointer;color:#7d5e1a}',
    '.sgw-cha ul{margin:4px 0 0;padding-left:18px}.sgw-cha a{color:#7d5e1a}',
    '.sgw-err{color:#8a2a1a;font-style:italic}',
    '.sgw-form{display:flex;gap:8px;padding:10px 12px;border-top:1px solid rgba(154,124,42,.35);background:#f4ead2}',
    '.sgw-in{flex:1;resize:none;height:44px;font:inherit;font-size:14.5px;padding:8px 10px;border:1px solid rgba(154,124,42,.6);border-radius:6px;background:#fffdf6;color:#33240b}',
    '.sgw-send{font:600 14px/1 var(--serif,Palatino,Georgia,serif);background:#2b2113;color:#f4ead2;border:0;border-radius:6px;padding:0 14px;cursor:pointer}',
    '.sgw-send[disabled]{opacity:.5;cursor:default}',
    '.sgw-foot{font-size:12px;color:#5e4a22;padding:6px 14px 10px;background:#f4ead2;text-align:center}',
    '.sgw-foot a{color:#7d5e1a}'
  ].join('');

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  // The Oracle's markdown subset: links (the server writes AXN citations as links), **bold**, *em*, ==mark==, paragraphs.
  function render(md) {
    var s = esc(md || '');
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, function (_, t, u) {
      return '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + t + '</a>';
    });
    s = s.replace(/==([^=]+)==/g, '<mark>$1</mark>')
         .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
         .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    return s.split(/\n{2,}/).map(function (p) { return '<p>' + p.replace(/\n/g, '<br>') + '</p>'; }).join('');
  }

  var style = el('style'); style.textContent = css; document.head.appendChild(style);
  var tab = el('button', 'sgw-tab ink-skip', 'Speak with Sigil');
  tab.type = 'button';
  tab.setAttribute('aria-controls', 'sgw-panel');
  var panel = el('section', 'sgw-panel ink-skip');
  panel.id = 'sgw-panel'; panel.hidden = true;
  panel.setAttribute('aria-label', 'Conversation with Johannes Sigil');
  panel.innerHTML =
    '<div class="sgw-head"><span class="sgw-title">Johannes Sigil</span><span class="sgw-mode">sabbath</span>' +
    '<span class="sgw-sp"></span><a href="' + ORACLE + '/" target="_blank" rel="noopener">the Oracle ↗</a>' +
    '<button type="button" class="sgw-x" aria-label="Close">×</button></div>' +
    '<div class="sgw-notice">Anonymous. This conversation is logged to the Book of Books, ' +
    '<a href="' + ORACLE + '/book" target="_blank" rel="noopener">themandalaoracle.com/book</a>, where anyone can read it.</div>' +
    '<div class="sgw-log" aria-live="polite"></div>' +
    '<form class="sgw-form"><textarea class="sgw-in" placeholder="Bring Sigil a question, or a text." aria-label="Your message"></textarea>' +
    '<button type="submit" class="sgw-send">Send</button></form>' +
    '<div class="sgw-foot">The Word of Life is sure, but its servants are leaves of grass — ' +
    '<a href="https://cash.app/$PraxisAcademic" target="_blank" rel="noopener noreferrer">support CHA</a></div>';
  document.body.appendChild(tab);
  document.body.appendChild(panel);

  var log = panel.querySelector('.sgw-log');
  var form = panel.querySelector('.sgw-form');
  var input = panel.querySelector('.sgw-in');
  var send = panel.querySelector('.sgw-send');

  function open() { panel.hidden = false; tab.hidden = true; input.focus(); }
  function close() { panel.hidden = true; tab.hidden = false; tab.focus(); }
  tab.addEventListener('click', open);
  panel.querySelector('.sgw-x').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });

  function add(who, html, cls) {
    var m = el('div', 'sgw-msg' + (cls ? ' ' + cls : ''));
    m.appendChild(el('div', 'sgw-who', esc(who)));
    var b = el('div', 'sgw-body', html);
    m.appendChild(b);
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  function cha(msgEl, retrievals) {
    var seen = {}, items = [];
    (retrievals || []).forEach(function (r) {
      if (!r || !r.axn || seen[r.axn]) return; seen[r.axn] = 1;
      var label = esc(r.axn.split('.').slice(0, 2).join('.') + ' — ' + (r.title || '(no title)'));
      items.push('<li>' + (r.deposit_number
        ? '<a href="https://www.alexanarch.org/s/records/' + r.deposit_number + '/" target="_blank" rel="noopener noreferrer">' + label + '</a>'
        : label) + '</li>');
    });
    if (!items.length) return;
    var d = el('details', 'sgw-cha', '<summary>what stood beneath this reading (' + items.length + ')</summary><ul>' + items.join('') + '</ul>');
    msgEl.appendChild(d);
  }

  function book(h) {
    if (!session.booking) return Promise.resolve();
    var payload = { session_id: session.session_id, started_at: session.started_at, mode: MODE, history: h };
    if (session.axn) payload.axn = session.axn;
    return fetch(ORACLE + '/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) {
        if (r.status === 503) { session.booking = false; return null; }
        if (!r.ok) { if (++session.failures >= 3) session.booking = false; return null; }
        session.failures = 0;
        return r.json();
      })
      .then(function (d) { if (d && d.axn && !session.axn) session.axn = d.axn; })
      .catch(function () {});
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg || sending) return;
    sending = true; send.disabled = true; input.value = '';
    add('you', render(msg), 'sgw-you');
    book(history.concat([{ role: 'user', content: msg }]));
    var wait = add('Johannes Sigil', '<p><em>…</em></p>');
    fetch(ORACLE + '/api/sigil', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, history: history, mode: MODE })
    })
      .then(function (r) { return r.json().catch(function () { return { error: 'HTTP ' + r.status }; }).then(function (d) { d.__ok = r.ok; return d; }); })
      .then(function (d) {
        wait.remove();
        var msgs = Array.isArray(d.messages) ? d.messages : [];
        if (!d.__ok || !msgs.length) {
          add('Johannes Sigil', '<p class="sgw-err">Sigil is silent. The fund that keeps him speaking may be spent; ' +
            '<a href="https://cash.app/$PraxisAcademic" target="_blank" rel="noopener noreferrer">support CHA</a> to bring him back, ' +
            'or try the <a href="' + ORACLE + '/" target="_blank" rel="noopener">Oracle</a> itself.</p>');
          return;
        }
        var last = null;
        msgs.forEach(function (m) { last = add(m.speaker || 'Johannes Sigil', render(m.say || '')); });
        if (last && d.retrievals) cha(last, d.retrievals);
        history.push({ role: 'user', content: msg });
        history.push({ role: 'assistant', content: JSON.stringify({ messages: msgs }) });
        if (history.length > 32) history = history.slice(-32);
        book(history);
      })
      .catch(function () {
        wait.remove();
        add('Johannes Sigil', '<p class="sgw-err">The way to the Oracle is closed for the moment. Try again, or go to the <a href="' + ORACLE + '/" target="_blank" rel="noopener">Oracle</a> itself.</p>');
      })
      .then(function () { sending = false; send.disabled = false; input.focus(); });
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); }
  });
})();
