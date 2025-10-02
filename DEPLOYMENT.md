# Deployment Guide

## Deploying to GitHub Pages

This guide shows how to deploy the Solidity CFG Visualizer to GitHub Pages for public access.

### Automatic Deployment with GitHub Actions

1. **Update `vite.config.js` to set base path:**

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/NT547/', // Replace with your repo name
  server: {
    port: 3000
  }
})
```

2. **Create GitHub Actions workflow file:**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build
        run: npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

3. **Enable GitHub Pages:**
   - Go to repository Settings
   - Navigate to Pages section
   - Select "gh-pages" branch as source
   - Click Save

4. **Push changes:**
```bash
git add .
git commit -m "Setup GitHub Pages deployment"
git push origin main
```

### Manual Deployment

1. **Build the project:**
```bash
npm run build
```

2. **Deploy using gh-pages package:**
```bash
npm install -D gh-pages

# Add to package.json scripts:
"deploy": "npm run build && gh-pages -d dist"

# Deploy:
npm run deploy
```

## Deploying to Other Platforms

### Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

### Netlify

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Deploy:
```bash
netlify deploy --prod --dir=dist
```

### Custom Server

1. Build the project:
```bash
npm run build
```

2. Copy `dist/` folder to your web server
3. Configure web server to serve `index.html` for all routes

## Environment Variables

If you need environment variables:

1. Create `.env` file:
```
VITE_API_URL=https://api.example.com
```

2. Access in code:
```javascript
const apiUrl = import.meta.env.VITE_API_URL
```

## Troubleshooting

### Build fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `rm -rf .vite`

### Assets not loading
- Check `base` path in `vite.config.js`
- Ensure all imports use relative paths

### Parser issues in production
- The @solidity-parser/parser works in browser
- No additional configuration needed
