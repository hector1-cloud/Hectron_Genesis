# Vercel Web Analytics Integration

This document explains how Vercel Web Analytics has been integrated into the Hectron Genesis project.

## Overview

Hectron Genesis is a Flet-based Python application that runs in web browser mode. Vercel Web Analytics has been integrated to track page views and user interactions when the app is deployed to Vercel's infrastructure.

## Implementation Details

### 1. Package Installation

The `@vercel/analytics` package (v1.4.1) has been installed via npm:

```bash
npm install @vercel/analytics
```

This is tracked in `package.json` and `package-lock.json`.

### 2. Analytics Script

A JavaScript file has been created at `assets/vercel-analytics.js` that:
- Dynamically loads the Vercel Analytics module from CDN
- Initializes analytics in production mode
- Includes error handling and console logging for debugging

### 3. Flet Configuration Updates

Both main application files have been updated to use the `assets` directory:

**main.py:**
```python
ft.app(target=main, view="web_browser", port=8080, assets_dir="assets")
```

**app.py:**
```python
ft.app(
    target=main, 
    view=ft.AppView.WEB_BROWSER, 
    port=7860,
    host="0.0.0.0",
    assets_dir="assets"
)
```

### 4. Analytics Loading

The analytics script is loaded via CDN using ES modules:
```javascript
import { inject } from 'https://cdn.jsdelivr.net/npm/@vercel/analytics@1/dist/index.mjs';
inject({ mode: 'production' });
```

## Important Notes

### Flet Limitations

Flet is a Flutter-based Python framework that doesn't natively support JavaScript injection. The analytics integration relies on:

1. **CDN Loading**: The analytics library is loaded from a CDN rather than from node_modules
2. **ES Module Imports**: Modern browsers support dynamic imports, which enables the analytics
3. **Vercel Deployment**: Analytics work best when deployed to Vercel's infrastructure

### Browser Compatibility

The implementation uses ES modules (import statements) which are supported in:
- Chrome 63+
- Firefox 60+
- Safari 11.1+
- Edge 79+

Older browsers may not support this implementation.

## Activation on Vercel

To activate analytics on Vercel:

1. **Enable in Dashboard**:
   - Go to your project on Vercel
   - Navigate to Settings → Analytics
   - Enable Web Analytics

2. **Deploy the Application**:
   ```bash
   vercel deploy
   ```

3. **Verify Tracking**:
   - Visit your deployed site
   - Open browser DevTools → Network tab
   - Look for requests to `/_vercel/insights/*` or similar analytics endpoints
   - Check console for "[HECTRON] Vercel Analytics initialized" message

4. **View Data**:
   - Return to the Vercel dashboard
   - Navigate to Analytics tab
   - Data appears after users visit your site (may take a few minutes)

## Testing Locally

When running locally, analytics will attempt to initialize but may not send data to Vercel. To test:

```bash
# Run the main application
python main.py
```

Then visit `http://localhost:8080` and check the browser console for initialization messages.

## Deployment Considerations

### Vercel Deployment

For optimal analytics tracking on Vercel, ensure:
- The project is connected to a Vercel account
- Web Analytics is enabled in the project settings
- The app is deployed using `vercel deploy` or GitHub integration

### Alternative Deployments

If deploying to other platforms (Hugging Face Spaces, Docker, etc.), the analytics script will still load but may not send data to Vercel's infrastructure. Consider:
- Using platform-specific analytics (e.g., Hugging Face Spaces analytics)
- Setting up a custom analytics endpoint
- Using server-side Python analytics libraries

## Files Modified

- `package.json` - Added @vercel/analytics dependency
- `package-lock.json` - Generated lock file
- `main.py` - Added assets_dir parameter
- `app.py` - Added assets_dir parameter
- `assets/vercel-analytics.js` - Analytics initialization script

## Troubleshooting

### Analytics Not Working

1. **Check Browser Console**: Look for error messages or initialization logs
2. **Verify Network Requests**: Use DevTools to ensure analytics requests are being sent
3. **Enable Debug Mode**: Edit `assets/vercel-analytics.js` and set `debug: true`
4. **Check Vercel Dashboard**: Ensure analytics are enabled for your project

### Build Errors

If you encounter build errors:
1. Ensure Node.js and npm are installed
2. Run `npm install` to reinstall dependencies
3. Check that `package-lock.json` is committed to version control

## Additional Resources

- [Vercel Analytics Documentation](https://vercel.com/docs/analytics)
- [Flet Documentation](https://flet.dev/docs/)
- [Flet Web Deployment Guide](https://flet.dev/docs/publish/web/dynamic-website/)

## Support

For issues specific to:
- **Vercel Analytics**: See [Vercel Support](https://vercel.com/support)
- **Flet Framework**: See [Flet GitHub Issues](https://github.com/flet-dev/flet/issues)
- **This Integration**: Open an issue in the project repository
