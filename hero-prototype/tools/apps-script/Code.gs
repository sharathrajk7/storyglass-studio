/**
 * Storyglass Studio: brief form receiver (Google Apps Script web app).
 *
 * Every brief sent from the website:
 *   1. is saved as a row in the "Briefs" tab of this Google Sheet,
 *   2. is emailed to the studio (pressing Reply answers the client directly),
 *   3. gets a short confirmation email to the client, from the studio's Gmail.
 *
 * Setup: see SETUP.md next to this file. Deploy as a Web app, Execute as: Me, Who has access: Anyone.
 */

const STUDIO_EMAIL = 'storyglassstudio@gmail.com';
const STUDIO_NAME = 'Storyglass Studio';
const REPLY_WITHIN = '24 hours';
const SHEET_NAME = 'Briefs';
const MAX_PER_EMAIL_PER_HOUR = 3;
const MIN_FILL_MS = 2500;  // five steps take a person longer than this, even with autofill; bots don't

const FIELDS = [
  ['received', 'Received'], ['name', 'Name'], ['email', 'Email'], ['company', 'Company'],
  ['site', 'Website / LinkedIn'], ['role', 'You are'], ['film', 'Film'], ['goal', 'Main goal'],
  ['content', 'Content'], ['assets', 'Assets link'], ['timing', 'Timing'], ['country', 'Country'],
  ['whatsapp', 'WhatsApp'], ['notes', 'Notes'], ['page', 'Sent from'],
];

function doPost(e) {
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    // a bot: the hidden field is filled, or five steps were done faster than a person can.
    // Answer "ok" so it doesn't retry, but keep nothing.
    if (d.hp || (Number(d.elapsedMs) > 0 && Number(d.elapsedMs) < MIN_FILL_MS)) return json_({ ok: true });

    const row = clean_(d);
    if (!row.name || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(row.email)) return json_({ ok: false, error: 'invalid' });

    // the same address can't flood the inbox (or be used to spam someone with confirmations)
    const cache = CacheService.getScriptCache();
    const key = 'n:' + row.email.toLowerCase();
    const n = Number(cache.get(key) || 0);
    if (n >= MAX_PER_EMAIL_PER_HOUR) return json_({ ok: true });
    cache.put(key, String(n + 1), 3600);

    row.received = new Date();
    sheet_().appendRow(FIELDS.map(([k]) => safeCell_(row[k])));
    notifyStudio_(row);
    confirmClient_(row);
    return json_({ ok: true });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server' });
  }
}

// Opening the web-app URL in a browser shows this, so you can check the deployment is live.
function doGet() {
  return json_({ ok: true, service: STUDIO_NAME + ' brief receiver' });
}

function clean_(d) {
  const out = {};
  FIELDS.forEach(([k]) => {
    let v = d[k];
    if (Array.isArray(v)) v = v.join(', ');
    out[k] = String(v == null ? '' : v).trim().slice(0, 2000);
  });
  return out;
}

// A cell that starts with = + - @ would run as a formula in the Sheet; store it as plain text.
function safeCell_(v) {
  if (v instanceof Date) return v;
  const s = String(v == null ? '' : v);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) sh = ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) {
    sh.appendRow(FIELDS.map(([, label]) => label));
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, FIELDS.length).setFontWeight('bold');
  }
  return sh;
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function table_(row, keys) {
  return '<table cellpadding="6" style="border-collapse:collapse;font:14px/1.5 Arial,sans-serif">' +
    FIELDS.filter(([k]) => keys.indexOf(k) >= 0 && row[k])
      .map(([k, label]) => '<tr><td style="color:#777;vertical-align:top;white-space:nowrap">' + esc_(label) +
        '</td><td>' + esc_(row[k]).replace(/\n/g, '<br>') + '</td></tr>').join('') + '</table>';
}

function notifyStudio_(row) {
  const keys = ['name', 'email', 'company', 'site', 'role', 'film', 'goal', 'content', 'assets', 'timing', 'country', 'whatsapp', 'notes', 'page'];
  const subject = 'New brief: ' + row.name + (row.company ? ' · ' + row.company : '') + (row.film ? ' · ' + row.film : '');
  MailApp.sendEmail({
    to: STUDIO_EMAIL,
    replyTo: row.email,
    name: STUDIO_NAME + ' website',
    subject: subject,
    htmlBody: '<p style="font:15px Arial,sans-serif">A new brief came in. Press Reply to answer ' + esc_(row.name) + ' directly.</p>' + table_(row, keys),
    body: keys.filter((k) => row[k]).map((k) => k + ': ' + row[k]).join('\n'),
  });
}

function confirmClient_(row) {
  const keys = ['film', 'goal', 'content', 'timing'];
  const first = row.name.split(/\s+/)[0];
  MailApp.sendEmail({
    to: row.email,
    replyTo: STUDIO_EMAIL,
    name: STUDIO_NAME,
    subject: 'We got your brief · ' + STUDIO_NAME,
    htmlBody: '<div style="font:15px/1.6 Arial,sans-serif;color:#111">' +
      '<p>Hi ' + esc_(first) + ',</p>' +
      '<p>Thanks for your brief. We read every one ourselves and will reply within ' + REPLY_WITHIN +
      ' with an approach, a timeline and a quote.</p>' +
      '<p>Here is what you sent:</p>' + table_(row, keys) +
      '<p>If you want to add anything, just reply to this email.</p>' +
      '<p>' + STUDIO_NAME + '</p></div>',
    body: 'Hi ' + first + ',\n\nThanks for your brief. We will reply within ' + REPLY_WITHIN +
      ' with an approach, a timeline and a quote. To add anything, just reply to this email.\n\n' + STUDIO_NAME,
  });
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

// Run this once from the editor (select it, press Run) to grant permissions and send yourself a test email.
function testSetup() {
  doPost({ postData: { contents: JSON.stringify({
    name: 'Test Lead', email: STUDIO_EMAIL, company: 'Acme', film: 'Product demo', goal: 'More leads',
    content: 'I have an idea', timing: '2–4 weeks', notes: 'This is a setup test. Delete this row.', page: 'setup test',
  }) } });
}
