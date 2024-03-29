from aiogram.filters import Filter
from aiogram import types
from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class MyFilter(Filter):
    """Фильтр для CallBack."""

    def __init__(self, callback_data: str) -> None:
        self.callback_data = callback_data

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.callback_data


class Category(str, Enum):
    main = 'main'
    head = 'head'
    cat = 'cat'
    subcat = 'subcat'
    item = 'item'
    shopping_cart = 'shopping_cart'
    add = 'add'
    delete = 'delete'
    address = 'address'


class CategoryCallback(CallbackData, prefix='cat'):
    action: Category
    id: int
