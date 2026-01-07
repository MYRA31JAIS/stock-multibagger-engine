# 🔑 API Keys Setup Guide

## **FREE AI ALTERNATIVES (RECOMMENDED)** ⭐

### **1. Google Gemini API** (FREE - 60 req/min) ⭐ BEST FREE OPTION
- **Sign up**: https://makersuite.google.com/app/apikey
- **Usage**: AI analysis for all 6 agents (FREE!)
- **Free tier**: 60 requests/minute, 1M tokens/month

### **2. Groq API** (FREE - Very Fast) ⭐ FASTEST
- **Sign up**: https://console.groq.com/keys
- **Usage**: Lightning-fast AI inference
- **Free tier**: Very generous limits, extremely fast

### **3. Anthropic Claude API** (FREE $5 credit)
- **Sign up**: https://console.anthropic.com/
- **Usage**: High-quality AI analysis
- **Free tier**: $5 credit for new users

### **4. Hugging Face API** (FREE)
- **Sign up**: https://huggingface.co/settings/tokens
- **Usage**: Open-source AI models
- **Free tier**: Generous inference limits

## **STOCK DATA APIs (FREE)** ✅

### **5. Alpha Vantage** (FREE - 25 calls/day) ✅ CONFIGURED
- **Sign up**: https://www.alphavantage.co/support/#api-key
- **Status**: ✅ Already working
- **Free tier**: 25 requests/day, 5 calls/minute

### **6. NewsAPI** (FREE - 1000 calls/day) ✅ CONFIGURED
- **Sign up**: https://newsapi.org/register
- **Status**: ✅ Already working
- **Free tier**: 1000 requests/day

### **7. Finnhub** (FREE - 60 calls/minute) ✅ CONFIGURED
- **Sign up**: https://finnhub.io/register
- **Status**: ✅ Already working
- **Free tier**: 60 calls/minute

## **PAID APIs (Optional)**

### **8. OpenAI API** (PAID) ⚠️ QUOTA EXCEEDED
- **Sign up**: https://platform.openai.com/api-keys
- **Status**: ⚠️ Currently hitting quota limits
- **Note**: Use FREE alternatives above instead!

---

## **📝 PASTE YOUR KEYS HERE:**

### **File 1: `.env` (Root directory)**
```env
# ===== PASTE YOUR API KEYS BELOW =====

# ===== FREE AI ALTERNATIVES (Choose at least ONE) =====
# Google Gemini API Key (FREE - Get from: https://makersuite.google.com/app/apikey)
GOOGLE_GEMINI_API_KEY=paste_your_gemini_key_here

# Groq API Key (FREE - Get from: https://console.groq.com/keys)
GROQ_API_KEY=paste_your_groq_key_here

# Anthropic Claude API Key (FREE $5 credit - Get from: https://console.anthropic.com/)
ANTHROPIC_API_KEY=paste_your_anthropic_key_here

# Hugging Face API Key (FREE - Get from: https://huggingface.co/settings/tokens)
HUGGINGFACE_API_KEY=paste_your_huggingface_key_here

# ===== STOCK DATA APIs (Already configured) =====
# Alpha Vantage API Key (FREE - Get from: https://www.alphavantage.co/support/#api-key)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# NewsAPI Key (FREE - Get from: https://newsapi.org/register)
NEWS_API_KEY=your_newsapi_key_here

# Finnhub API Key (FREE - Get from: https://finnhub.io/register)
FINNHUB_API_KEY=your_finnhub_key_here

# ===== PAID APIs (Optional) =====
# OpenAI API Key (PAID - Currently quota exceeded)
OPENAI_API_KEY=paste_your_openai_key_here
```

