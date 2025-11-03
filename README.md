# 🌌 Gemini Telegram Quiz Assistant

A blazing-fast, AI-powered Telegram bot that auto-solves polls and QuizBot questions using Google Gemini — with stunning console visuals and human-like response timing. Perfect for quiz enthusiasts, competitive group chats, or anyone who wants to dominate Telegram trivia.

---

## 🚀 Features

- 🧠 **Gemini-Powered Intelligence**  
  Uses Google Gemini (Flash 2.0) to analyze and answer quiz questions with high accuracy.

- 🗳️ **Poll + QuizBot Support**  
  Automatically detects Telegram polls and QuizBot messages, analyzes options, and selects the best answer.

- 🎨 **Rich Console UI**  
  Beautifully styled output using `rich`, including banners, spinners, confidence meters, and animated typing.

- ✅ **Auto-Vote System**  
  Automatically ticks the correct poll option with human-like delay — no manual interaction needed.

- 🔄 **Multi-Group Compatibility**  
  Supports multiple target groups or bots simultaneously.

- 🔐 **Secure Session Management**  
  Stores Telegram sessions locally in a safe and reusable format.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/gemini-telegram-quiz-assistant.git
cd gemini-telegram-quiz-assistant
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit the `config.py` file to set up your credentials and preferences:

```python
# Telegram API credentials
API_ID = 123456
API_HASH = "your_api_hash"

# Gemini API
GEMINI_API_KEY = "your_gemini_api_key"
GEMINI_MODEL = "gemini-2.0-flash"

# Target groups or bot usernames
TARGET_GROUPS = ["your_group_name"]

# Auto-vote toggle
AUTO_VOTE = True
```

---

## 🧠 How It Works

1. Listens for new messages in specified Telegram groups.
2. Detects polls or QuizBot questions.
3. Sends the question and options to Gemini.
4. Parses Gemini’s response to identify the best answer.
5. Displays a rich UI with confidence meter and timing.
6. Auto-votes the correct option (if enabled).

---

## 🖥️ Run Locally

```bash
python main_quiz_bot.py
```

You'll see banners, spinners, and poll breakdowns in your terminal — all in real time.

---

## 🧪 Example Output

```text
🌌 GEMINI AI QUIZ ASSISTANT 🌌

🧩 Gemini Poll Analysis
Q: What is the capital of France?

→ 1. Paris (Gemini Best)
   2. Berlin
   3. Madrid
   4. Rome

🎯 Gemini Confidence
Accuracy: 92.3%
████████░░

✨ Gemini says: Paris
🕓 Gemini answered in 1.42s
```

---

## 🛠️ Tech Stack

- Python 3.10+
- [Telethon](https://github.com/LonamiWebs/Telethon) — Telegram API client
- [Google Gemini](https://ai.google.dev/) — AI answer engine
- [Rich](https://github.com/Textualize/rich) — Terminal UI
- [aiohttp](https://docs.aiohttp.org/) — Async HTTP
- [qrcode](https://pypi.org/project/qrcode/) — Optional QR features

---

## 🧩 Tips & Customization

- Add more groups to `TARGET_GROUPS` to expand coverage.
- Adjust `RESPONSE_SPEED` for faster or slower typing animation.
- Use `USE_GPT = True` to enable GPT fallback if Gemini fails.

---

##  Author

Saqueeb

---

## 📜 License

MIT License — free to use, modify, and share.
```
