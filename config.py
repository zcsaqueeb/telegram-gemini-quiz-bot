# ============================================================
# ⚙️ CONFIGURATION FILE — Gemini Telegram Quiz Assistant
# ============================================================

# 🔐 Telegram API credentials (replace with your own)
API_ID = 123456
API_HASH = "your_api_hash_here"

# 🤖 Telegram Bot Token (optional, if using bot mode)
BOT_TOKEN = "your_bot_token_here"

# 🎯 Target group names or bot usernames (supports multiple)
TARGET_GROUPS = [
    "your_group_name_or_bot_username",
]

# 🕓 Timing controls
RESPONSE_DELAY = 0
CHATTER_REPLY_DELAY = 0

# ⚡ Speed control for typing animation
# Options: "instant", "superfast", "normal", "slow"
RESPONSE_SPEED = "superfast"
RESPONSE_SPEED_MAP = {
    "instant": 0.0,
    "superfast": 0.005,
    "normal": 0.02,
    "slow": 0.05
}

# ✅ Auto-vote feature (tick the correct poll option automatically)
AUTO_VOTE = True

# 🧠 Choose answer provider
ANSWER_PROVIDER = "gemini"

# 🔑 Gemini API config (replace with your own key)
GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "gemini-2.0-flash"

# 🧩 GPT fallback (optional)
USE_GPT = False
GPT_API_URL = "https://api.example.com/gpt"
