// Service Worker para PWA - soporte offline y caching
const CACHE_NAME = 'modeling-dashboard-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json'
];

// Instalar service worker y cachear assets estáticos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Service Worker: cacheing static assets');
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.log('Service Worker: some assets could not be cached', err);
      });
    })
  );
  self.skipWaiting();
});

// Activar service worker y limpiar cachés viejos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: deleting old cache', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Estrategia Network First con Cache Fallback
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // No cache POST, DELETE, PUT
        if (!response || response.status !== 200 || response.type === 'error') {
          return response;
        }

        // Clone la response
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });

        return response;
      })
      .catch(() => {
        // Si hay error en network, intenta cache
        return caches.match(event.request).then(response => {
          if (response) {
            console.log('Service Worker: serving from cache', event.request.url);
            return response;
          }
          // Si no está en cache, return offline page
          return new Response('Offline - no cache available', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
              'Content-Type': 'text/plain'
            })
          });
        });
      })
  );
});
