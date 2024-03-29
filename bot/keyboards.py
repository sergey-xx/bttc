from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from filters import Category, CategoryCallback

main = InlineKeyboardBuilder()
main.button(text='Каталог',
            callback_data=CategoryCallback(action=Category.head,
                                           id=0),)
main.button(text='Корзина',
            callback_data=CategoryCallback(action=Category.shopping_cart,
                                           id=0),)


async def create_category_kb(categories) -> InlineKeyboardBuilder:
    category_kb = InlineKeyboardBuilder()
    for category in categories:
        category_kb.button(
            text=category.name,
            callback_data=CategoryCallback(action=Category.cat,
                                           id=category.id),
        )
    category_kb.button(
            text='В главное меню',
            callback_data=CategoryCallback(action=Category.main,
                                           id=0))
    category_kb.adjust(1)
    return category_kb


async def create_subcategory_kb(subcats,
                                parent_id: int) -> InlineKeyboardBuilder:
    subcat_kb = InlineKeyboardBuilder()

    for subcat in subcats:
        subcat_kb.button(
            text=subcat.name,
            callback_data=CategoryCallback(action=Category.subcat,
                                           id=subcat.id),
        )
    subcat_kb.button(
            text='Назад',
            callback_data=CategoryCallback(action=Category.head,
                                           id=parent_id))
    subcat_kb.adjust(1)
    return subcat_kb


async def create_items_kb(items,
                          parent_id: int) -> InlineKeyboardBuilder:
    items_kb = InlineKeyboardBuilder()
    for item in items:
        items_kb.button(
            text=item.description,
            callback_data=CategoryCallback(action=Category.item,
                                           id=item.id),
        )
    items_kb.button(
            text='Назад',
            callback_data=CategoryCallback(action=Category.cat,
                                           id=parent_id))
    items_kb.adjust(1)
    return items_kb


async def create_certain_item_kb(item) -> InlineKeyboardBuilder:
    item_kb = InlineKeyboardBuilder()
    item_kb.button(
            text='Добавить в корзину',
            callback_data=CategoryCallback(action=Category.add,
                                           id=item.id))
    item_kb.button(
            text='Удалить из корзины',
            callback_data=CategoryCallback(action=Category.delete,
                                           id=item.id))
    item_kb.button(
            text='Назад',
            callback_data=CategoryCallback(action=Category.subcat,
                                           id=item.sub_category_id))
    item_kb.adjust(1)
    return item_kb


async def create_cart_items_kb(items) -> InlineKeyboardBuilder:
    items_kb = InlineKeyboardBuilder()
    for item in items:
        items_kb.button(
            text=(f'{item.description} - {item.amount} шт.'),
            callback_data=CategoryCallback(action=Category.item,
                                           id=item.id),
        )
    items_kb.button(
            text='Оформить заказ',
            callback_data=CategoryCallback(action=Category.address,
                                           id=0))
    items_kb.button(
            text='Назад',
            callback_data=CategoryCallback(action=Category.main,
                                           id=0))
    items_kb.adjust(1)
    return items_kb


confirm_kb = ReplyKeyboardBuilder()
confirm_kb.button(text='Да')
confirm_kb.button(text='Нет')


async def create_paiment_kb(confirmation_url) -> InlineKeyboardBuilder:
    paiment_kb = InlineKeyboardBuilder()
    paiment_kb.button(text='Ссылка для оплаты',
                      url=confirmation_url)
    return paiment_kb