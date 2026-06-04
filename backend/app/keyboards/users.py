from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

back_builder = InlineKeyboardBuilder()
back_builder.button(
    text="🔙 Меню выбора",
    callback_data="back_to_days"
)


class ChangeMethodCallback(CallbackData, prefix="change_method"):
    method: bool

change_builder = InlineKeyboardBuilder()
change_builder.button(
    text="Записаться",
    callback_data=ChangeMethodCallback(method=True)
)
change_builder.button(
    text="Отменить",
    callback_data=ChangeMethodCallback(method=False)
)