from aiogram.fsm.state import State, StatesGroup


class AskAddress(StatesGroup):
    address = State()
    confirm = State()
    check_payment_status = State()