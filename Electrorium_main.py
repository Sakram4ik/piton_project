import telebot  # Імпортуємо бібліотеку для роботи з Telegram Bot API
from telebot import types  # Імпортуємо модуль types для створення клавіатур та інших елементів інтерфейсу
import datetime  # Імпортуємо модуль datetime для роботи з датою та часом

TOKEN = "8110054911:AAF7Qxhwb5vgu7yRXBiAVKMKOtQ7hUYQHZQ"  # Токен вашого Telegram-бота. Зберігайте його в безпеці!
bot = telebot.TeleBot(TOKEN)  # Створюємо екземпляр бота

REGISTRATION_PROCESS = {}  # Словник для зберігання стану запису користувачів.
                            # Ключем буде chat_id користувача, а значенням - інший словник з даними процесу реєстрації.


def log_registration(user_id, username, name, game, time):
    """
    Записує дані про реєстрацію користувача у файл.

    Args:
        user_id (int): ID користувача Telegram.
        username (str): Нікнейм користувача Telegram.
        name (str): Ім'я користувача, яке він ввів.
        game (str): Обрана гра для запису.
        time (str): Бажаний час гри.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Отримуємо поточний час у форматі РРРР-ММ-ДД ГГ:ХХ:СС
    with open("electrorium_registrations.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ID: {user_id}, Username: @{username}, Ім'я: {name}, Гра: {game}, Час: {time}\n")


# Обробник команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Обробляє команду /start. Відправляє вітальне повідомлення з основним меню.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id  # Отримуємо ID чату користувача
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Створюємо об'єкт клавіатури
    btn1 = types.KeyboardButton("🎮 Розклад ігор")  # Створюємо кнопку "Розклад ігор"
    btn2 = types.KeyboardButton("🕹️ Записатися на гру")  # Створюємо кнопку "Записатися на гру"
    btn3 = types.KeyboardButton("📞 Контакти")  # Створюємо кнопку "Контакти"
    btn4 = types.KeyboardButton("ℹ️ Про клуб")  # Створюємо кнопку "Про клуб"
    markup.add(btn1, btn2, btn3, btn4)  # Додаємо кнопки до клавіатури

    bot.send_message(
        chat_id,
        "👾 Вітаємо в ігровому клубі <b>Electrorium</b>!\n"
        "Оберіть опцію з меню:",
        parse_mode="HTML",  # Вказуємо, що в тексті є HTML-теги для форматування
        reply_markup=markup  # Відправляємо клавіатуру разом з повідомленням
    )
    REGISTRATION_PROCESS[chat_id] = {}  # Ініціалізуємо порожній словник для зберігання стану реєстрації нового користувача


# Обробка натискання кнопки "Записатися на гру"
@bot.message_handler(func=lambda message: message.text == "🕹️ Записатися на гру")
def ask_name(message):
    """
    Обробляє натискання кнопки "Записатися на гру". Запитує ім'я користувача.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Створюємо клавіатуру
    btn_back = types.KeyboardButton("⬅️ Назад")  # Створюємо кнопку "Назад"
    markup.add(btn_back)  # Додаємо кнопку "Назад" до клавіатури
    bot.send_message(chat_id, "Будь ласка, введіть ваше ім'я:", reply_markup=markup)  # Запитуємо ім'я та відправляємо клавіатуру з кнопкою "Назад"
    REGISTRATION_PROCESS[chat_id] = {"step": "waiting_for_name"}  # Встановлюємо стан очікування імені


# Обробка введення імені
@bot.message_handler(func=lambda message: REGISTRATION_PROCESS.get(message.chat.id, {}).get("step") == "waiting_for_name")
def ask_game_time(message):
    """
    Обробляє введення імені користувача. Запитує бажаний день та час гри.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id
    if message.text == "⬅️ Назад":  # Перевіряємо, чи натиснута кнопка "Назад"
        send_welcome(message)  # Повертаємося до головного меню
        del REGISTRATION_PROCESS[chat_id]  # Видаляємо стан реєстрації користувача
        return
    REGISTRATION_PROCESS[chat_id]["name"] = message.text  # Зберігаємо введене ім'я
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)  # Створюємо клавіатуру
    btn_back = types.KeyboardButton("⬅️ Назад")  # Створюємо кнопку "Назад"
    markup.add(btn_back)  # Додаємо кнопку "Назад" до клавіатури
    bot.send_message(chat_id, "Вкажіть бажаний день та час гри (наприклад: Завтра 19:00):", reply_markup=markup)  # Запитуємо час та відправляємо клавіатуру з кнопкою "Назад"
    REGISTRATION_PROCESS[chat_id]["step"] = "waiting_for_game_time"  # Встановлюємо стан очікування часу гри


# Обробка введення бажаного дня та часу
@bot.message_handler(func=lambda message: REGISTRATION_PROCESS.get(message.chat.id, {}).get("step") == "waiting_for_game_time")
def ask_game(message):
    """
    Обробляє введення бажаного дня та часу гри. Запитує вибір гри.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id
    if message.text == "⬅️ Назад":  # Перевіряємо, чи натиснута кнопка "Назад"
        ask_name(message)  # Повертаємося до запиту імені
        REGISTRATION_PROCESS[chat_id]["step"] = "waiting_for_name"  # Оновлюємо стан
        return
    REGISTRATION_PROCESS[chat_id]["time"] = message.text  # Зберігаємо введений час
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)  # Створюємо одноразову клавіатуру з кнопками в 3 стовпці
    btn1 = types.KeyboardButton("Counter-Strike: GO")
    btn2 = types.KeyboardButton("Dota 2")
    btn3 = types.KeyboardButton("League of Legends")
    btn4 = types.KeyboardButton("Valorant")
    btn5 = types.KeyboardButton("Fortnite")
    btn6 = types.KeyboardButton("Apex Legends")
    btn_back = types.KeyboardButton("⬅️ Назад")  # Кнопка "Назад"
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn_back)  # Додаємо кнопки ігор та "Назад"
    bot.send_message(chat_id, "Оберіть гру:", reply_markup=markup)  # Запитуємо вибір гри та відправляємо клавіатуру
    REGISTRATION_PROCESS[chat_id]["step"] = "waiting_for_game"  # Встановлюємо стан очікування вибору гри


