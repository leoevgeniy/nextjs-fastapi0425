from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from api.services.gigachat import GigaChatService
import logging

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
gigachat = GigaChatService()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Проверяем подписку пользователя через API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.API_URL}/users/me",
            headers={"Authorization": f"Bearer {message.get_user_token()}"}
        )
        
        if response.status_code == 200:
            await message.answer("Добро пожаловать в ваш AI ассистент!")
        else:
            await message.answer("Пожалуйста, авторизуйтесь через сайт")

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        # Получаем ответ от GigaChat
        response = await gigachat.ask(
            prompt=message.text,
            user_id=message.from_user.id
        )
        
        await message.answer(response)
    
    except Exception as e:
        logging.error(f"Error in Telegram bot: {e}")
        await message.answer("Произошла ошибка, попробуйте позже")

async def on_startup(dp):
    await bot.set_webhook(settings.TELEGRAM_WEBHOOK_URL)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)