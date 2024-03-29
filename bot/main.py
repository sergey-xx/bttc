import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.fsm.context import FSMContext

import database as db
import keyboards as kb
from constants import TELEGRAM_TOKEN, MEDIA_ROOT, BASE_DIR, LOGS_FILENAME
from filters import Category, CategoryCallback
from paiment import create_payment
from states import AskAddress

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot=bot)
dp.callback_query.middleware(CallbackAnswerMiddleware())


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Стартует чат и сохраняет данные пользователя."""
    await db.add_user(from_user=message.from_user)
    # await db.get_shop_cart_items(message.from_user.id)
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}',
                         reply_markup=kb.main.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.main))
async def back_2_main(query: CallbackQuery,
                      callback_data: CategoryCallback):
    """Возращает в главное меню."""
    await query.message.edit_text(f'Вы вернулись в главное меню.',
                                  reply_markup=kb.main.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.head))
async def catalog(data: types.CallbackQuery):
    """Отдает каталог."""
    categories = await db.get_all_categories()
    catalog_kb = await kb.create_category_kb(categories=categories)
    await data.message.edit_text('Каталог', reply_markup=catalog_kb.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.cat))
async def sub_categories(query: CallbackQuery,
                         callback_data: CategoryCallback):
    """Отдает подкатегории."""
    cat_id = callback_data.id
    cat = await db.get_category(category_id=cat_id)
    subcats = await db.get_subcats(category_id=cat_id)
    sub_category_kb = await kb.create_subcategory_kb(subcats=subcats,
                                                     parent_id=cat.id,)
    await query.message.edit_text(cat.name,
                                  reply_markup=sub_category_kb.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.subcat))
async def get_items(query: CallbackQuery,
                    callback_data: CategoryCallback):
    """Отдает товары."""
    subcat_id = callback_data.id
    subcat = await db.get_subcat(subcat_id=subcat_id)
    items = await db.get_items(subcat_id=subcat_id)
    items_kb = await kb.create_items_kb(items=items,
                                        parent_id=subcat.category_id)
    
    await query.message.edit_text(subcat.name,
                                  reply_markup=items_kb.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.item))
async def get_certain_item(query: CallbackQuery,
                           callback_data: CategoryCallback):
    """Отдает конкретный товар."""
    item_id = callback_data.id
    item = await db.get_certain_item(item_id=item_id)
    item_kb = await kb.create_certain_item_kb(item=item,)
    if item.photo:
        image_path = MEDIA_ROOT / item.photo
        image = FSInputFile(image_path)
        await query.message.answer_photo(photo=image)
    await query.message.answer(f'{item.description} Цена:{item.price}₽',
                                  reply_markup=item_kb.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.add))
async def add_2_cart(query: CallbackQuery,
                     callback_data: CategoryCallback):
    """Добавляет в корзину."""
    item = await db.get_certain_item(item_id=callback_data.id)
    telegram_id = query.from_user.id
    cart_item = await db.add_item_2_cart(item_id=item.id,
                             telegram_id=telegram_id,)
    item = await db.get_certain_item(item_id=cart_item.item_id)
    await query.answer(text=(f'Товар {item.description[:10]} добавлен в '
                             'корзину в количестве {cart_item.amount}.'))


@dp.callback_query(CategoryCallback.filter(F.action == Category.shopping_cart))
async def show_cart(query: CallbackQuery,
                     callback_data: CategoryCallback):
    """Просмотр Корзины."""
    items = await db.get_shop_cart_items(telegram_id=query.from_user.id)
    overall = 0
    for item in items:
        overall += item.amount * item.price
    items_kb = await kb.create_cart_items_kb(items=items)
    await query.message.edit_text(f'Общая сумма корзины {overall}₽',
                                  reply_markup=items_kb.as_markup())


@dp.callback_query(CategoryCallback.filter(F.action == Category.delete))
async def delete_from_cart(query: CallbackQuery,
                           callback_data: CategoryCallback):
    """Удаление из корзины."""
    cart_item = await db.delete_item_from_cart(telegram_id=query.from_user.id,
                                               item_id=callback_data.id)
    if cart_item:
        item = await db.get_certain_item(item_id=cart_item.item_id)
        await query.answer(text=(f'Товар {item.description[:10]} удален из корзины.'))


@dp.callback_query(CategoryCallback.filter(F.action == Category.address))
async def get_address(query: CallbackQuery,
                      callback_data: CategoryCallback,
                      state: FSMContext):
    """Переход к оформлению."""
    await query.message.answer(text='Введите адрес для доставки.')
    await state.set_state(AskAddress.address)


@dp.message(AskAddress.address)
async def ask_confirm(message: types.Message, state: FSMContext):
    """Переход к оформлению."""
    await message.answer(text=f'Вы ввели адрес: \n {message.text}')
    await state.update_data(address=message.text)
    await state.set_state(AskAddress.confirm)
    await message.answer(text='Данные верны?',
                         reply_markup=kb.confirm_kb.as_markup())


@dp.message(AskAddress.confirm)
async def get_confirm(message: types.Message, state: FSMContext):
    """Проверка подтверждения адреса."""
    if message.text == "Да":
        data = await state.get_data()
        await db.make_order(telegram_id=message.from_user.id,
                            address=data.get('address'))
        overall = await db.get_overall(telegram_id=message.from_user.id)
        await state.clear()
        confirm_url, paiment_id = create_payment(overall)
        await db.add_payment(telegram_id=message.from_user.id,
                             payment_id=paiment_id)
        paiment_kb = await kb.create_paiment_kb(confirmation_url=confirm_url)
        await message.answer(text=f'Ваш заказ принят, Сумма к оплате {overall}',
                             reply_markup=paiment_kb.as_markup())
    else:
        await state.set_state(AskAddress.confirm)
        await message.answer(text='Введите адрес для доставки.')


@dp.message()
async def get_confirm():
    """Проверка платежа."""
    pass


async def main() -> None:
    """Точка входа."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    logs_path = BASE_DIR / 'logs' / LOGS_FILENAME

    logging.basicConfig(
        level=logging.INFO,
        filename=logs_path,
        filemode='a+',
        format='%(asctime)s, %(levelname)s, %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
