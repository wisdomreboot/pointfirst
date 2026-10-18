/* Point First service worker, for the hosted copy.
   Keeps the app itself, so it opens without a connection.
   Essays never pass through here. They live in the folder the writer connects.
   Word lists are not cached either. They live in that folder too. */
const CACHE='pointfirst-v9';
/* Install: cache the page under both its addresses, then take over without waiting. */
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','./index.html'])));self.skipWaiting()});
/* Activate: delete caches from older versions, then serve the open tabs straight away. */
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
/* Fetch: same-origin GETs only, and never the word lists. The rest goes to the network untouched. */
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==self.location.origin||u.pathname.includes('/word-lists/'))return;
  /* Network first, so a new version arrives on the next visit. Each good answer refreshes the cache.
     Offline, the cached copy answers. Anything the cache lacks gets the app itself. */
  e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy))}return r})
    .catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))))});
