import os
from aiogram import Bot, Dispatcher, executor, types
from middleware import AccessMiddleware
import expenses
import exceptions
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
        "Бот для учёта расходов\n\n"
        "Добавить расход: 250 такси\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /last\n"
        "Просмотреть категории: /categories"
    )


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет расход"""
    message_text = message.text[4:]
    expense = expenses.parse_message(message_text)
    sheets.delete_expense_from_table(expense)
    await message.answer(f"Удалил {message_text}")


@dp.message_handler(commands=['last'])
async def get_last_ten_transaction(message: types.Message):
    """Выводит последние 10 внесенных расходов"""
    last_expenses = expenses.get_last_ten_expenses()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category} — нажми "
        f"/del{expense.amount}{expense.category} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


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
    try:
        expense_message = expenses.add_expense(message)
    except exceptions.IncorrectMessage as e:
        await message.answer(str(e))
        return
    try:
        sheets.add_expense_to_table(expense_message.expense)
    except ValueError:
        await message.answer("Не удалось внести значение в таблицу, ошибка в данных ячейки.")
        return
    sheets.add_transaction(expense_message)
    await message.answer(expense_message.expense.get_answer())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)