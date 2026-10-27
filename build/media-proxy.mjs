// Only explicitly verified files at immutable public GitHub commits are served.
// Bodies stay as streams so large videos do not consume the isolate's memory.
const types = {
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', webp: 'image/webp',
  avif: 'image/avif', gif: 'image/gif', svg: 'image/svg+xml', mp4: 'video/mp4', webm: 'video/webm',
  woff: 'font/woff', woff2: 'font/woff2', ttf: 'font/ttf', otf: 'font/otf',
};
const encode = value => value.split('/').map(encodeURIComponent).join('/');
const cacheControl = 'public, max-age=3600, s-maxage=86400';

export function createMediaHandler(groups, fetchMedia = fetch) {
  const assets = new Map();
  for (const group of groups) {
    if (!/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/[a-f0-9]{40}\//.test(group.base)) {
      throw new Error('Media requires an immutable public GitHub source');
    }
    for (const asset of group.assets) {
      const type = types[asset.path.split('.').pop().toLowerCase()];
      if (!type || !/^[a-f0-9]{64}$/.test(asset.sha256) || !Number.isSafeInteger(asset.bytes) || asset.bytes < 1 ||
          asset.path.startsWith('/') || asset.path.includes('\\') || asset.path.split('/').some(x => !x || x === '.' || x === '..')) {
        throw new Error('Invalid media allowlist entry');
      }
      const pathname = group.prefix + asset.path;
      if (assets.has(pathname)) throw new Error('Duplicate media route');
      assets.set(pathname, { ...asset, type, url: group.base + encode(asset.path), etag: '"sha256-' + asset.sha256 + '"' });
    }
  }
  return async request => {
    let pathname;
    try { pathname = decodeURIComponent(new URL(request.url).pathname); } catch { return null; }
    const asset = assets.get(pathname);
    if (!asset) return null;
    if (!['GET', 'HEAD'].includes(request.method)) {
      return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
    }
    const responseHeaders = new Headers({
      'Content-Type': asset.type,
      'Cache-Control': cacheControl,
      'ETag': asset.etag,
      'Accept-Ranges': 'bytes',
      'Access-Control-Allow-Origin': '*',
      'Cross-Origin-Resource-Policy': 'cross-origin',
      'X-Content-Type-Options': 'nosniff',
      'X-Source-SHA256': asset.sha256,
    });
    const validators = (request.headers.get('If-None-Match') ?? '').split(',').map(x => x.trim().replace(/^W\//, ''));
    if (validators.includes('*') || validators.includes(asset.etag)) {
      return new Response(null, { status: 304, headers: responseHeaders });
    }
    // Never forward visitor cookies, authorization, query strings, or headers.
    const headers = new Headers();
    const range = request.headers.get('Range');
    const ifRange = request.headers.get('If-Range');
    if (range && /^bytes=(?:\d+-\d*|-\d+)$/.test(range) && (!ifRange || ifRange === asset.etag)) {
      headers.set('Range', range);
    }
    let upstream;
    try {
      upstream = await fetchMedia(asset.url, {
        method: request.method, headers, redirect: 'manual',
        cf: { cacheEverything: true, cacheTtl: 86400 },
      });
    } catch (error) {
      console.warn('Immutable media fetch failed:', error instanceof Error ? error.message : 'network error');
      return new Response('Media temporarily unavailable', { status: 502, headers: { 'Cache-Control': 'no-store' } });
    }
    if (![200, 206, 416].includes(upstream.status)) {
      console.warn('Immutable media upstream returned status', upstream.status);
      await upstream.body?.cancel();
      return new Response('Media temporarily unavailable', { status: 502, headers: { 'Cache-Control': 'no-store' } });
    }
    for (const name of ['Content-Length', 'Content-Range', 'Last-Modified']) {
      const value = upstream.headers.get(name);
      if (value) responseHeaders.set(name, value);
    }
    if (upstream.status === 416) responseHeaders.set('Cache-Control', 'no-store');
    return new Response(request.method === 'HEAD' ? null : upstream.body, { status: upstream.status, headers: responseHeaders });
  };
}