# Обробка вибору гри
@bot.message_handler(func=lambda message: REGISTRATION_PROCESS.get(message.chat.id, {}).get("step") == "waiting_for_game")
def process_registration(message):
    """
    Обробляє вибір гри користувачем. Завершує процес реєстрації.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id
    if message.text == "⬅️ Назад":  # Перевіряємо, чи натиснута кнопка "Назад"
        ask_game_time(message)  # Повертаємося до запиту часу гри
        REGISTRATION_PROCESS[chat_id]["step"] = "waiting_for_game_time"  # Оновлюємо стан
        return
    game = message.text  # Отримуємо обрану гру
    user_id = message.from_user.id  # Отримуємо ID користувача
    username = message.from_user.username  # Отримуємо нікнейм користувача
    name = REGISTRATION_PROCESS[chat_id].get("name")  # Отримуємо ім'я з тимчасового словника
    time = REGISTRATION_PROCESS[chat_id].get("time")  # Отримуємо час гри з тимчасового словника

    if name and time and game:  # Перевіряємо, чи всі необхідні дані є
        log_registration(user_id, username, name, game, time)  # Записуємо дані про реєстрацію
        bot.send_message(chat_id, f"✅ Вас успішно записано на гру:\n"
                                    f"Ім'я: {name}\n"
                                    f"Час: {time}\n"
                                    f"Гра: {game}", reply_markup=types.ReplyKeyboardRemove())  # Відправляємо підтвердження та видаляємо клавіатуру
        del REGISTRATION_PROCESS[chat_id]  # Очищаємо стан реєстрації користувача
    else:
        bot.send_message(chat_id, "⚠️ Виникла помилка при обробці запису. Будь ласка, спробуйте ще раз.", reply_markup=types.ReplyKeyboardRemove())  # Повідомляємо про помилку та видаляємо клавіатуру
        del REGISTRATION_PROCESS[chat_id]  # Очищаємо стан реєстрації користувача


# Обробка інших основних повідомлень (кнопки головного меню)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    """
    Обробляє текстові повідомлення, які відповідають кнопкам головного меню.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    chat_id = message.chat.id
    if message.text == "🎮 Розклад ігор":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Назад")
        markup.add(btn_back)
        bot.send_message(
            chat_id,
            "<b>🕒 Розклад турнірів:</b>\n\n"
            "<u>🔹 Понеділок/Середа/П'ятниця:</u>\n"
            "    - 14:00 - Турнір з Counter-Strike: GO\n"
            "    - 18:00 - Вільні ігри в Dota 2\n\n"
            "<u>🔹 Вівторок/Четвер:</u>\n"
            "    - 16:00 - Збірні ігри в League of Legends\n"
            "    - 20:00 - Вечірні катки у Valorant\n\n"
            "<u>🔹 Субота/Неділя:</u>\n"
            "    - 15:00 - Турніри вихідного дня (різні ігри)\n"
            "    - 19:00 - Вільна гра в Fortnite/Apex Legends",
            parse_mode="HTML",
            reply_markup=markup
        )
    elif message.text == "📞 Контакти":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Назад")
        markup.add(btn_back)
        bot.send_message(
            chat_id,
            "<b>📞 Наші контакти:</b>\n\n"
            "📍 <i>Адреса:</i> м. Київ, вул. Ігрова, 7\n"
            "📱 <i>Телефон:</i> +380 66 555 55 55\n"
            "🕒 <i>Графік роботи:</i> 12:00 - 00:00\n\n"
            "🌐 <a href='https://electrorium.gg'>Наш сайт</a>",
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=markup
        )
    elif message.text == "ℹ️ Про клуб":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("⬅️ Назад")
        markup.add(btn_back)
        bot.send_message(
            chat_id,
            "<b>🕹️ Про клуб Electrorium</b>\n\n"
            "Сучасний ігровий клуб з:\n"
            "✅ Потужними комп'ютерами\n"
            "✅ Професійними девайсами\n"
            "✅ Затишною атмосферою\n"
            "✅ Регулярними турнірами та івентами\n\n"
            "<i>Приєднуйся до нашої геймерської спільноти!</i> 👾",
            parse_mode="HTML",
            reply_markup=markup
        )
    elif message.text == "⬅️ Назад":
        send_welcome(message)  # Повертаємося до головного меню
    else:
        bot.send_message(chat_id, "Вибачте, я не розумію цієї команди. Будь ласка, скористайтеся меню.")


# Обробка невідомих команд (якщо користувач введе щось, що не є командою або кнопкою)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    """
    Обробляє всі інші текстові повідомлення, які не були оброблені попередніми функціями.
    Відправляє повідомлення про невідому команду.

    Args:
        message (telebot.types.Message): Об'єкт повідомлення від Telegram.
    """
    bot.reply_to(message, "Вибачте, я не розумію цієї команди. Будь ласка, скористайтеся меню.")


# Запуск бота
print("Бот Electrorium запущено...")
bot.polling(none_stop=True)  # Запускаємо нескінченний цикл отримання оновлень від Telegram