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
  let strategiesByCode = new Map();  // erasmus_code -> document[]
  let strategiesMeta = null;         // { institutions_covered, ... } or null if the file couldn't be loaded
  let mobility = null;               // data/mobility.json, or null if the file couldn't be loaded
  let contacts = null;               // data/contacts.json, or null if the file couldn't be loaded
  let networks = null;               // data/networks.json, or null if the file couldn't be loaded
  const state = { view: 'list', sort: 'country', q: '', country: new Set(), type: new Set(), language: new Set(), partner: new Set(), strategy: new Set(), network: new Set(), id: null };
  let langNames;
  let hasPartnerData = false, hasLanguageData = false, hasStrategyData = false, hasNetworkData = false;
  let lastTrigger = null;

  const partnerKey = (i) => (i.partner_of_siba === true ? 'yes' : i.partner_of_siba === false ? 'no' : 'unknown');
  const STRATEGY_STATUS_ORDER = ['published', 'mentioned_no_link', 'not_found'];
  let strategyStatusLabels = { published: 'Published document available', mentioned_no_link: 'Mentioned but no link', not_found: 'Not found' };
  const GROUPS = {
    country: { label: 'Country', values: (i) => [i.country], text: (v) => v },
    type: { label: 'Institution type', values: (i) => [String(i.tier)], text: (v) => tierLabels[v] || v },
    language: { label: 'Language of instruction', values: (i) => i.languages_of_instruction || [], text: (v) => langName(v) },
    partner: {
      label: 'Partner status',
      values: (i) => [partnerKey(i)],
      text: (v) => ({ yes: 'Partner', no: 'Not a partner', unknown: 'Not recorded' })[v],
    },
    network: {
      label: 'Networks',
      // AEC membership is known for every institution (its whole list has been checked), so "not a member" is a real value
      values: (i) => {
        const ids = new Set(((networks && networks.memberships[i.erasmus_code]) || []).map((r) => r.network));
        return [ids.has('aec') ? 'aec' : 'not-aec', ...(ids.has('eua') ? ['eua'] : [])];
      },
      text: (v) => ({ aec: 'AEC member', 'not-aec': 'Not an AEC member', eua: 'EUA member' })[v],
    },
    strategy: {
      label: 'Strategy documents',
      // No value at all for institutions not yet checked, so they can never match once this filter is active
      values: (i) => { const s = strategyStatusOf(i.erasmus_code); return s ? [s] : []; },
      text: (v) => strategyStatusLabels[v] || v,
    },
  };
  // Country last: it is the longest list, so the short groups stay in view without scrolling the sidebar
  const GROUP_ORDER = ['type', 'strategy', 'network', 'language', 'partner', 'country'];
  let strategyStatusByCode = new Map();
  const strategyStatusOf = (code) => strategyStatusByCode.get(code) || null;

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
    state.sort = p.get('sort') === 'name' ? 'name' : 'country';
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
    if (state.sort === 'name') p.set('sort', 'name');
    if (state.q) p.set('q', state.q);
    for (const g of GROUP_ORDER) for (const v of state[g]) p.append(g, v);
    if (state.id) p.set('id', state.id);
    const s = p.toString();
    history.replaceState(null, '', location.pathname + location.search + (s ? '#' + s : ''));
    if (document.getElementById('reset')) updateReset();
  }

  // ---------- filter UI (built once, counts updated on every change) ----------
  function optionValues(g) {
    const set = new Set(data.flatMap(GROUPS[g].values));
    const arr = [...set];
    if (g === 'country') return arr.sort((a, b) => a.localeCompare(b, 'en'));
    if (g === 'language') return arr.sort((a, b) => langName(a).localeCompare(langName(b), 'en'));
    if (g === 'partner') return ['yes', 'no', 'unknown'].filter((v) => set.has(v));
    if (g === 'strategy') return STRATEGY_STATUS_ORDER; // fixed set, shown in full even when a status has zero institutions
    if (g === 'network') return ['aec', 'not-aec', 'eua'].filter((v) => set.has(v));
    return arr.sort();
  }
  const groupVisible = (g) => (g === 'language' ? hasLanguageData : g === 'partner' ? hasPartnerData : g === 'strategy' ? hasStrategyData : g === 'network' ? hasNetworkData : true);

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
    updateReset();
  }

  // The reset button is only shown while something can be reset: a filter, the search, or a selected institution
  function updateReset() {
    const filters = activeFilterCount() > 0;
    const btn = $('#reset');
    btn.hidden = !(filters || state.id);
    btn.textContent = filters ? 'Clear all filters' : 'Clear selection';
    btn.title = filters ? 'Clear the search, all filters and the selection, and return to the list' : 'Close the details of the selected institution';
  }

  // ---------- list ----------
  function glyph(i) {
    return h('span', { class: `glyph glyph--t${i.tier}${i.partner_of_siba === true ? ' glyph--partner' : ''}`, 'aria-hidden': 'true' });
  }
  function entryButton(i, showCountry) {
    const btn = h('button', { type: 'button', class: 'entry', 'data-id': i.id, 'aria-current': i.id === state.id ? 'true' : false },
      glyph(i),
      h('span', { class: 'nm', text: i.name }),
      h('span', { class: 'meta' },
        i.parent_name ? h('span', { text: i.parent_name }) : null,
        showCountry ? h('span', { text: i.country }) : null,
        h('span', { text: i.city }),
        h('span', { text: tierLabels[i.tier] }),
        i.partner_of_siba === true ? h('span', { class: 'partner', text: 'Partner' }) : null));
    btn.addEventListener('click', () => openPanel(i.id, btn));
    return btn;
  }
  function renderList(rows) {
    const host = $('#list-view');
    host.textContent = '';
    if (state.sort === 'name') {
      const ul = h('ul', { class: 'entries' });
      for (const i of [...rows].sort((a, b) => a.name.localeCompare(b.name, 'en'))) ul.append(h('li', {}, entryButton(i, true)));
      host.append(h('section', { class: 'country' }, h('h2', {}, 'All institutions, A–Z', h('span', { class: 'n', text: rows.length })), ul));
      return;
    }
    const groups = new Map();
    for (const i of rows) (groups.get(i.country) || groups.set(i.country, []).get(i.country)).push(i);
    for (const [country, items] of groups) {
      const ul = h('ul', { class: 'entries' });
      for (const i of items) ul.append(h('li', {}, entryButton(i, false)));
      host.append(h('section', { class: 'country' }, h('h2', {}, country, h('span', { class: 'n', text: items.length })), ul));
    }
  }

  // ---------- map ----------
  let map, markerLayer, markerById = new Map();
  let colors;
  const palette = () => colors || (colors = Object.fromEntries(['--ink', '--paper', '--vermilion'].map((n) => [n, getComputedStyle(document.documentElement).getPropertyValue(n).trim()])));

  // Shape = institution type (dot / ring / small dot), red = exchange partner. Selection is a separate halo so it never changes a marker's colour.
  function markerStyle(i) {
    const { '--ink': ink, '--paper': paper, '--vermilion': verm } = palette();
    const partner = i.partner_of_siba === true;
    const accent = partner ? verm : ink;
    const ring = i.tier === 2;
    return {
      radius: partner ? 7 : i.tier === 3 ? 4 : 5.5,
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

  const STRATEGY_TYPE_LABEL = {
    strategy: 'Strategy',
    'internationalisation-strategy': 'Internationalisation strategy',
    'annual-report': 'Annual report',
  };
  const isOutdated = (period) => {
    const m = /-(\d{4})$/.exec(period || '');
    return !!m && Number(m[1]) <= new Date().getFullYear();
  };
  function renderStrategySection(i) {
    const docs = strategiesByCode.get(i.erasmus_code) || [];
    const section = h('div', { class: 'panel__section' }, h('h3', { class: 'panel__section-title', text: 'Strategy documents' }));
    if (strategiesMeta) {
      section.append(h('p', { class: 'panel__coverage', text: `Strategy data covers ${strategiesMeta.institutions_covered} of ${data.length} institutions.` }));
    }
    if (!docs.length) {
      section.append(h('p', { class: 'strategy-empty', text: 'No strategy document found.' }));
      return section;
    }
    const ul = h('ul', { class: 'strategy-list' });
    for (const doc of docs) {
      const period = doc.period || (doc.publication_year ? String(doc.publication_year) : 'Year not stated');
      const outdated = isOutdated(doc.period);
      let host = doc.document_url;
      try { host = new URL(doc.document_url).hostname.replace(/^www\./, ''); } catch { /* keep raw */ }
      const isPdf = /\.pdf(?:[?#]|$)/i.test(doc.document_url || '');
      ul.append(h('li', { class: 'strategy-item' },
        h('p', { class: 'strategy-name' }, doc.name_original, outdated ? h('span', { class: 'tag-outdated', text: 'Outdated' }) : null),
        h('p', { class: 'strategy-meta', text: `${STRATEGY_TYPE_LABEL[doc.type] || doc.type} · ${period} · ${langName(doc.language)}` }),
        h('a', { href: doc.document_url, target: '_blank', rel: 'noopener noreferrer' }, host + (isPdf ? ' (PDF)' : ''),
          h('span', { class: 'sr-only', text: ' (opens in a new tab)' }))));
    }
    section.append(ul);
    return section;
  }
  // Erasmus+ mobility: scale classes only (quartiles among the music institutions on the page), never exact counts
  // 'short' (short-term student mobility) is in the data but hidden for now: most institutions have none in the data
  const MOBILITY_TYPES = ['studies', 'traineeships', 'teaching', 'training'];
  function mobilityCell(cls, key) {
    if (cls === null) return h('td', { class: 'mob-absent', text: 'No field recorded', title: 'This type appears only in rows without a field of education, so the music share cannot be told apart' });
    if (!cls) return h('td', { class: 'mob-absent', text: 'Not in data' });
    const c = mobility.meta.classes[key];
    const [lo, hi] = c.ranges[cls - 1];
    const meter = h('span', { class: 'mob-meter', 'aria-hidden': 'true' });
    for (let k = 1; k <= c.ranges.length; k++) meter.append(h('span', { class: k <= cls ? 'on' : '' }));
    return h('td', { title: `${lo}–${hi} participants` }, meter, h('span', { class: 'mob-label', text: c.labels[cls - 1] }));
  }
  function renderMobilitySection(i) {
    const m = mobility.meta;
    const [y0, y1] = m.years;
    const section = h('div', { class: 'panel__section' }, h('h3', { class: 'panel__section-title', text: `Erasmus+ mobility, ${y0}–${y1}` }));
    const rec = mobility.institutions[i.erasmus_code];
    if (i.parent_name && !rec) {
      section.append(h('p', { class: 'strategy-empty', text: 'Not shown for units inside a larger institution: the Commission’s data is recorded for the whole institution, not for its music unit.' }));
      return section;
    }
    if (!rec) {
      section.append(h('p', { class: 'strategy-empty', text: 'This institution could not be identified in the European Commission’s mobility data.' }));
      return section;
    }
    const tbody = h('tbody');
    for (const t of MOBILITY_TYPES) {
      tbody.append(h('tr', {}, h('th', { scope: 'row', text: m.types[t] }),
        mobilityCell(rec.types[t][0], `${t}.out`), mobilityCell(rec.types[t][1], `${t}.in`)));
    }
    section.append(h('table', { class: 'mob-table' },
      h('caption', { class: 'sr-only', text: `Scale of Erasmus+ mobility by type, ${y0}–${y1}` }),
      h('thead', {}, h('tr', {}, h('th', { scope: 'col', text: 'Type' }), h('th', { scope: 'col', text: 'Outgoing' }), h('th', { scope: 'col', text: 'Incoming' }))),
      tbody));
    if (rec.partners.length) {
      section.append(h('p', { class: 'mob-partners' }, h('strong', { text: 'Most frequent partner countries: ' }),
        rec.partners.map((cc) => m.country_names[cc] || cc).join(', ')));
    }
    section.append(h('p', { class: 'small', text: '“Not in data” means that this type of mobility does not appear in the Commission’s data for this institution, not that the institution does not offer it.' }));
    if (rec.music_field_only) {
      section.append(h('p', { class: 'small', text: 'Only mobility recorded in the field of music and performing arts is counted. Staff mobility is often recorded without a field, so staff figures are likely to be too low.' }));
    }
    const rows = h('tbody');
    for (const t of MOBILITY_TYPES) {
      for (const [d, dl] of [['out', 'outgoing'], ['in', 'incoming']]) {
        const c = m.classes[`${t}.${d}`];
        if (!c) continue;
        rows.append(h('tr', {}, h('th', { scope: 'row', text: `${m.types[t]}, ${dl}` }),
          ...c.ranges.map((r, k) => h('td', { text: r ? `${c.labels[k]} ${r[0]}–${r[1]} (${c.institutions[k]})` : `${c.labels[k]} —` }))));
      }
    }
    section.append(h('details', { class: 'mob-scale' },
      h('summary', { text: 'How the scale is defined' }),
      h('p', { text: `Participants over ${y0}–${y1}, outgoing and incoming counted separately. The classes are the quartiles (for traineeships, whose numbers are small, the thirds) of the music institutions on this page in whose data the type appears; the number of institutions in each class is in brackets. The latest years are left out because the Commission publishes final figures only once a project has closed.` }),
      h('div', { class: 'table-wrap' }, h('table', { class: 'mob-ranges' },
        h('thead', {}, h('tr', {}, h('th', { scope: 'col', text: 'Type' }), h('th', { scope: 'col', colspan: 4, text: 'Classes: participants (institutions)' }))),
        rows))));
    return section;
  }
  // Networks: discipline networks first, then umbrella organisations. Only mapped networks can show a membership,
  // so the coverage line names the networks that have not been mapped yet.
  const NETWORK_GROUPS = [['discipline', 'Discipline networks'], ['umbrella', 'Umbrella organisations']];
  function renderNetworksSection(i) {
    const section = h('div', { class: 'panel__section' }, h('h3', { class: 'panel__section-title', text: 'Networks' }));
    const netById = new Map(networks.networks.map((n) => [n.id, n]));
    const names = (list) => list.map((n) => n.name.split(' – ')[0]).join(', ');
    const mapped = networks.networks.filter((n) => n.mapped);
    const notYet = networks.networks.filter((n) => !n.mapped);
    section.append(h('p', { class: 'panel__coverage', text: `Membership lists checked: ${names(mapped)}.` + (notYet.length ? ` Not yet checked: ${names(notYet)}.` : '') }));
    const recs = (networks.memberships[i.erasmus_code] || []).filter((r) => netById.has(r.network));
    if (!recs.length) {
      section.append(h('p', { class: 'strategy-empty', text: 'No network memberships recorded' }));
      return section;
    }
    for (const [type, label] of NETWORK_GROUPS) {
      const inGroup = recs.filter((r) => netById.get(r.network).type === type);
      if (!inGroup.length) continue;
      const ul = h('ul', { class: 'network-list' });
      for (const r of inGroup) {
        const n = netById.get(r.network);
        ul.append(h('li', {},
          h('p', { class: 'network-name' }, h('a', { href: n.url, target: '_blank', rel: 'noopener noreferrer' }, n.name, h('span', { class: 'sr-only', text: ' (opens in a new tab)' })),
            r.category && r.category !== 'Active member' && r.category !== 'Full member' ? h('span', { class: 'network-cat', text: r.category }) : null),
          h('p', { class: 'network-desc', text: n.description })));
      }
      section.append(h('h4', { class: 'network-group', text: label }), ul);
    }
    return section;
  }
  // Copy buttons for the two values that go into agreements: the institution's name and its Erasmus code
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); return true; } catch { /* fall back below */ }
    const ta = h('textarea', { class: 'sr-only', 'aria-hidden': 'true' });
    ta.value = text;
    document.body.append(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch { ok = false; }
    ta.remove();
    return ok;
  }
  function copyButton(text, what) {
    const status = h('span', { class: 'sr-only', role: 'status', 'aria-live': 'polite' });
    const btn = h('button', { type: 'button', class: 'copy-btn', title: `Copy ${what}`, 'aria-label': `Copy ${what}` }, 'Copy');
    btn.addEventListener('click', async () => {
      const ok = await copyText(text);
      btn.textContent = ok ? 'Copied' : 'Copy failed';
      status.textContent = ok ? `${what} copied` : `Could not copy the ${what}`;
      clearTimeout(btn._t);
      btn._t = setTimeout(() => { btn.textContent = 'Copy'; status.textContent = ''; }, 1600);
    });
    return h('span', { class: 'copy-wrap' }, btn, status);
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
    if (i.parent_name) row('Part of', i.parent_name, copyButton(i.parent_name, 'name of the parent institution'), h('p', { class: 'small', text: 'The Erasmus Charter is held by this parent institution.' }));
    const addr = h('span');
    addressLines(i).forEach((l, k) => { if (k) addr.append(h('br')); addr.append(l); });
    row('Address', addr);
    if (contacts) {
      const c = contacts.contacts[i.erasmus_code];
      if (c && c.email) row('International office', h('a', { href: `mailto:${c.email}` }, c.email));
      else if (c && c.page) {
        let host = c.page;
        try { host = new URL(c.page).hostname.replace(/^www\./, ''); } catch { /* keep raw */ }
        row('International office', h('a', { href: c.page, target: '_blank', rel: 'noopener noreferrer' }, `Contact page (${host})`, h('span', { class: 'sr-only', text: ' (opens in a new tab)' })));
      } else row('International office', h('span', { class: 'muted', text: i.parent_name ? 'Not collected yet for this unit' : 'No general address found on the website' }));
    }
    // Shown exactly as in the Commission's list, spaces included ("A  WIEN08"), because that is the form used in agreements
    row('Erasmus code', h('span', { class: 'code', text: i.erasmus_code }), copyButton(i.erasmus_code, 'Erasmus code'));
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
    if (i.name_upstream) {
      row('Name in the ECHE list', h('span', { class: 'eche-name', text: i.name_upstream }));
      dl.lastChild.previousSibling.classList.add('dt-quiet');
    }

    const title = h('div', { class: 'panel__title-row' }, h('h2', { class: 'panel__title', id: 'panel-title', tabindex: '-1', text: i.name }), copyButton(i.name, 'name'));
    const sub = h('p', { class: 'panel__sub', text: `${i.city}, ${i.country}` });
    body.append(title, sub, dl);
    if (i.public_note) body.append(h('p', { class: 'note', text: i.public_note }));
    if (i.geo_precision === 'city') body.append(h('p', { class: 'small', text: 'Map position is approximate (city centre).' }));
    body.append(renderStrategySection(i));
    if (mobility) body.append(renderMobilitySection(i));
    if (networks) body.append(renderNetworksSection(i));
    if (state.view === 'list' && i.lat != null && matches(i)) {
      body.append(h('p', { class: 'actions' }, h('button', { type: 'button', class: 'btn', onclick: () => { setView('map'); focusMarker(i); }, text: 'Show on map' })));
    }

    $('#panel').hidden = false;
    $('#layout').classList.add('has-panel');
    for (const b of document.querySelectorAll('.entry')) b.setAttribute('aria-current', b.dataset.id === id ? 'true' : 'false');
    if (map && state.view === 'map') { highlightMarker(); const m = markerById.get(id); if (m && !map.getBounds().contains(m.getLatLng())) map.panTo(m.getLatLng(), { animate: !reduceMotion }); }
    writeHash();
    $('#panel-title').focus({ preventScroll: true });
  }
  function hidePanel() {
    state.id = null;
    $('#panel').hidden = true;
    $('#layout').classList.remove('has-panel');
    for (const b of document.querySelectorAll('.entry')) b.setAttribute('aria-current', 'false');
    if (map) highlightMarker();
  }
  function closePanel() {
    hidePanel();
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
    if (hints.length > 1) box.append(h('button', { type: 'button', class: 'btn', onclick: resetAll, text: 'Clear all filters' }));
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

  // Back to the initial state: no search, no filters, no selection, list view, empty URL hash
  function resetAll() {
    hidePanel();
    lastTrigger = null;
    state.q = '';
    for (const g of GROUP_ORDER) state[g].clear();
    state.view = 'list';
    state.sort = 'country';
    update({ fit: true }); // also clears the URL hash
  }

  function renderLegend() {
    const lg = $('#legend');
    lg.textContent = '';
    const item = (cls, text) => h('span', {}, h('span', { class: `glyph ${cls}` }), text);
    lg.append(item('glyph--t1', tierLabels[1]), item('glyph--t2', tierLabels[2]));
    if (data.some((i) => i.tier === 3)) lg.append(item('glyph--t3', tierLabels[3]));
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
    $('#sort-toggle').hidden = isMap; // sort order only affects the list
    for (const b of document.querySelectorAll('.sort-toggle .btn')) b.setAttribute('aria-pressed', String(b.dataset.listSort === state.sort));
    $('#empty').hidden = rows.length > 0;
    if (rows.length === 0) renderEmpty();

    const covNote = $('#strategy-coverage');
    if (state.strategy.size && strategiesMeta) {
      covNote.textContent = `Strategy data covers ${strategiesMeta.institutions_covered} of ${data.length} institutions — filtering shows only what has been checked.`;
      covNote.hidden = false;
    } else covNote.hidden = true;

    if (isMap) renderMap(rows, opts.fit !== false);
    else renderList(rows);
    writeHash();
  }

  // ---------- optional data files ----------
  async function fetchJson(url) {
    try {
      const res = await fetch(url, { cache: 'no-cache' });
      return res.ok ? await res.json() : null;
    } catch { return null; }
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
      ...(mobility ? [h('p', {}, `Erasmus+ mobility: ${mobility.meta.source}, `, h('a', { href: mobility.meta.source_url }, 'Erasmus+ Mobility Raw Data'),
        `, mobility periods started ${mobility.meta.years[0]}–${mobility.meta.years[1]}. Institutions are matched to the data by name, because the data has no Erasmus codes.`)] : []),
      h('p', { text: 'No cookies and no analytics. Opening the map view loads map tiles from OpenStreetMap.' }));
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
      const t = fold([i.name, i.name_upstream, i.parent_name, i.city].filter(Boolean).join(' '));
      i._hay = t + ' ' + t.replace(/ae|oe|ue/g, (m) => m[0]);
    }
    hasLanguageData = data.some((i) => i.languages_of_instruction && i.languages_of_instruction.length);
    hasPartnerData = data.some((i) => i.partner_of_siba != null);

    const strat = await fetchJson('data/strategies.json');  // optional: panel and filter work without it
    if (strat) {
      strategiesMeta = strat.meta;
      for (const doc of strat.documents) {
        (strategiesByCode.get(doc.erasmus_code) || strategiesByCode.set(doc.erasmus_code, []).get(doc.erasmus_code)).push(doc);
      }
      strategyStatusByCode = new Map(Object.entries(strat.institution_status || {}));
      if (strat.meta.status_labels) strategyStatusLabels = strat.meta.status_labels;
      hasStrategyData = strategyStatusByCode.size > 0;
    }

    mobility = await fetchJson('data/mobility.json');  // optional: the panel works without it
    contacts = await fetchJson('data/contacts.json');  // optional
    networks = await fetchJson('data/networks.json');  // optional
    hasNetworkData = !!(networks && networks.networks.some((n) => n.id === 'aec' && n.mapped));

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
    $('#reset').addEventListener('click', () => {
      resetAll();
      $('#results').focus({ preventScroll: true }); // the button hides itself, so keep keyboard focus somewhere sensible
    });
    $('#home').addEventListener('click', (e) => {
      if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // let "open in new tab" work as a normal link
      e.preventDefault();
      resetAll();
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
    $('#csv').addEventListener('click', downloadCsv);
    $('#panel-close').addEventListener('click', closePanel);
    for (const b of document.querySelectorAll('.view-toggle .btn')) b.addEventListener('click', () => { if (state.view !== b.dataset.view) setView(b.dataset.view); });
    for (const b of document.querySelectorAll('.sort-toggle .btn')) b.addEventListener('click', () => { if (state.sort !== b.dataset.listSort) { state.sort = b.dataset.listSort; update(); } });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('#panel').hidden) closePanel(); });
    window.addEventListener('hashchange', () => { readHash(); update({ fit: true }); if (state.id) openPanel(state.id, null); });

    update({ fit: true });
    if (state.id) openPanel(state.id, null);
  }

  init();
})();
