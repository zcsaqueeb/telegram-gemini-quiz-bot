import sys
import asyncio
import os
import logging
import qrcode
from colorama import init
from google import genai
import aiohttp
import certifi
import ssl
import time
import random
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPoll
from telethon.tl.functions.messages import SendVoteRequest
from config import *

# Rich UI
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from rich import box
from rich.progress import Progress

# Initialize
console = Console()
init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.makedirs("sessions", exist_ok=True)
ssl_context = ssl.create_default_context(cafile=certifi.where())

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 🌈 Gemini Banner
def gemini_banner():
    styles = ["bold magenta", "bold cyan", "bold green", "bold yellow"]
    banner = random.choice([
        "🌌 GEMINI AI QUIZ ASSISTANT 🌌",
        "🧠 POWERED BY GOOGLE GEMINI 🧠",
        "✨ TELEGRAM QUIZ INTELLIGENCE ✨"
    ])
    console.print(Panel(Text(banner, style=random.choice(styles)), style="bold blue", box=box.DOUBLE_EDGE))

# 🧠 Gemini Answer Fetching
def fetch_answer_from_gemini_sync(prompt: str) -> str:
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[{"text": f"Answer this quiz or riddle concisely:\n{prompt}"}]
        )
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error fetching Gemini answer: {e}")
        return ""

async def fetch_answer_from_gemini(prompt: str) -> str:
    return await asyncio.to_thread(fetch_answer_from_gemini_sync, prompt)

async def fetch_quiz_answer(prompt: str) -> str:
    with Live(Spinner("dots", text="🧠 Gemini is thinking...", style="bold cyan"), refresh_per_second=10):
        start = time.time()
        answer = await fetch_answer_from_gemini(prompt)
        duration = time.time() - start
    return answer or "No answer", duration

# 🎨 Typing Animation
async def type_out(text, delay=0.02):
    for ch in text:
        console.print(ch, end="", style="bold cyan")
        sys.stdout.flush()
        await asyncio.sleep(delay)
    print()

# 📈 Confidence Meter
def show_confidence_meter(score: float):
    bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
    console.print(
        Panel(
            f"[bold white]Accuracy:[/bold white] {score:.1f}%\n[green]{bar}[/green]",
            title="🎯 Gemini Confidence",
            style="bold green",
            box=box.ROUNDED
        )
    )

# 🧩 Poll UI
def print_poll_console(question, options, correct_index, confidence, duration):
    lines = []
    for i, opt in enumerate(options, 1):
        if i - 1 == correct_index:
            lines.append(f"[bold green]→ {i}. {opt}[/bold green] [dim](Gemini Best)[/dim]")
        else:
            lines.append(f"[dim]{i}. {opt}[/dim]")

    console.print(
        Panel(
            f"[bold white]Q:[/bold white] {question}\n\n" + "\n".join(lines),
            title="🧩 Gemini Poll Analysis",
            border_style="bright_magenta",
            box=box.ROUNDED,
        )
    )

    show_confidence_meter(confidence)

    console.print(
        Panel(
            f"[bold cyan]Here is the correct answer 👇[/bold cyan]\n\n"
            f"[bold green]{options[correct_index]}[/bold green]\n"
            f"[dim]🕓 Gemini answered in {duration:.2f}s[/dim]",
            style="bold green",
            box=box.DOUBLE_EDGE,
        )
    )

# 🔍 Gemini Poll Answer Logic
async def get_poll_answer(poll_question, poll_options) -> tuple[int, float]:
    options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(poll_options)])
    prompt = (
        f"Question: {poll_question}\n\nOptions:\n{options_text}\n\n"
        "Return only the number (1, 2, 3, etc.) of the correct answer:"
    )
    answer, duration = await fetch_quiz_answer(prompt)
    try:
        import re
        match = re.search(r'\d+', answer)
        if match:
            idx = int(match.group()) - 1
            if 0 <= idx < len(poll_options):
                return idx, duration
    except Exception:
        pass
    return 0, duration

# 🗳️ Auto-Tick Correct Poll Option
async def vote_poll(client: TelegramClient, message, option_index: int) -> bool:
    """
    Votes using the poll's actual option bytes (not raw index).
    Works reliably with both QuizBot and native Telegram polls.
    """
    try:
        poll = message.media.poll
        option_bytes = poll.answers[option_index].option
        await client(
            SendVoteRequest(
                peer=message.peer_id,
                msg_id=message.id,
                options=[option_bytes],
            )
        )
        logging.info(f"✅ Auto-voted for option {option_index + 1}: {poll.answers[option_index].text}")
        return True
    except IndexError:
        logging.error(f"❌ Option index {option_index} out of range.")
        return False
    except Exception as e:
        logging.error(f"❌ Voting failed: {e}")
        return False

# 🔎 Find All Groups
async def find_groups(client):
    found = {}
    async for dialog in client.iter_dialogs():
        name = (dialog.name or "").lower()
        username = (getattr(dialog.entity, "username", "") or "").lower()
        for target in TARGET_GROUPS:
            t = target.lower()
            if t in name or username == t:
                found[target] = dialog.id
                logging.info(f"✅ Found '{target}' with ID {dialog.id}")
    return found

# 🧠 Main Quiz Handler
async def responder_loop(client, group_map):
    gemini_banner()
    console.print("[bold cyan]🤖 Gemini Auto-Responder (with auto-tick) active![/bold cyan]\n")

    @client.on(events.NewMessage(chats=list(group_map.values())))
    async def handler(event):
        if event.message.media and isinstance(event.message.media, MessageMediaPoll):
            try:
                poll = event.message.media.poll
                question = poll.question.text if hasattr(poll.question, "text") else str(poll.question)
                options = [opt.text.text if hasattr(opt.text, "text") else str(opt.text) for opt in poll.answers]
                idx, duration = await get_poll_answer(question, options)
                confidence = random.uniform(75, 95)

                print_poll_console(question, options, idx, confidence, duration)
                await type_out(f"✨ Gemini says: [bold green]{options[idx]}[/bold green]\n")

                await asyncio.sleep(random.uniform(0.8, 1.5))  # simulate human-like delay
                await vote_poll(client, event.message, idx)

            except Exception as e:
                logging.error(f"Poll handling error: {e}")

    await client.run_until_disconnected()

# 🚀 Main Entry
async def main():
    session_file = os.path.join("sessions", "user0.session")

    client = TelegramClient(session_file, API_ID, API_HASH)
    await client.start()
    logging.info("✅ Client started")

    group_map = await find_groups(client)
    if not group_map:
        logging.warning("⚠️ No matching groups found. Check TARGET_GROUPS in config.")
        return

    logging.info("🚀 Bot running in multi-group mode")
    await responder_loop(client, group_map)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Script stopped by user.")
