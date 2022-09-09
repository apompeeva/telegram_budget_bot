from typing import List
from sheets import get_all_values, categories_sheet


class Category:
    code_name: str
    description: str
    aliases: List[str]

    def __init__(self, category):
        self.code_name = category['Category']
        self.description = category['Description']
        self.aliases = category['Aliases'].split(", ")

    def get_category_data(self):
        return '\n' + self.code_name + ' - ' + self.description + '\n' + ', '.join([str(elem) for elem in self.aliases])


class Categories:

    def __init__(self):
        self._categories = []
        categories = get_all_values(categories_sheet)
        for category in categories:
            self._categories.append(Category(category))

    def get_all_categories(self) -> List[Category]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        finded = None
        other_category = None
        for category in self._categories:
            if category.code_name == "Other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded

