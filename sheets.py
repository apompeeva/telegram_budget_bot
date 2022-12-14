import gspread
import datetime
from typing import List, Dict, Tuple

# from expenses import Message, Expense

gc = gspread.service_account()
sh = gc.open("TurkeyBudget")
budget_sheet = sh.worksheet("2022")
transaction_sheet = sh.worksheet("Transaction")
categories_sheet = sh.worksheet("Categories")


def get_value(cell: Tuple[int, int]) -> str:
    data = budget_sheet.cell(*cell).value
    return data


def get_range_of_values(sheet, range) -> List:
    values = sheet.get(range)
    return values


def get_all_values(sheet) -> Dict:
    values = sheet.get_all_records()
    return values


def find_cell_by_value(value):
    cell = budget_sheet.find(value)
    return cell


def get_current_month_name() -> str:
    current_date = datetime.datetime.now()
    return current_date.strftime("%B")


def get_cell_address(category: str) -> Tuple[int, int]:
    category_address = find_cell_by_value(category)
    month_address = find_cell_by_value(get_current_month_name())
    return category_address.row, month_address.col


def add_expense_to_table(expense):
    cell_address = get_cell_address(expense.get_category())
    try:
        current_value = int(get_value(cell_address))
    except ValueError:
        raise
    new_data = current_value + int(expense.get_amount())
    budget_sheet.update_cell(*cell_address, str(new_data))


def delete_expense_from_table(expense):
    cell_address = get_cell_address(expense.get_category())
    current_value = get_value(cell_address)
    try:
        new_data = int(current_value) - int(expense.get_amount())
    except TypeError:
        print("Какая то дичь с типами")
        raise
    budget_sheet.update_cell(*cell_address, str(new_data))


def add_transaction(transaction):
    transaction_sheet.insert_row(transaction.get_message_data(), index=2, value_input_option='USER_ENTERED')

