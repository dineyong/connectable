/* Test-only asset, opt-in to the authenticated private preview package. */
(async () => {
  'use strict';
  const targets = [
    ['/', 200],
    ['/monitor-v3-data.js', 200],
    ['/monitor-v3.css', 200],
    ['/monitors/', 200],
    ['/monitors/asus-pa279crv/', 200],
    ['/guides/monitor-buying.html', 200],
    ['/tech-news.html', 200],
    ['/__missing_preview_check_20261022', 404],
    ['/monitors/__missing_preview_check_20261022/', 404],
  ];
  // An allowlist prevents authentication/session headers from entering the report.
  const headerNames = ['content-type', 'x-robots-tag', 'x-content-type-options',
    'x-frame-options', 'referrer-policy', 'permissions-policy', 'cache-control'];
  const results = [];
  for (const [path, expectedStatus] of targets) {
    try {
      const response = await fetch(path, {
        credentials: 'same-origin', redirect: 'error', cache: 'no-store',
      });
      const headers = Object.fromEntries(headerNames.map(name => [name, response.headers.get(name)]));
      const failures = [];
      if (response.status !== expectedStatus) failures.push('status');
      if (!(headers['x-robots-tag'] || '').split(/[,\s]+/).includes('noindex')) failures.push('noindex');
      if (headers['x-content-type-options'] !== 'nosniff') failures.push('nosniff');
      if (headers['x-frame-options'] !== 'DENY') failures.push('frame');
      if (headers['referrer-policy'] !== 'strict-origin-when-cross-origin') failures.push('referrer');
      if (!(headers['cache-control'] || '').includes('no-store')) failures.push('cache');
      if (!['camera=()', 'microphone=()', 'geolocation=()'].every(value =>
        (headers['permissions-policy'] || '').includes(value))) failures.push('permissions');
      let title = null;
      if ((headers['content-type'] || '').includes('text/html')) {
        const page = new DOMParser().parseFromString(await response.text(), 'text/html');
        title = page.title;
        if (expectedStatus === 404 && !page.body.textContent.includes('페이지를 찾을 수 없어요.')) {
          failures.push('404-content');
        }
      }
      results.push({path, expectedStatus, status: response.status, title, headers, failures});
    } catch {
      results.push({path, expectedStatus, failures: ['request-failed-or-auth-redirect']});
    }
  }
  document.getElementById('results').textContent = JSON.stringify(results, null, 2);
  const failed = results.filter(result => result.failures.length).length;
  document.getElementById('status').textContent = failed
    ? `FAIL: ${failed}/${results.length} responses` : `PASS: ${results.length}/${results.length} responses`;
})();
