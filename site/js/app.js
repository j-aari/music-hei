/* European Music Institutions with an Erasmus Charter.
   Static page: loads data/site.json, filters in the browser, no server, no cookies, no analytics.
   The map (Leaflet + OpenStreetMap tiles) is only initialised when the user opens the map view. */
(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, root = document) => root.querySelector(sel);

  function h(tag, attrs, ...kids) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === 'class') node.className = v;
      else if (k === 'text') node.textContent = v;
      else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v === true ? '' : v);
    }
    for (const kid of kids.flat()) {
      if (kid == null || kid === false) continue;
      node.append(kid.nodeType ? kid : document.createTextNode(kid));
    }
    return node;
  }

  // Search folding: case- and diacritic-insensitive ("Nurnberg" finds "Nürnberg")
  const EXTRA = { 'ø': 'o', 'æ': 'ae', 'ł': 'l', 'đ': 'd', 'ð': 'd', 'þ': 'th', 'ß': 'ss', 'ı': 'i', 'œ': 'oe' };
  const fold = (s) => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[øæłđðþßıœ]/g, (c) => EXTRA[c]);

  let meta, data, byId;
  let tierLabels = {};
  const state = { view: 'list', q: '', country: new Set(), type: new Set(), language: new Set(), partner: new Set(), id: null };
  let langNames;
  let hasPartnerData = false, hasLanguageData = false;
  let lastTrigger = null;

  const partnerKey = (i) => (i.partner_of_siba === true ? 'yes' : i.partner_of_siba === false ? 'no' : 'unknown');
  const GROUPS = {
    country: { label: 'Country', values: (i) => [i.country], text: (v) => v },
    type: { label: 'Institution type', values: (i) => [String(i.tier)], text: (v) => tierLabels[v] || v },
    language: { label: 'Language of instruction', values: (i) => i.languages_of_instruction || [], text: (v) => langName(v) },
    partner: {
      label: 'Partner status',
      values: (i) => [partnerKey(i)],
      text: (v) => ({ yes: 'Partner', no: 'Not a partner', unknown: 'Not recorded' })[v],
    },
  };
  const GROUP_ORDER = ['country', 'type', 'language', 'partner'];

  function langName(code) {
    try { return (langNames = langNames || new Intl.DisplayNames(['en'], { type: 'language' })).of(code) || code; }
    catch { return code; }
  }

  // ---------- filtering ----------
  function matchesQuery(i) {
    if (!state.q) return true;
    const hay = i._hay;
    return fold(state.q).split(/\s+/).filter(Boolean).every((t) => hay.includes(t));
  }
  // skip: a group name (or 'q') to leave out, for faceted counts and empty-state hints
  function matches(i, skip) {
    if (skip !== 'q' && !matchesQuery(i)) return false;
    for (const g of GROUP_ORDER) {
      if (g === skip || !state[g].size) continue;
      if (!GROUPS[g].values(i).some((v) => state[g].has(v))) return false;
    }
    return true;
  }
  const results = () => data.filter((i) => matches(i));
  const activeFilterCount = () => GROUP_ORDER.reduce((n, g) => n + (state[g].size ? 1 : 0), 0) + (state.q ? 1 : 0);

  // ---------- URL hash (shareable state) ----------
  function readHash() {
    const p = new URLSearchParams(location.hash.replace(/^#/, ''));
    state.view = p.get('view') === 'map' ? 'map' : 'list';
    state.q = p.get('q') || '';
    for (const g of GROUP_ORDER) {
      const valid = new Set(groupVisible(g) ? optionValues(g) : []); // hidden filters cannot be set from a link
      state[g] = new Set(p.getAll(g).filter((v) => valid.has(v)));
    }
    const id = p.get('id');
    state.id = id && byId.has(id) ? id : null;
  }
  function writeHash() {
    const p = new URLSearchParams();
    if (state.view === 'map') p.set('view', 'map');
    if (state.q) p.set('q', state.q);
    for (const g of GROUP_ORDER) for (const v of state[g]) p.append(g, v);
    if (state.id) p.set('id', state.id);
    const s = p.toString();
    history.replaceState(null, '', location.pathname + location.search + (s ? '#' + s : ''));
  }

  // ---------- filter UI (built once, counts updated on every change) ----------
  function optionValues(g) {
    const set = new Set(data.flatMap(GROUPS[g].values));
    const arr = [...set];
    if (g === 'country') return arr.sort((a, b) => a.localeCompare(b, 'en'));
    if (g === 'language') return arr.sort((a, b) => langName(a).localeCompare(langName(b), 'en'));
    if (g === 'partner') return ['yes', 'no', 'unknown'].filter((v) => set.has(v));
    return arr.sort();
  }
  const groupVisible = (g) => (g === 'language' ? hasLanguageData : g === 'partner' ? hasPartnerData : true);

  function buildFilters() {
    const host = $('#filter-groups');
    host.textContent = '';
    for (const g of GROUP_ORDER) {
      if (!groupVisible(g)) continue;
      const ul = h('ul');
      for (const v of optionValues(g)) {
        const input = h('input', { type: 'checkbox', name: g, value: v });
        input.addEventListener('change', () => {
          if (input.checked) state[g].add(v); else state[g].delete(v);
          update();
        });
        ul.append(h('li', {}, h('label', { class: 'opt', 'data-group': g, 'data-value': v }, input, h('span', { class: 'lab', text: GROUPS[g].text(v) }), h('span', { class: 'n' }))));
      }
      const fs = h('fieldset', { class: `group group--${g}` }, h('legend', { text: GROUPS[g].label }), ul);
      if (g === 'partner') fs.append(h('p', { class: 'group__source', text: `Source: ${meta.partner_source_name}.` }));
      host.append(fs);
    }
    const missing = [];
    if (!hasPartnerData) missing.push('partner status');
    if (!hasLanguageData) missing.push('languages of instruction');
    const note = $('#missing');
    if (missing.length) {
      const txt = missing.join(' and ');
      note.textContent = `${txt.charAt(0).toUpperCase() + txt.slice(1)} ${missing.length > 1 ? 'have' : 'has'} not been recorded yet.` +
        (hasPartnerData ? '' : ` Partner information will be taken from ${meta.partner_source_name}.`);
      note.hidden = false;
    } else note.hidden = true;
  }

  function updateFilters() {
    for (const label of document.querySelectorAll('.opt')) {
      const g = label.dataset.group, v = label.dataset.value;
      const n = data.filter((i) => matches(i, g) && GROUPS[g].values(i).includes(v)).length;
      $('.n', label).textContent = n;
      label.classList.toggle('is-zero', n === 0);
      $('input', label).checked = state[g].has(v);
    }
    const q = $('#q');
    if (q.value !== state.q) q.value = state.q;
    $('#clear').hidden = activeFilterCount() === 0;
  }

  // ---------- list ----------
  function glyph(i) {
    return h('span', { class: `glyph glyph--t${i.tier}${i.partner_of_siba === true ? ' glyph--partner' : ''}`, 'aria-hidden': 'true' });
  }
  function renderList(rows) {
    const host = $('#list-view');
    host.textContent = '';
    const groups = new Map();
    for (const i of rows) (groups.get(i.country) || groups.set(i.country, []).get(i.country)).push(i);
    for (const [country, items] of groups) {
      const ul = h('ul', { class: 'entries' });
      for (const i of items) {
        const btn = h('button', { type: 'button', class: 'entry', 'data-id': i.id, 'aria-current': i.id === state.id ? 'true' : false },
          glyph(i),
          h('span', { class: 'nm', text: i.name }),
          h('span', { class: 'meta' },
            h('span', { text: i.city }),
            h('span', { text: tierLabels[i.tier] }),
            i.partner_of_siba === true ? h('span', { class: 'partner', text: 'Partner' }) : null));
        btn.addEventListener('click', () => openPanel(i.id, btn));
        ul.append(h('li', {}, btn));
      }
      host.append(h('section', { class: 'country' }, h('h2', {}, country, h('span', { class: 'n', text: items.length })), ul));
    }
  }

  // ---------- map ----------
  let map, markerLayer, markerById = new Map();
  let colors;
  const palette = () => colors || (colors = Object.fromEntries(['--ink', '--paper', '--vermilion'].map((n) => [n, getComputedStyle(document.documentElement).getPropertyValue(n).trim()])));

  // Shape = institution type (dot / ring), red = exchange partner. Selection is a separate halo so it never changes a marker's colour.
  function markerStyle(i) {
    const { '--ink': ink, '--paper': paper, '--vermilion': verm } = palette();
    const partner = i.partner_of_siba === true;
    const accent = partner ? verm : ink;
    const ring = i.tier === 2;
    return {
      radius: partner ? 7 : 5.5,
      color: ring ? accent : paper,
      weight: ring ? 2.5 : 1.5,
      fillColor: ring ? paper : accent,
      fillOpacity: 1,
    };
  }
  function initMap() {
    map = L.map('map', { minZoom: 3, maxZoom: 17, zoomAnimation: !reduceMotion, fadeAnimation: !reduceMotion, markerZoomAnimation: !reduceMotion })
      .setView([50, 12], 4);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
    markerLayer = L.layerGroup().addTo(map);
  }
  function renderMap(rows, fit) {
    if (!map) initMap();
    map.invalidateSize(); // the container was hidden until now
    markerLayer.clearLayers();
    markerById.clear();
    const pts = [];
    // Partners last so they sit on top
    const ordered = [...rows].sort((a, b) => (a.partner_of_siba === true) - (b.partner_of_siba === true));
    for (const i of ordered) {
      if (i.lat == null) continue;
      const m = L.circleMarker([i.lat, i.lon], markerStyle(i));
      m.bindTooltip(i.name, { direction: 'top', offset: [0, -6] });
      m.on('click', () => openPanel(i.id, null));
      m.addTo(markerLayer);
      markerById.set(i.id, m);
      pts.push([i.lat, i.lon]);
    }
    if (fit && pts.length) map.fitBounds(pts, { padding: [40, 40], maxZoom: 9, animate: !reduceMotion });
    highlightMarker();
  }
  let halo = null;
  function highlightMarker() {
    if (halo) { halo.remove(); halo = null; }
    const m = markerById.get(state.id);
    if (!m || !map) return;
    halo = L.circleMarker(m.getLatLng(), { radius: 13, color: palette()['--ink'], weight: 2, fill: false, interactive: false }).addTo(map);
    m.bringToFront();
  }

  // ---------- details panel ----------
  function addressLines(i) {
    return [i.street, [i.postal_code, i.city].filter(Boolean).join(' '), i.country].filter(Boolean);
  }
  function openPanel(id, trigger) {
    const i = byId.get(id);
    if (!i) return;
    state.id = id;
    lastTrigger = trigger;
    const body = $('#panel-body');
    body.textContent = '';
    const dl = h('dl');
    const row = (dt, ...dd) => { dl.append(h('dt', { text: dt }), h('dd', {}, ...dd)); };

    row('Institution type', glyph(i), tierLabels[i.tier]);
    const addr = h('span');
    addressLines(i).forEach((l, k) => { if (k) addr.append(h('br')); addr.append(l); });
    row('Address', addr);
    row('Erasmus code', i.erasmus_code);
    if (i.oid) row('OID', i.oid);
    if (i.website) {
      let host = i.website;
      try { host = new URL(i.website).hostname.replace(/^www\./, ''); } catch { /* keep raw */ }
      row('Website', h('a', { href: i.website, target: '_blank', rel: 'noopener noreferrer' }, host, h('span', { class: 'sr-only', text: ' (opens in a new tab)' })));
    }
    if (hasLanguageData) row('Languages of instruction', i.languages_of_instruction && i.languages_of_instruction.length ? i.languages_of_instruction.map(langName).join(', ') : 'Not recorded');
    if (hasPartnerData) {
      const label = GROUPS.partner.text(partnerKey(i));
      row('Partner status', label);
      dl.lastChild.append(h('p', { class: 'small', text: `Source: ${meta.partner_source_name}.` }));
    }
    if (i.name_upstream) row('Name in the ECHE list', i.name_upstream);

    const title = h('h2', { class: 'panel__title', id: 'panel-title', tabindex: '-1', text: i.name });
    const sub = h('p', { class: 'panel__sub', text: `${i.city}, ${i.country}` });
    body.append(title, sub, dl);
    if (i.public_note) body.append(h('p', { class: 'note', text: i.public_note }));
    if (i.geo_precision === 'city') body.append(h('p', { class: 'small', text: 'Map position is approximate (city centre).' }));
    if (state.view === 'list' && i.lat != null && matches(i)) {
      body.append(h('p', { class: 'actions' }, h('button', { type: 'button', class: 'btn', onclick: () => { setView('map'); focusMarker(i); }, text: 'Show on map' })));
    }

    $('#panel').hidden = false;
    $('#layout').classList.add('has-panel');
    for (const b of document.querySelectorAll('.entry')) b.setAttribute('aria-current', b.dataset.id === id ? 'true' : 'false');
    if (map && state.view === 'map') { highlightMarker(); const m = markerById.get(id); if (m && !map.getBounds().contains(m.getLatLng())) map.panTo(m.getLatLng(), { animate: !reduceMotion }); }
    writeHash();
    title.focus({ preventScroll: true });
  }
  function closePanel() {
    state.id = null;
    $('#panel').hidden = true;
    $('#layout').classList.remove('has-panel');
    for (const b of document.querySelectorAll('.entry')) b.setAttribute('aria-current', 'false');
    if (map) highlightMarker();
    writeHash();
    const target = lastTrigger && document.contains(lastTrigger) && !lastTrigger.closest('[hidden]') ? lastTrigger : $('#results');
    target.focus({ preventScroll: true });
    lastTrigger = null;
  }
  function focusMarker(i) {
    const m = markerById.get(i.id);
    if (m && map) { map.setView(m.getLatLng(), Math.max(map.getZoom(), 8), { animate: !reduceMotion }); highlightMarker(); }
  }

  // ---------- views, counts, empty state, CSV ----------
  function setView(v) {
    state.view = v;
    update({ fit: true });
  }

  function renderEmpty() {
    const box = $('#empty');
    box.textContent = '';
    const active = [];
    if (state.q) active.push({ key: 'q', label: `Search "${state.q}"` });
    for (const g of GROUP_ORDER) if (state[g].size) active.push({ key: g, label: `${GROUPS[g].label}: ${[...state[g]].map((v) => GROUPS[g].text(v)).join(', ')}` });
    const hints = active.map((a) => ({ ...a, n: data.filter((i) => matches(i, a.key)).length })).sort((a, b) => b.n - a.n);
    box.append(h('h2', { text: 'No institutions match your filters' }));
    if (hints.length && hints[0].n > 0) {
      box.append(h('p', { text: `${hints.length > 1 ? 'The combination of filters leaves nothing. ' : ''}Removing “${hints[0].label}” would show ${hints[0].n} ${hints[0].n === 1 ? 'institution' : 'institutions'}.` }));
    }
    const ul = h('ul');
    for (const a of hints) {
      ul.append(h('li', {}, h('button', {
        type: 'button', class: 'btn',
        onclick: () => { if (a.key === 'q') state.q = ''; else state[a.key].clear(); update({ fit: true }); },
        text: `Remove: ${a.label}${a.n ? ` (${a.n})` : ''}`,
      })));
    }
    box.append(ul);
    if (hints.length > 1) box.append(h('button', { type: 'button', class: 'btn', onclick: clearAll, text: 'Clear all filters' }));
  }

  const plural = (n) => `${n} ${n === 1 ? 'institution' : 'institutions'}`;

  function csvCell(v) {
    let s = v == null ? '' : String(v);
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // neutralise spreadsheet formulas
    return '"' + s.replace(/"/g, '""') + '"';
  }
  function downloadCsv() {
    const rows = results();
    const cols = ['Name', 'Country', 'City', 'Address', 'Postal code', 'Erasmus code', 'OID', 'Website', 'Institution type'];
    if (hasLanguageData) cols.push('Languages of instruction');
    if (hasPartnerData) cols.push('Partner status');
    cols.push('Note');
    const lines = [cols.map(csvCell).join(',')];
    for (const i of rows) {
      const r = [i.name, i.country, i.city, i.street, i.postal_code, i.erasmus_code, i.oid, i.website, tierLabels[i.tier]];
      if (hasLanguageData) r.push((i.languages_of_instruction || []).map(langName).join('; '));
      if (hasPartnerData) r.push(GROUPS.partner.text(partnerKey(i)));
      r.push(i.public_note);
      lines.push(r.map(csvCell).join(','));
    }
    const blob = new Blob([String.fromCharCode(0xFEFF) + lines.join('\r\n') + '\r\n'], { type: 'text/csv;charset=utf-8' });
    const a = h('a', { href: URL.createObjectURL(blob), download: `european-music-institutions-${new Date().toISOString().slice(0, 10)}.csv` });
    document.body.append(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  function clearAll() {
    state.q = '';
    for (const g of GROUP_ORDER) state[g].clear();
    update({ fit: true });
  }

  function renderLegend() {
    const lg = $('#legend');
    lg.textContent = '';
    const item = (cls, text) => h('span', {}, h('span', { class: `glyph ${cls}` }), text);
    lg.append(item('glyph--t1', tierLabels[1]), item('glyph--t2', tierLabels[2]));
    if (hasPartnerData) lg.append(item('glyph--partner', 'Exchange partner (red)'));
  }

  function update(opts = {}) {
    const rows = results();
    const total = data.length;
    $('#count').textContent = rows.length === total ? plural(total) : `${rows.length} of ${plural(total)}`;
    const csv = $('#csv');
    csv.textContent = `Download ${plural(rows.length)} as CSV`;
    csv.disabled = rows.length === 0;
    for (const b of document.querySelectorAll('.view-toggle .btn')) b.setAttribute('aria-pressed', String(b.dataset.view === state.view));
    updateFilters();

    const isMap = state.view === 'map';
    $('#list-view').hidden = isMap;
    $('#map-view').hidden = !isMap;
    $('#empty').hidden = rows.length > 0;
    if (rows.length === 0) renderEmpty();

    if (isMap) renderMap(rows, opts.fit !== false);
    else renderList(rows);
    writeHash();
  }

  // ---------- footer ----------
  function renderFooter() {
    const f = $('#footer');
    const d = new Date(meta.fetched + 'T00:00:00');
    const when = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
    f.append(
      h('p', { text: meta.disclaimer }),
      h('p', { text: meta.partner_source }),
      h('p', {}, `Institution data: the list of Erasmus Charter for Higher Education holders published by the European Commission, retrieved on ${when} through the `,
        h('a', { href: 'https://eche-list.erasmuswithoutpaper.eu/openapi' }, 'ECHE List API'),
        ' of the European University Foundation. Which institutions count as music institutions is our own classification; map positions are geocoded with Nominatim and may be approximate.'),
      h('p', { text: 'No cookies and no analytics. Opening the map loads map tiles from OpenStreetMap.' }));
  }

  // ---------- init ----------
  async function init() {
    let json;
    try {
      const res = await fetch('data/site.json', { cache: 'no-cache' });
      if (!res.ok) throw new Error(res.status);
      json = await res.json();
    } catch (e) {
      $('#main').prepend(h('p', { class: 'error', role: 'alert', text: 'The list of institutions could not be loaded. Please reload the page.' }));
      return;
    }
    meta = json.meta;
    data = json.institutions;
    tierLabels = meta.tier_labels;
    byId = new Map(data.map((i) => [i.id, i]));
    // Search text also in its umlaut-transliterated form: the source data writes "Nuernberg", people type "Nurnberg"
    for (const i of data) {
      const t = fold([i.name, i.name_upstream, i.city].filter(Boolean).join(' '));
      i._hay = t + ' ' + t.replace(/ae|oe|ue/g, (m) => m[0]);
    }
    hasLanguageData = data.some((i) => i.languages_of_instruction && i.languages_of_instruction.length);
    hasPartnerData = data.some((i) => i.partner_of_siba != null);

    $('#scope').textContent = meta.scope_text;
    renderFooter();
    renderLegend();
    buildFilters();
    readHash();

    let t;
    $('#q').addEventListener('input', (e) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = e.target.value.trim(); update({ fit: true }); }, 120);
    });
    $('#filters').addEventListener('submit', (e) => e.preventDefault());
    $('#clear').addEventListener('click', clearAll);
    $('#csv').addEventListener('click', downloadCsv);
    $('#panel-close').addEventListener('click', closePanel);
    for (const b of document.querySelectorAll('.view-toggle .btn')) b.addEventListener('click', () => { if (state.view !== b.dataset.view) setView(b.dataset.view); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('#panel').hidden) closePanel(); });
    window.addEventListener('hashchange', () => { readHash(); update({ fit: true }); if (state.id) openPanel(state.id, null); });

    update({ fit: true });
    if (state.id) openPanel(state.id, null);
  }

  init();
})();
