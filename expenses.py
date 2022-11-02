import requests
import re
import datetime
from bs4 import BeautifulSoup
from categories import Category, Categories
from typing import NamedTuple
from sheets import get_all_values, get_current_month_str, budget_sheet, get_range_of_values, transaction_sheet


class Expense(NamedTuple):
    amount: float
    category: Category
    currency: str

    def get_amount(self):
        return self.amount

    def get_category(self):
        return self.category.code_name

    def get_answer(self):
        return str(self.amount) + " " + str(self.currency) + " " + str(self.category.code_name)


class Message(NamedTuple):
    user_id: str
    user_name: str
    message_date: datetime.date
    expense: Expense
    raw_message: str

    def message_date_str(self):
        return self.message_date.strftime('%d.%m.%Y')

    def get_message_data(self):
        return [self.expense.get_amount(), self.expense.get_category(), self.message_date_str(), self.user_name, self.raw_message]


# TO DO: добавить исключение, если сообщение распозналось некорректно
def parse_message(raw_message: str) -> Expense:
    match = re.match(r'(\d+)(\$*) (.+)', raw_message)
    if not match.group(2):
        currency = 'lira'
    else:
        currency = 'usd'
    amount = float(match.group(1).replace(" ", ""))
    category = Categories().get_category(match.group(3))

    return Expense(amount=amount, category=category, currency=currency)


def add_expense(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    date = datetime.date.today()
    expense = parse_message(message.text)
    return Message(user_id=user_id, user_name=user_name, message_date=date, expense=expense, raw_message=message.text)


def _get_exchange_rate() -> float:
    url = 'https://freecurrencyrates.com/ru/convert-TRY-USD'
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", class_='src-entry-to')
    return float(convert[0].text)


def convert_lira_to_usd(lira_amount: int) -> float:
    current_rate = _get_exchange_rate()
    return lira_amount * current_rate


def get_month_statistics():
    values = get_all_values(budget_sheet)
    month_name = get_current_month_str()
    statistic = []
    for value in values:
        statistic.append(value['Category'] + ': ' + str(value[month_name]) + ' из ' + str(value['Limit']))
    return month_name, statistic


def get_last_ten_expenses():
    last_transaction = get_range_of_values(transaction_sheet, 'A2:E11')
    last_expenses = [Expense(amount=transaction[0], category=transaction[1], currency='currency') for transaction in last_transaction]
    return last_expenses