### **File 2: `multibagger_system/.env` (Python system directory)**
```env
# ===== PASTE YOUR API KEYS BELOW =====

# ===== FREE AI ALTERNATIVES (Choose at least ONE) =====
# Google Gemini API Key (FREE - Get from: https://makersuite.google.com/app/apikey)
GOOGLE_GEMINI_API_KEY=paste_your_gemini_key_here

# Groq API Key (FREE - Get from: https://console.groq.com/keys)
GROQ_API_KEY=paste_your_groq_key_here

# Anthropic Claude API Key (FREE $5 credit - Get from: https://console.anthropic.com/)
ANTHROPIC_API_KEY=paste_your_anthropic_key_here

# Hugging Face API Key (FREE - Get from: https://huggingface.co/settings/tokens)
HUGGINGFACE_API_KEY=paste_your_huggingface_key_here

# ===== STOCK DATA APIs (Already configured) =====
# Alpha Vantage API Key (FREE - Get from: https://www.alphavantage.co/support/#api-key)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# NewsAPI Key (FREE - Get from: https://newsapi.org/register)
NEWS_API_KEY=your_newsapi_key_here

# Finnhub API Key (FREE - Get from: https://finnhub.io/register)
FINNHUB_API_KEY=your_finnhub_key_here

# ===== PAID APIs (Optional) =====
# OpenAI API Key (PAID - Currently quota exceeded)
OPENAI_API_KEY=paste_your_openai_key_here
```

---

## **🚀 WHAT EACH API PROVIDES:**

### **FREE AI ALTERNATIVES** ✅ CRITICAL
- **Google Gemini**: Fast, reliable, 1M tokens/month FREE
- **Groq**: Extremely fast inference, generous limits
- **Anthropic Claude**: High-quality analysis, $5 free credit
- **Hugging Face**: Open-source models, completely free
- **Impact**: Transforms system from "calculator" to "AI analyst" - FOR FREE!

### **Alpha Vantage** ✅ HIGH VALUE (Already configured)
- **Powers**: Enhanced financial data, company overviews
- **Replaces**: Limited yfinance data
- **Impact**: Better fundamental analysis accuracy

### **NewsAPI** ✅ HIGH VALUE (Already configured)
- **Powers**: Real news sentiment for policy analysis
- **Replaces**: No news analysis (major gap)
- **Impact**: Policy agent becomes actually useful

### **Finnhub** ✅ MEDIUM VALUE (Already configured)
- **Powers**: Comprehensive stock lists, institutional data
- **Replaces**: Hardcoded 28-stock sample with 500+ real stocks
- **Impact**: System can analyze actual NSE universe

### **OpenAI** ⚠️ QUOTA EXCEEDED
- **Status**: Currently hitting quota limits
- **Solution**: Use FREE alternatives above instead!

---

## **💡 QUICK START:**

1. **Get at least ONE free AI key** (Gemini or Groq recommended)
2. **Paste key in both .env files** (root and multibagger_system)
3. **Test AI providers**: `python test_ai_providers.py`
4. **Test full system**: `python test_system.py`
5. **Start system**: `./start_system.sh` or `start_system.bat`

---

## **🔄 AI PROVIDER FALLBACK:**

The system automatically tries providers in this order:
1. **Groq** (if API key provided) - FASTEST
2. **Hugging Face** (if API key provided) - RELIABLE
3. **Anthropic Claude** (if API key provided) - HIGH QUALITY
4. **Google Gemini** (disabled due to rate limits)
5. **OpenAI** (disabled due to quota exceeded)

If one fails, it automatically tries the next one! 🚀

---

## **🎯 EXPECTED RESULTS:**

With FREE AI alternatives, your system will:
- ✅ Analyze 500+ real NSE stocks (vs 28 fake ones)
- ✅ Use actual institutional trading data
- ✅ Provide real news-based policy analysis  
- ✅ Generate AI-powered insights (completely FREE!)
- ✅ Work even when OpenAI quota is exceeded
- ✅ Become a legitimate financial analysis tool

**Bottom line**: These FREE APIs give you the same AI power as OpenAI without the cost! 🚀💰