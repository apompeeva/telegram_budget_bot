import re
import datetime
from categories import Category, Categories
from typing import NamedTuple, List
from sheets import get_all_values, get_current_month_name, budget_sheet, get_range_of_values, transaction_sheet


class Expense(NamedTuple):
    amount: float
    category: Category

    def get_amount(self):
        return self.amount

    def get_category(self):
        return self.category.code_name

    def get_answer(self):
        return str(self.amount) + " " + str(self.category.code_name)


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
    match = re.match(r'(\d+) *(.+)', raw_message)

    amount = float(match.group(1).replace(" ", ""))
    category = Categories().get_category(match.group(2))

    return Expense(amount=amount, category=category)


def add_expense(message) -> Message:
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    date = datetime.date.today()
    expense = parse_message(message.text)
    return Message(user_id=user_id, user_name=user_name, message_date=date, expense=expense, raw_message=message.text)


def get_month_statistics() -> (str, List):
    values = get_all_values(budget_sheet)
    month_name = get_current_month_name()
    statistic = [f"{value['Category']}: {str(value[month_name])}руб. из {str(value['Limit'])}руб." for value in values]
    return month_name, statistic


def get_last_ten_expenses() -> List:
    last_transaction = get_range_of_values(transaction_sheet, 'A2:E11')
    last_expenses = [Expense(amount=transaction[0], category=transaction[1]) for transaction in last_transaction]
    return last_expenses









