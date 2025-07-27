import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageEnhance
import io
import rembg

TOKEN = "8307033370:AAFr9g1ozkx9o5dWNA-QAETbeh6q6CSw9dI

"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أرسل صورة وسأقوم بتعديلها ✨")

def process_image(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_bytes = photo_file.download_as_bytearray()

    img_no_bg = rembg.remove(photo_bytes)
    img = Image.open(io.BytesIO(img_no_bg)).convert("RGBA")

    enhancer_brightness = ImageEnhance.Brightness(img)
    img = enhancer_brightness.enhance(1.2)
    enhancer_contrast = ImageEnhance.Contrast(img)
    img = enhancer_contrast.enhance(1.3)

    dpi = 300
    width_cm, height_cm = 3.7, 5
    width_px = int(width_cm / 2.54 * dpi)
    height_px = int(height_cm / 2.54 * dpi)
    img = img.resize((width_px, height_px), Image.ANTIALIAS)

    a4_width, a4_height = 2480, 3508
    canvas = Image.new("RGBA", (a4_width, a4_height), (255, 255, 255, 255))

    for i in range(10):
        x = i * width_px
        canvas.paste(img, (x, 0), img)

    output_buffer = io.BytesIO()
    canvas.convert("RGB").save(output_buffer, format="JPEG")
    output_buffer.seek(0)

    update.message.reply_photo(photo=output_buffer, caption="تم تعديل الصورة ✅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, process_image))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
