from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, String,
                        BigInteger, Numeric)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'shop_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100))
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    date_joined = Column(TIMESTAMP)


class Category(Base):
    """Модель категории."""

    __tablename__ = 'shop_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    slug = Column(String(100))


class SubCategory(Base):
    """Модель подкатегории"""

    __tablename__ = 'shop_subcategory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    slug = Column(String(100))
    category_id = Column(Integer)


class Item(Base):
    """Модель Товаров"""

    __tablename__ = 'shop_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1000))
    photo = Column(String())
    sub_category_id = Column(Integer)
    price = Column(Numeric)


class ShoppingCart(Base):
    __tablename__ = 'shop_shoppingcart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    order_time = Column(TIMESTAMP)
    address = Column(String)
    is_paid = Column(Boolean, default=False)
    payment_id = Column(UUID, nullable=True)


class CartItem(Base):
    __tablename__ = 'shop_cartitem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    item_id = Column(Integer)
    shopping_cart_id = Column(Integer)
