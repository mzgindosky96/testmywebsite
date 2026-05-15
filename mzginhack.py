import os
import time
import uuid
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ================== CONFIGURATION ==================
BOT_TOKEN = "AAH8cZ8mwikGQYsR1Nub4CndfNi9X8sEnxA"  # Your Bot Token

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create directories for images
os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)

# ================== Processor Class ==================
class Processor:
    URL = "https://pornworks.com/api/v2"
    HEADERS = {'User-Agent': 'Mozilla/5.0'}

    def upload(self, path):
        try:
            with open(path, 'rb') as f:
                r = requests.put(f"{self.URL}/uploads/undress", headers=self.HEADERS, files={'file': f}, timeout=60)
            if "child" in r.text.lower():
                return "CHILD_DETECTED"
            return r.json().get("url") or r.json().get("data", {}).get("url")
        except:
            return None

    def generate(self, url, pose="auto", clear=True):
        prompts = {
            "doggy": "doggy style, high quality, clear" if clear else "doggy style, high quality, blurry",
            "squirt": "squirting, high detail, clear" if clear else "squirting, high detail, blurry",
            "legs": "open legs, spreading, clear" if clear else "open legs, spreading, blurry",
            "spicy": "sexy pose, spicy, detailed, clear" if clear else "sexy pose, spicy, detailed, blurry"
        }
        target_prompt = prompts.get(pose, "high quality, clear" if clear else "high quality, blurry")
        try:
            r = requests.post(
                f"{self.URL}/generate/undress",
                headers=self.HEADERS,
                json={"image": url, "gender": "auto", "prompt": target_prompt},
                timeout=60
            )
            return r.json().get("id") or r.json().get("data", {}).get("id")
        except:
            return None

    def wait_done(self, gen_id):
        for _ in range(60):
            try:
                r = requests.get(f"{self.URL}/generations/{gen_id}/state", headers=self.HEADERS, timeout=30)
                state = r.json().get("state") or r.json().get("data", {}).get("state")
                if state in ["done", "completed", "success"]:
                    return True
                time.sleep(2)
            except:
                time.sleep(2)
        return False

    def result(self, gen_id):
        try:
            r = requests.get(f"{self.URL}/generations/{gen_id}", headers=self.HEADERS, timeout=60)
            res = r.json().get("results") or r.json().get("data", {}).get("results", {})
            url = res.get("image") or res.get("output") or res.get("url")
            return f"https:{url}" if url and url.startswith("//") else url
        except:
            return None

# ================== Handlers ==================

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("started"):
        msg = ("Welcome! This bot can edit images and adjust poses.\n"
               "Click the button below to get started.")
        keyboard = [
            [InlineKeyboardButton("Connect TikTok Profile", url="https://www.tiktok.com/@_72mg")],
            [InlineKeyboardButton("✅ Done", callback_data="done")]
        ]
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        context.user_data["started"] = True

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "done":
        await query.message.reply_text("Please send a photo of a woman. After sending, click the 🔥 button.")
        context.user_data["awaiting_photo"] = True

    elif data == "generate_photo":
        # Find the stored image path
        image_path = None
        for key in context.user_data:
            if key.startswith("images/"):
                image_path = context.user_data[key]
                break
        if not image_path:
            await query.message.reply_text("No image found to generate from. Please send a photo first.")
            return

        await query.message.reply_text("Generating your photo, please wait...")

        try:
            processor = Processor()
            # Upload image to get URL
            up_url = processor.upload(image_path)
            if up_url == "CHILD_DETECTED":
                await query.message.reply_text("Child detected. Cannot process this image.")
                return

            # Generate image (set clear=True for sharp, False for blurry)
            gen_id = processor.generate(up_url, clear=True)  # Change to False for blurry
            if gen_id and processor.wait_done(gen_id):
                res_url = processor.result(gen_id)
                if res_url:
                    img_data = requests.get(res_url).content
                    res_path = "results/generated.jpg"
                    with open(res_path, "wb") as f:
                        f.write(img_data)
                    await query.message.reply_document(document=open(res_path, "rb"))
                else:
                    await query.message.reply_text("Failed to get generated image.")
            else:
                await query.message.reply_text("Generation did not complete in time.")
        except Exception as e:
            print(f"Error during generation: {e}")
            await query.message.reply_text("Error generating image.")

# When user sends media
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_photo"):
        uid = str(uuid.uuid4())[:8]
        path = f"images/{uid}.jpg"
        file_obj = None
        if update.message.photo:
            file_obj = await update.message.photo[-1].get_file()
        elif update.message.document:
            file_obj = await update.message.document.get_file()
        if not file_obj:
            await update.message.reply_text("Please send a valid photo.")
            return
        await file_obj.download_to_drive(path)
        # Save image path with key starting with "images/"
        context.user_data["images/" + uid] = path
        # Send confirmation with generate button
        keyboard = [
            [InlineKeyboardButton("🔥", callback_data="generate_photo")]
        ]
        await update.message.reply_text("Click 🔥 to generate the photo.", reply_markup=InlineKeyboardMarkup(keyboard))
        # Reset flag
        context.user_data["awaiting_photo"] = False
    else:
        await update.message.reply_text("Please press the '✅ Done' button first and then send a photo.")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_media))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
