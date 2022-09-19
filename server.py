import os
from aiogram import Bot, Dispatcher, executor, types
from middleware import AccessMiddleware
import expenses
import sheets
from categories import Categories


API_TOKEN = os.getenv('API_TOKEN')
ACCESS_ID = [int(x) for x in os.getenv('ACCESS_ID').split(",")]

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories")


async def del_expense(message: types.Message):
    """Удаляет расход"""
    await message.answer("")


@dp.message_handler(commands=['today'])
async def get_today_expenses(message: types.Message):
    """Выводит расходы за сегодня"""
    await message.answer("Расходы за сегодня")


@dp.message_handler(commands=['week'])
async def get_week_expenses(message: types.Message):
    """Выводит расходы за неделю"""
    await message.answer("Расходы за неделю")


@dp.message_handler(commands=['month'])
async def get_month_expenses(message: types.Message):
    """Выводит расходы за месяц"""
    month, answer = expenses.get_month_statistics()
    await message.answer(f"Расходы за {month}" + '\n' + ('\n'.join(answer)))


@dp.message_handler(commands=['categories'])
async def get_all_categories(message: types.Message):
    """Выводит список категорий с алиасами и лимитами"""
    answer = Categories().get_all_categories()
    await message.answer('\n'.join([category.get_category_data() for category in answer]))


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    expense_message = expenses.add_expense(message)
    sheets.add_transaction(expense_message)
    sheets.add_expense_to_table(expense_message.expense)
    await message.answer(expense_message.expense.get_answer())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)