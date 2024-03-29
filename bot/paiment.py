from yookassa import Payment
from yookassa import Configuration
from constants import API_KEY, SHOP_ID, BOT_URL
import uuid

Configuration.account_id = SHOP_ID
Configuration.secret_key = API_KEY


def create_payment(value):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
          "value": value,
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "confirmation": {
          "type": "redirect",
          "return_url": BOT_URL
        },
        "description": "Заказ №72"
    }, idempotence_key)
  
    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url
    payment_id = payment.id
    return confirmation_url, payment_id


def get_payment(payment_id: str) -> Payment:
    payment = Payment.find_one(payment_id)
    return payment
