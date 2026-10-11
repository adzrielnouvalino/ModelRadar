"""ModelRadar Telegram bot (long polling).
Menghubungkan pengguna Telegram ke flow Langflow lewat endpoint /api/v1/run.
Tidak menyimpan isi pesan dan tidak menulis isi pesan ke log.
"""
import os
import re
import threading
import time

import requests


def load_env(path=".env"):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
TG_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
LF_URL = os.environ.get("LANGFLOW_URL", "http://127.0.0.1:7860").rstrip("/")
FLOW_ID = os.environ["FLOW_ID"]
LF_KEY = os.environ["LANGFLOW_API_KEY"]

TG = f"https://api.telegram.org/bot{TG_TOKEN}"
MAX_INPUT = 500      # batas panjang pesan pengguna
COOLDOWN = 10        # detik antar pesan per pengguna
WAIT_LIMIT = 240     # detik menunggu Langflow

WELCOME = (
    "Halo! Saya ModelRadar.\n\n"
    "Ceritakan levelmu dan tugasnya, misalnya:\n"
    "\"Saya pemula, rekomendasikan model text-generation yang sedang trending.\"\n\n"
    "Catatan:\n"
    "- Data dari Hugging Face, hanya model open-source.\n"
    "- Saya tidak menguji model; trending tidak berarti terbaik atau aman.\n"
    "- Jangan kirim data pribadi.\n"
    "- Jawaban bisa butuh setengah menit atau lebih.\n\n"
    "Ketik /baru untuk memulai percakapan baru."
)

session_no = {}   # chat_id -> nomor sesi
last_msg = {}     # chat_id -> waktu pesan terakhir
busy = set()      # chat_id yang sedang diproses
lock = threading.Lock()


def send(chat_id, text):
    for i in range(0, len(text), 4000):
        requests.post(
            f"{TG}/sendMessage",
            json={"chat_id": chat_id, "text": text[i:i + 4000]},
            timeout=30,
        )


def clean(text):
    text = text.replace("**", "")
    return re.sub(r"^#+\s*", "", text, flags=re.M)


def ask_langflow(text, session_id):
    r = requests.post(
        f"{LF_URL}/api/v1/run/{FLOW_ID}",
        headers={"Content-Type": "application/json", "x-api-key": LF_KEY},
        json={
            "input_value": text,
            "input_type": "chat",
            "output_type": "chat",
            "session_id": session_id,
        },
        timeout=WAIT_LIMIT,
    )
    r.raise_for_status()
    return r.json()["outputs"][0]["outputs"][0]["results"]["message"]["text"]


def handle(chat_id, text):
    try:
        requests.post(f"{TG}/sendChatAction",
                      json={"chat_id": chat_id, "action": "typing"}, timeout=10)
        sid = f"tg-{chat_id}-{session_no.get(chat_id, 0)}"
        send(chat_id, clean(ask_langflow(text, sid)))
    except requests.Timeout:
        send(chat_id, "Maaf, prosesnya terlalu lama. Coba lagi sebentar lagi.")
    except Exception as e:  # jangan mencatat isi pesan
        print("error:", type(e).__name__)
        send(chat_id, "Maaf, terjadi kesalahan. Coba lagi sebentar lagi.")
    finally:
        with lock:
            busy.discard(chat_id)


def main():
    print("ModelRadar bot berjalan. Tekan Ctrl+C untuk berhenti.")
    offset = None
    while True:
        try:
            r = requests.get(f"{TG}/getUpdates",
                             params={"timeout": 30, "offset": offset}, timeout=40)
            updates = r.json().get("result", [])
        except Exception as e:
            print("koneksi Telegram bermasalah:", type(e).__name__)
            time.sleep(5)
            continue

        for upd in updates:
            offset = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg or "text" not in msg:
                continue
            chat_id, text = msg["chat"]["id"], msg["text"].strip()

            if text.startswith("/start"):
                send(chat_id, WELCOME)
                continue
            if text.startswith("/baru"):
                session_no[chat_id] = session_no.get(chat_id, 0) + 1
                send(chat_id, "Percakapan baru dimulai.")
                continue
            if len(text) > MAX_INPUT:
                send(chat_id, f"Pesan terlalu panjang (maksimal {MAX_INPUT} karakter).")
                continue

            now = time.time()
            with lock:
                if chat_id in busy:
                    send(chat_id, "Permintaanmu sebelumnya masih diproses, mohon tunggu.")
                    continue
                if now - last_msg.get(chat_id, 0) < COOLDOWN:
                    send(chat_id, "Mohon tunggu beberapa detik sebelum mengirim lagi.")
                    continue
                busy.add(chat_id)
                last_msg[chat_id] = now
            threading.Thread(target=handle, args=(chat_id, text), daemon=True).start()


if __name__ == "__main__":
    main()
