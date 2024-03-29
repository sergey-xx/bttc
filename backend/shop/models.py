from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_id = models.BigIntegerField(blank=True, null=True)
    password = models.CharField("password", max_length=128, null=True)
    email = models.EmailField("email address", blank=True, null=True)
    first_name = models.CharField("first name", max_length=150, blank=True, null=True)
    last_name = models.CharField("last name", max_length=150, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=100,
        blank=False,
        unique=True
    )
    slug = models.SlugField('Слаг категории', blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        'Название подкатегории',
        max_length=100,
        blank=False,
        unique=True
    )
    slug = models.SlugField('Слаг подкатегории', blank=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.name


class Item(models.Model):

    description = models.CharField(
        'Описание товара',
        max_length=1000,
        blank=False)
    photo = models.ImageField(blank=False)
    sub_category = models.ForeignKey(SubCategory,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='Подкатегория',
                                     related_name='items')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=False,
                                blank=False)

    def __str__(self) -> str:
        return self.description[:20]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             blank=False,
                             null=False,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Item,
                                   blank=False,
                                   through='CartItem',)
    order_time = models.DateTimeField(null=True,
                                      blank=True)
    address = models.CharField(null=True,
                               blank=True)
    is_paid = models.BooleanField(default=False)
    payment_id = models.UUIDField(blank=True,
                                  null=True)


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [models.UniqueConstraint(
            fields=['user', 'order_time'],
            name='unique_user_order_time'
        )]

    def __str__(self) -> str:
        return str(self.user) + '/' + super().__str__()


class CartItem(models.Model):
    item = models.ForeignKey(Item,
                             blank=False,
                             null=False,
                             on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(ShoppingCart,
                                      blank=False,
                                      null=False,
                                      on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина/Товар'
        verbose_name_plural = 'Корзины/Товары'
        constraints = [models.UniqueConstraint(
            fields=['item', 'shopping_cart'],
            name='unique_item_shopping_cart'
        )]
