/**
 * Vercel Web Analytics Integration for Flet Application
 * 
 * This script loads and initializes Vercel Web Analytics.
 * It's designed to work with Flet's web_browser mode.
 */

(function() {
  'use strict';
  
  // Wait for the page to fully load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnalytics);
  } else {
    initAnalytics();
  }
  
  function initAnalytics() {
    console.log('[Vercel Analytics] Initializing...');
    
    // Load the analytics module dynamically
    import('https://cdn.jsdelivr.net/npm/@vercel/analytics@1/dist/index.mjs')
      .then(module => {
        // Inject analytics
        module.inject({
          mode: 'production', // Can be 'development' or 'production'
          debug: false
        });
        console.log('[Vercel Analytics] Successfully initialized');
      })
      .catch(error => {
        console.error('[Vercel Analytics] Failed to load:', error);
      });
  }
})();
