# Deployment Guide

## Frontend (Next.js) - Deploy to Vercel

### Method 1: Vercel Dashboard (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Configure Project**:
   - **Root Directory**: Set to `client`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

4. **Environment Variables**:
   - Add: `NEXT_PUBLIC_API_URL` = your backend API URL
   - Example: `https://your-backend.railway.app`

5. **Deploy**: Click "Deploy" and wait for build to complete

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to client folder
cd client

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name? (enter name)
# - Directory? ./
# - Override settings? N

# For production deployment
vercel --prod
```

### Post-Deployment

After deployment, Vercel will give you a URL like:
- Preview: `https://your-app-xyz123.vercel.app`
- Production: `https://your-app.vercel.app`

Update your backend CORS settings to allow this domain.

---

## Backend (FastAPI) - Deploy Options

### Option 1: Railway (Easiest)

1. **Create `requirements.txt`**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Create `railway.toml`**:
   ```toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   startCommand = "uvicorn server.api:app --host 0.0.0.0 --port $PORT"
   ```

3. **Deploy via Railway Dashboard**:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Add environment variables:
     - `ANTHROPIC_API_KEY`
     - `YOUTUBE_API_KEY`
   - Deploy automatically starts

4. **Get URL**:
   - Railway generates URL: `https://your-app.railway.app`
   - Use this as `NEXT_PUBLIC_API_URL` in Vercel

### Option 2: Render

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: func-backend
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "uvicorn server.api:app --host 0.0.0.0 --port $PORT"
       envVars:
         - key: ANTHROPIC_API_KEY
           sync: false
         - key: YOUTUBE_API_KEY
           sync: false
   ```

2. **Deploy**:
   - Go to [render.com](https://render.com)
   - New Web Service from GitHub
   - Select repository
   - Add environment variables
   - Deploy

### Option 3: Fly.io

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Initialize**:
   ```bash
   fly launch
   ```

3. **Set secrets**:
   ```bash
   fly secrets set ANTHROPIC_API_KEY=your_key
   fly secrets set YOUTUBE_API_KEY=your_key
   ```

4. **Deploy**:
   ```bash
   fly deploy
   ```

---

## Environment Variables Checklist

### Frontend (.env.local - Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (.env - Railway/Render/Fly.io)
```
ANTHROPIC_API_KEY=sk-ant-...
YOUTUBE_API_KEY=AIza...
```

---

## CORS Configuration

After deploying frontend, update backend CORS in `server/api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",
        "http://localhost:3000"  # for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Quick Deployment Checklist

- [ ] Frontend pushed to GitHub
- [ ] Backend has `requirements.txt`
- [ ] Environment variables ready
- [ ] Deploy backend first (get URL)
- [ ] Deploy frontend with backend URL
- [ ] Update CORS in backend
- [ ] Test the deployed app
- [ ] Monitor logs for errors

---

## Troubleshooting

**Build fails on Vercel**:
- Check that root directory is set to `client`
- Ensure all dependencies are in `package.json`
- Check build logs for specific errors

**Backend API not responding**:
- Verify environment variables are set
- Check CORS configuration
- Review Railway/Render logs

**CORS errors**:
- Add your Vercel domain to backend CORS settings
- Ensure protocol (https) matches

---

Deployment complete! 🚀
