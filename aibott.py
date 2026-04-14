import anthropic
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

TELEGRAM_TOKEN = os.getenv("8453781858:AAFAWr37co76pPS21PxT8ADbcqJ9khP0Q8c")
ANTHROPIC_KEY = os.getenv("sk-183cc7bf565999ad833e51a894a9254456b99a9f66df1d05")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

memory = {}

@dp.message(Command("start"))
async def start(msg: types.Message):
    memory[msg.from_user.id] = []
    await msg.answer("👋 Привет! Я AI-ассистент. Пиши что хочешь!")

@dp.message(Command("clear"))
async def clear(msg: types.Message):
    memory[msg.from_user.id] = []
    await msg.answer("🧹 Память очищена!")

@dp.message()
async def handle(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in memory:
        memory[user_id] = []
    memory[user_id].append({"role": "user", "content": msg.text})
    if len(memory[user_id]) > 20:
        memory[user_id] = memory[user_id][-20:]
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="Ты полезный ассистент. Отвечай кратко и по делу.",
            messages=memory[user_id]
        )
        answer = response.content[0].text
        memory[user_id].append({"role": "assistant", "content": answer})
        await msg.answer(answer)
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
