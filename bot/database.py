from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from constants import (POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT, POSTGRES_PASSWORD,
                       POSTGRES_USER)
from models import Category, User, SubCategory, Item, CartItem, ShoppingCart

engine = create_async_engine(
        (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:'
         f'{POSTGRES_PORT}/{POSTGRES_DB}'),
        # echo=True,
    )

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def add_user(from_user):
    """Добавляет пользователя в БД."""
    username = from_user.username
    if from_user.username is None:
        username = str(from_user.id)
    new_user = User(
        telegram_id=from_user.id,
        first_name=from_user.first_name,
        last_name=from_user.last_name,
        username=username
    )
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(User).where(
            User.telegram_id == from_user.id
        ))
        user = db_obj.scalars().first()
        if not user:
            session.add(new_user)
            await session.commit()
            await session.refresh(user)
            return user


async def get_user(telegram_id: int) -> User:
    """Получаем Юзера по telegram_id."""

    async with AsyncSessionLocal() as session:
        user = await session.execute(select(User).where(
            User.telegram_id == telegram_id
        ))
        return user.scalars().first()


async def get_all_categories():
    """Получаем все категории."""

    async with AsyncSessionLocal() as session:
        categories = await session.execute(select(Category))
        return categories.scalars().all()


async def get_category(category_id: int) -> Category:
    """Получаем Категорию по id."""

    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(Category).where(
            Category.id == category_id
        ))
        return db_obj.scalars().first()


async def get_subcats(category_id: int):
    """Получаем подкатегории по id Категории."""

    async with AsyncSessionLocal() as session:
        subcategories = await session.execute(select(SubCategory).where(
            SubCategory.category_id == category_id))
        return subcategories.scalars().all()


async def get_subcat(subcat_id: int) -> SubCategory:
    """Получаем ПодКатегорию по id."""

    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(SubCategory).where(
            SubCategory.id == subcat_id
        ))
        return db_obj.scalars().first()


async def get_items(subcat_id: int):
    """Получаем Товары по id ПодКатегории."""

    async with AsyncSessionLocal() as session:
        subcategories = await session.execute(select(Item).where(
            Item.sub_category_id == subcat_id))
        return subcategories.scalars().all()


async def get_certain_item(item_id: int) -> Item:
    """Получаем товар по id."""

    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(Item).where(
            Item.id == item_id
        ))
        return db_obj.scalars().first()


async def add_item_2_cart(item_id: int,
                          telegram_id: int,
                          amount: int = 1,
                          ) -> CartItem:
    """Добавляем Товар в корзину."""

    item = await get_certain_item(item_id=item_id)
    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(ShoppingCart).where(
                ShoppingCart.user_id == user.id).filter(
                    ShoppingCart.order_time == None)
                )
        cart = db_obj.scalars().first()
        if not cart:
            cart = ShoppingCart(user_id=user.id,
                                is_paid=False)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)
        db_obj = await session.execute(select(CartItem).where(
                CartItem.item_id == item.id).where(
                    CartItem.shopping_cart_id == cart.id
                ))
        cart_item = db_obj.scalars().first()
        if not cart_item:
            cart_item = CartItem(amount=amount,
                                 item_id=item.id,
                                 shopping_cart_id=cart.id)
        else:
            cart_item.amount += 1
        session.add(cart_item)
        await session.commit()
        await session.refresh(cart_item)
    return cart_item


async def delete_item_from_cart(telegram_id: int,
                                item_id: int):
    """Удаляем Товар из Корзины."""
    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(ShoppingCart).where(
                ShoppingCart.user_id == user.id).where(
                    ShoppingCart.order_time == None)
                )
        cart = db_obj.scalars().first()
        if cart:
            db_obj = await session.execute(select(CartItem).where(
                CartItem.item_id == item_id).where(
                    CartItem.shopping_cart_id == cart.id)
                    )
            item = db_obj.scalars().first()
            if item:
                await session.delete(item)
                await session.commit()
                return item


async def make_order(telegram_id: int,
                     address: str) -> ShoppingCart:
    """Добавляет в заказ адресс и дату оформления."""

    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(ShoppingCart).where(
                ShoppingCart.user_id == user.id).where(
                    ShoppingCart.order_time == None)
                )
        cart: ShoppingCart = db_obj.scalars().first()
        cart.address = address
        cart.order_time = datetime.now()
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
        return cart


async def get_overall(telegram_id: int) -> float:
    """Получаем сумму для оплаты."""
    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(ShoppingCart).where(
                ShoppingCart.user_id == user.id).where(
                    ShoppingCart.order_time != None).where(
                        ShoppingCart.is_paid == False
                    )
                )
        cart = db_obj.scalars().first()
        db_objs = await session.execute(select(CartItem).where(
                CartItem.shopping_cart_id == cart.id))
        cart_items = db_objs.scalars().all()
        items_ids = [cart_item.item_id for cart_item in cart_items]
        amounts = [cart_item.amount for cart_item in cart_items]
        db_objs = await session.execute(select(Item).where(
                Item.id.in_(items_ids)))
        items = db_objs.scalars().all()
        overall = 0 
        for i in range(len(items)):
            items[i].amount = amounts[i]
            overall += (items[i].price * items[i].amount)
        return overall


async def add_payment(telegram_id: int,
                      payment_id: str) -> None:
    """Добавляем в объект Корзины payment_id"""
    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(ShoppingCart).where(
                ShoppingCart.user_id == user.id).where(
                    ShoppingCart.order_time != None).where(
                        ShoppingCart.is_paid == False
                    )
                )
        cart = db_obj.scalars().first()
        cart.payment_id = payment_id
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
    return cart


async def get_shop_cart_items(telegram_id: int):
    user = await get_user(telegram_id=telegram_id)
    async with AsyncSessionLocal() as session:
        query = select(Item).join(
            CartItem, CartItem.item_id == Item.id).join(
                ShoppingCart, ShoppingCart.id == CartItem.shopping_cart_id).join(
                    User, User.id == ShoppingCart.user_id
                ).where(User.telegram_id == telegram_id).where(
                    ShoppingCart.order_time == None)
        result = await session.execute(query)
        items = result.scalars().all()
        query = select(CartItem).join(
            ShoppingCart, ShoppingCart.id == CartItem.shopping_cart_id).join(
                User, User.id == ShoppingCart.user_id).where(
                    User.telegram_id == telegram_id)
        result = await session.execute(query)
        cart_items = result.scalars().all()
        for item in items:
            for cart_item in cart_items:
                if item.id == cart_item.item_id:
                    item.amount = cart_item.amount
        return items
