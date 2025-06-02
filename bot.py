import asyncio, json, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from download import download_audio

TOKEN = "7758509052:AAGhPRXvyunjQHflOFc9MTD1CiTxyexI-g0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

DB_FILE = "playlist.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎧 Отправь ссылку на трек или название!")

@dp.message(Command("playlist"))
async def show_playlist(message: types.Message):
    data = load_data()
    user_id = str(message.from_user.id)
    tracks = data.get(user_id, [])
    if not tracks:
        await message.answer("📭 Плейлист пуст.")
        return

    buttons = [
        [
            InlineKeyboardButton(text=f"▶️ {title[:30]}", callback_data=f"play_{i}"),
            InlineKeyboardButton(text="🗑", callback_data=f"delete_{i}")
        ]
        for i, title in enumerate(tracks)
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🎵 Твой плейлист:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("play_"))
async def play_track(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    data = load_data()
    tracks = data.get(str(callback.from_user.id), [])
    if index >= len(tracks):
        await callback.message.answer("⚠️ Трек не найден")
        return
    await callback.message.answer(f"⏳ Ищу: {tracks[index]}")
    file, _ = download_audio(f"ytsearch:{tracks[index]}")
    await callback.message.answer_audio(types.FSInputFile(file), caption=tracks[index])
    os.remove(file)
    await callback.answer()

@dp.callback_query(F.data.startswith("delete_"))
async def delete_track(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    data = load_data()
    user_id = str(callback.from_user.id)
    tracks = data.get(user_id, [])
    if index < len(tracks):
        removed = tracks.pop(index)
        save_data(data)
        await callback.message.answer(f"🗑 Удалено: {removed}")
    await callback.answer()

@dp.message()
async def handle_text(message: types.Message):
    query = message.text.strip()
    await message.answer("⏳ Скачиваю...")
    try:
        file, title = download_audio(query)
        await message.answer_audio(types.FSInputFile(file), caption=title)
        os.remove(file)

        data = load_data()
        user_id = str(message.from_user.id)
        data.setdefault(user_id, []).append(title)
        save_data(data)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
