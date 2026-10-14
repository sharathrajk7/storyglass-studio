// Primary: static copy bundled with this Worker (Cloudflare).
// Secondary: Hostinger, used only for paths the bundle doesn't have (dynamic routes, new files).
const SECONDARY_TIMEOUT_MS = 4000;
const REDIRECT_WWW_TO_APEX = true;

const failed = (res) =>
  res.status === 429 || res.status === 403 || res.status === 408 ||
  (res.status >= 500 && !(res.headers.get('content-type') || '').includes('application/json'));

const tag = (res, served) => {
  const out = new Response(res.body, res);
  out.headers.set('x-served-by', served);
  return out;
};

// Static assets are served whole; add HTTP range support (Safari needs 206 for video).
async function withRange(request, res) {
  const range = request.headers.get('range');
  const out = new Response(res.body, res);
  out.headers.set('Accept-Ranges', 'bytes');
  if (!range || request.method !== 'GET' || res.status !== 200) return out;
  const m = /^bytes=(\d*)-(\d*)$/.exec(range.trim());
  if (!m || (m[1] === '' && m[2] === '')) return out;
  const buf = await res.arrayBuffer();
  const size = buf.byteLength;
  let start, end;
  if (m[1] === '') { start = Math.max(size - Number(m[2]), 0); end = size - 1; }
  else { start = Number(m[1]); end = m[2] === '' ? size - 1 : Math.min(Number(m[2]), size - 1); }
  if (start >= size || start > end) {
    return new Response(null, { status: 416, headers: { 'Content-Range': 'bytes */' + size } });
  }
  const headers = new Headers(res.headers);
  headers.set('Accept-Ranges', 'bytes');
  headers.set('Content-Range', 'bytes ' + start + '-' + end + '/' + size);
  headers.set('Content-Length', String(end - start + 1));
  headers.delete('content-encoding');
  return new Response(buf.slice(start, end + 1), { status: 206, headers });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (REDIRECT_WWW_TO_APEX && url.hostname.startsWith('www.')) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }

    const body = request.method === 'GET' || request.method === 'HEAD'
      ? undefined : await request.text();

    // Static requests: the bundle answers first.
    if (request.method === 'GET' || request.method === 'HEAD') {
      const res = await env.ASSETS.fetch(request);
      if (res.status !== 404) return tag(await withRange(request, res), 'cloudflare');
    }

    // Miss (or non-GET): try Hostinger.
    try {
      const res = await fetch(new URL(url.pathname + url.search, env.SECONDARY_ORIGIN), {
        method: request.method,
        headers: request.headers,
        body,
        redirect: 'manual',
        signal: AbortSignal.timeout(SECONDARY_TIMEOUT_MS),
        ...(request.method === 'GET'
          ? { cf: { cacheEverything: true, cacheTtlByStatus: { '200-299': 60, '300-599': -1 } } } : {}),
      });
      if (!failed(res)) return tag(res, 'hostinger');
    } catch {
      // fall through
    }
    return tag(new Response('Not found', { status: 404 }), 'cloudflare');
  },
};
