import requests
from bs4 import BeautifulSoup
import time
import platform
from datetime import datetime

# ================= CONFIG =================

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRODUCTS = [
    "https://www.imagineonline.store/products/iphone-16-myec3hn-a",
    "https://www.imagineonline.store/products/iphone-16-myed3hn-a",
    "https://www.imagineonline.store/products/iphone-16-myea3hn-a",
    "https://www.imagineonline.store/products/iphone-16-mye93hn-a",
    "https://www.imagineonline.store/products/iphone-16-mye73hn-a",
    "https://www.imagineonline.store/products/iphone-15-mtp13hn-a",
    "https://www.imagineonline.store/products/iphone-15-mtp53hn-a",
    "https://www.imagineonline.store/products/iphone-15-mtp03hn-a",
    "https://www.imagineonline.store/products/iphone-15-mtp43hn-a"
]

CHECK_INTERVAL = 10  # seconds

# ============== TELEGRAM CONFIG ==============

TELEGRAM_BOT_TOKEN = "8368045102:AAEwoGZRGLP5mKK745r5pjUwNUhZZvSWL_M"
TELEGRAM_CHAT_ID = -5075163584
ENABLE_TELEGRAM = True
TELEGRAM_REPEAT_INTERVAL = 10  # seconds

# ============================================

last_telegram_time = 0


# ================= TELEGRAM =================

def send_telegram_message(text):
    if not ENABLE_TELEGRAM:
        print("⚠️ Telegram disabled")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        r = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=10
        )
        print("📨 Telegram status:", r.status_code)
    except Exception as e:
        print("❌ Telegram error:", e)


# ================= ALARM =================

def play_alarm():
    print("\n🚨🚨🚨 STOCK AVAILABLE — ALARM STARTED 🚨🚨🚨\n")

    while True:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(2000, 800)
        else:
            print("\a")
        time.sleep(0.5)


# ================= STOCK CHECK =================

def check_stock(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        add_btn = soup.select_one(
            "button[name='add'], button.add-to-cart, button.btn-add-cart"
        )

        if add_btn:
            text = add_btn.get_text(strip=True).lower()
            if "add to cart" in text or "buy" in text or "order" in text:
                return True

        return False

    except Exception as e:
        print("❌ Request error:", e)
        return False


# ================= MAIN LOOP =================

def run_checker():
    global last_telegram_time

    print("🚀 Stock checker running...\n")

    # 🔥 TELEGRAM START MESSAGE
    send_telegram_message(
        f"🚀 Imagine Store Bot STARTED\n"
        f"Monitoring {len(PRODUCTS)} products\n"
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    )

    notified = set()

    while True:
        print(f"🕒 {datetime.now().strftime('%H:%M:%S')} Checking...")

        for url in PRODUCTS:
            if check_stock(url):
                print(f"✅ IN STOCK → {url}")

                # Telegram repeat alert
                if time.time() - last_telegram_time >= TELEGRAM_REPEAT_INTERVAL:
                    send_telegram_message(
                        f"🚨 STOCK AVAILABLE!\n{url}"
                    )
                    last_telegram_time = time.time()

                # Alarm only once
                if url not in notified:
                    notified.add(url)
                    play_alarm()

            else:
                print(f"⛔ Out of stock → {url}")

        time.sleep(CHECK_INTERVAL)


# ================= START =================

if __name__ == "__main__":
    run_checker()
