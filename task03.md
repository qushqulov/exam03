# Task 3: Random Image Bot

## Loyiha Haqida

### Nima Qilamiz?
Telegram bot yozasiz. Bot random hayvonlar rasmlarini yuboradi: it, mushuk yoki tulki.

### Bot Qanday Ishlaydi? (UX)

**Foydalanuvchi tajribasi:**

```
👤 Foydalanuvchi: /start

🤖 Bot: Qaysi hayvon rasmini ko'rmoqchisiz?
       [tugmalar ko'rsatadi]
       🐶 Dog    🐱 Cat    🦊 Fox

👤 Foydalanuvchi: [🐱 Cat tugmasini bosadi]

🤖 Bot: [Random mushuk rasmini yuboradi]

👤 Foydalanuvchi: /dog

🤖 Bot: [Random it rasmini yuboradi]
```

**Asosiy xususiyatlar:**
- 3 xil hayvon: it, mushuk, tulki
- Har safar BOSHQA rasm (random API dan)
- Rasm **to'g'ridan-to'g'ri yuboriladi** (link emas!)
- Inline tugmalar bilan qulay interfeys

---

## Texnik Ma'lumot

### Ishlatadigan API lar

Bot 3 ta bepul public API dan foydalanadi:

**1. Dog API 🐶**
```
URL: https://dog.ceo/api/breeds/image/random
```
Response:
```json
{
  "message": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg",
  "status": "success"
}
```

**2. Cat API 🐱**
```
URL: https://api.thecatapi.com/v1/images/search
```
Response:
```json
[
  {
    "url": "https://cdn2.thecatapi.com/images/abc.jpg"
  }
]
```

**3. Fox API 🦊**
```
URL: https://randomfox.ca/floof/
```
Response:
```json
{
  "image": "https://randomfox.ca/images/32.jpg"
}
```

---

## Task Talablari

### 1. Texnologiya
- `python-telegram-bot==13.15` (muhim: versiya 13.15)
- `requests` kutubxonasi

### 2. Arxitektura

Kod **3 ta class**ga bo'linishi kerak:

```
ImageBot
 ├── APIClient      - API ga request yuboradi
 ├── ImageService   - qaysi API ishlatishni tanlaydi  
 └── Handlers       - faqat Telegram bilan ishlaydi
```

**Qoidalar:**
- Handler ichida `requests` ishlatish **TAQIQLANADI**
- Barcha kod bitta faylda bo'lsa → FAIL
- Classlar bo'lmasa → FAIL

---

### 3. Bot Buyruqlari

#### `/start`
Inline keyboard (tugmalar) ko'rsatadi:

```
🐶 Dog    🐱 Cat    🦊 Fox
```

**Tugma bosilganda:**
- Bot tegishli API dan rasm oladi
- `bot.send_photo(chat_id, image_url)` orqali yuboradi

#### `/dog`
Random it rasmini yuboradi

#### `/cat`
Random mushuk rasmini yuboradi

#### `/fox`
Random tulki rasmini yuboradi

---

### 4. Classlar Tuzilishi

#### `APIClient`

HTTP requestlarni bajaradi.

**Method:**
```python
get_image_url(api_type: str) -> str
```

- `api_type`: "dog", "cat", "fox"
- Tegishli API ga request yuboradi
- JSON dan rasm URL ni parse qiladi
- URL qaytaradi

---

#### `ImageService`

Biznes logika - qaysi API ishlatishni biladi.

**Method:**
```python
fetch_random_image(animal: str) -> str
```

- `animal`: "dog", "cat", "fox"
- `APIClient` ni chaqiradi
- Rasm URL ni qaytaradi

---

#### `Handlers`

Faqat Telegram bilan ishlaydi.

**Metodlar:**

```python
start_command(update, context) -> None
```
- Inline keyboard yuboradi

```python
button_handler(update, context) -> None
```
- Tugma bosilganda ishga tushadi
- `ImageService` dan rasm oladi
- `send_photo()` bilan yuboradi

```python
dog_command(update, context) -> None
cat_command(update, context) -> None
fox_command(update, context) -> None
```
- Har biri o'z hayvonining rasmini yuboradi

---

## 5. Foydalanish Misoli

```python
# main.py

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from image_bot import ImageBot

def main():
    # Bot yaratish
    bot = ImageBot(token="YOUR_TOKEN")
    
    # Updater sozlash
    updater = Updater(bot.token)
    dp = updater.dispatcher
    
    # Handlerlarni qo'shish
    dp.add_handler(CommandHandler('start', bot.handlers.start_command))
    dp.add_handler(CommandHandler('dog', bot.handlers.dog_command))
    dp.add_handler(CommandHandler('cat', bot.handlers.cat_command))
    dp.add_handler(CommandHandler('fox', bot.handlers.fox_command))
    dp.add_handler(CallbackQueryHandler(bot.handlers.button_handler))
    
    # Ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```

---

## 6. Muhim Nuqtalar

### ✅ To'g'ri:
```python
# Handler ichida
def dog_command(update, context):
    url = image_service.fetch_random_image("dog")
    context.bot.send_photo(chat_id=chat_id, photo=url)
```

### ❌ Noto'g'ri:
```python
# Handler ichida requests ishlatish TAQIQLANADI
def dog_command(update, context):
    response = requests.get("https://dog.ceo/...")  # FAIL!
    context.bot.send_message(text=url)  # Link yuborish FAIL!
```

---

## 7. Test Kriteryalari

Student **yiqiladi** agar:

❌ Handler ichida `requests` ishlatsa

❌ Inline keyboard bo'lmasa

❌ `send_photo()` o'rniga `send_message()` ishlatsa (link yuborish)

❌ Barcha kod bitta faylda bo'lsa (class strukturasiz)

❌ API response to'g'ri parse qilinmasa (har bir API formati boshqacha)

---

## 8. Nimani O'rganasiz

| Skill | Ma'nosi |
|-------|---------|
| **requests** | Tashqi API bilan ishlash |
| **JSON parsing** | Turli formatlarni handle qilish |
| **Telegram media** | `send_photo()` ishlatish |
| **Separation** | Handler/Service/Client ajratish |
| **Keyboard** | Inline buttons yaratish |

---

## 9. Qo'shimcha Ma'lumotlar

### Inline Keyboard Yaratish

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [
        InlineKeyboardButton("🐶 Dog", callback_data='dog'),
        InlineKeyboardButton("🐱 Cat", callback_data='cat'),
        InlineKeyboardButton("🦊 Fox", callback_data='fox')
    ]
]
reply_markup = InlineKeyboardMarkup(keyboard)
update.message.reply_text('Tanlang:', reply_markup=reply_markup)
```

### Rasm Yuborish

```python
# To'g'ri
context.bot.send_photo(chat_id=chat_id, photo=image_url)

# Noto'g'ri
context.bot.send_message(chat_id=chat_id, text=image_url)
```
