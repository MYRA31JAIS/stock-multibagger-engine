# 🚀 Deployment Guide for Render

## ✅ Pre-Deployment Checklist Complete

✅ **Project Structure Ready**
- Frontend: Next.js app in `multibagger_webapp/`
- Backend: Python Flask API in `multibagger_webapp/python_bridge/`
- Configuration files created
- Environment variables documented

✅ **Dependencies Complete**
- Python requirements.txt updated with all dependencies
- Next.js package.json ready
- All AI providers configured (Groq, Hugging Face working)

✅ **System Tested & Working**
- ✅ Multi-Agent AI system operational
- ✅ Stock analysis working (60.9% probability for TCS.NS)
- ✅ Real market data integration
- ✅ News sentiment analysis
- ✅ Technical indicators
- ✅ Python bridge server ready

## 🌐 Deploy to Render (Ready to Deploy!)

### **Step 1: Deploy Python Backend**

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository: `https://github.com/MYRA31JAIS/stock-multibagger-engine`

2. **Configure Backend Service**
   ```
   Name: multibagger-python-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn wsgi:application --bind 0.0.0.0:$PORT
   Python Version: 3.11.9 (specified in runtime.txt)
   ```

3. **Add Environment Variables**
   ```
   GROQ_API_KEY=your_groq_key_here
   GOOGLE_GEMINI_API_KEY=your_gemini_key_here
   HUGGINGFACE_API_KEY=your_huggingface_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
   NEWS_API_KEY=your_news_api_key_here
   FINNHUB_API_KEY=your_finnhub_key_here
   POLYGON_API_KEY=your_polygon_key_here
   PORT=5000
   FLASK_ENV=production
   ```

4. **Deploy Backend**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://your-backend.onrender.com`

### **Step 2: Deploy Next.js Frontend**

1. **Create New Static Site**
   - Click "New" → "Static Site"
   - Connect same GitHub repository

2. **Configure Frontend Service**
   ```
   Name: multibagger-frontend
   Root Directory: multibagger_webapp
   Build Command: npm install && npm run build
   Publish Directory: .next
   ```

3. **Add Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   NODE_VERSION=18.17.0
   ```

4. **Deploy Frontend**
   - Click "Create Static Site"
   - Wait for deployment (3-5 minutes)
   - Your app will be live at: `https://your-frontend.onrender.com`

## 🔧 Post-Deployment

### **Test Your Deployment**

1. **Backend Health Check**
   ```bash
   curl https://your-backend.onrender.com/health
   # Should return: OK
   ```

2. **API Status Check**
   ```bash
   curl https://your-backend.onrender.com/api/health
   # Should return JSON with system status
   ```

3. **Frontend Access**
   - Visit: `https://your-frontend.onrender.com`
   - Should load the multibagger analysis interface

### **Configure API Connection**

Update your frontend environment variable:
```
NEXT_PUBLIC_API_URL=https://your-actual-backend-url.onrender.com
```

## 🎯 Expected Results

After successful deployment:

✅ **Backend API**: `https://your-backend.onrender.com`
- Health check at `/health`
- API endpoints at `/api/*`
- AI system initialization
- Stock analysis capabilities

✅ **Frontend Web App**: `https://your-frontend.onrender.com`
- Modern Next.js interface
- Real-time stock analysis
- AI-powered insights
- Responsive design

## 🔍 Troubleshooting

### **Common Issues**

1. **Backend Build Fails**
   - Check Python version (should be 3.9+)
   - Verify requirements.txt dependencies
   - Check environment variables

2. **Frontend Build Fails**
   - Verify Node.js version (18.x)
   - Check package.json dependencies
   - Ensure API URL is set

3. **API Connection Issues**
   - Verify CORS configuration
   - Check backend URL in frontend env
   - Test backend health endpoint

### **Logs & Monitoring**

- **Backend Logs**: Render Dashboard → Your Service → Logs
- **Frontend Logs**: Render Dashboard → Your Site → Deploy Logs
- **Health Monitoring**: Use `/health` endpoint for uptime monitoring

## 🚀 Success!

Once deployed, you'll have a fully functional AI-powered multibagger stock analysis platform accessible worldwide!

**Share your live app**: `https://your-frontend.onrender.com`

## 📊 System Capabilities

Your deployed system will provide:
- **Multi-Agent AI Analysis**: 6 specialized AI agents
- **Real Market Data**: Live NSE stock prices and financials
- **News Sentiment**: Real-time news analysis
- **Technical Analysis**: RSI, moving averages, support/resistance
- **Smart Money Tracking**: FII/DII flow analysis
- **Policy Impact**: Government policy analysis
- **Multibagger Scoring**: 0-100% probability scoring

**Example Results**: TCS.NS analyzed at 60.9% multibagger probability with detailed insights!