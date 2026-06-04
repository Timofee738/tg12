from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.users.states import RegState
from app.users.dao import UsersDao
from app.keyboards.users import back_builder

from app.config import settings

users_router = Router()

#=========================================================
@users_router.message(CommandStart())
async def str_cmd(message: Message, state: FSMContext):
    user = await UsersDao.find_one_or_none(tg_id=message.from_user.id)
    if user:
        await message.answer("Снова добро пожаловать. Как захочешь, запланируем урок.", reply_markup=back_builder.as_markup())
        return
    
    await message.answer("Добро пожаловать! Здесь ты можешь запланировать урок с репетитором.\n\nНапиши свое ФИО:")
    await state.set_state(RegState.username)
#=========================================================



#=========================================================
name_builder = InlineKeyboardBuilder()
name_builder.add(
    InlineKeyboardButton(text="Да", callback_data='usname:y'),
    InlineKeyboardButton(text='Нет', callback_data='usname:n')
)

@users_router.message(RegState.username)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(text=f"Тебя зовут: {message.text}?", reply_markup=name_builder.as_markup())
#=========================================================    


#=========================================================
class AdminReview(CallbackData, prefix="review"):
    action: str
    user_id: int
    


@users_router.callback_query(F.data.startswith('usname:'))
async def handle_usname(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    
    
    action = callback.data.split(':')[1]
    
    if action == 'y':
        
        await callback.message.edit_text(text='✅ Имя успешно подтверждено! ✅')
        
        
        user_data = await state.get_data()
        username_from_state = user_data.get('username')
        
        student_id = callback.from_user.id
        
        await UsersDao.add(
            tg_id=student_id,
            tg_usname=callback.from_user.username,
            username=username_from_state
        )      
        
        await state.clear()
        await callback.message.answer("Регистрация завершена!")
        
        admin_builder = InlineKeyboardBuilder()
        admin_builder.button(
            text="Отклонить",
            callback_data=AdminReview(action="reject", user_id=student_id)
        )
        
        admin_builder.button(
            text="Принять",
            callback_data=AdminReview(action="accept", user_id=student_id)
        )
        admin_builder.adjust(2)
        
        await bot.send_message(
            chat_id=settings.ADMIN,
            text=f"🔔 <b>Новая заявка!</b>\n\n"
                 f"👤 Имя: {username_from_state}\n"
                 f"🆔 ID: <code>{student_id}</code>",
            parse_mode="HTML",
            reply_markup=admin_builder.as_markup()
        )
        

        
        return
        

    await state.set_state(RegState.username)
    await callback.message.edit_text('Хорошо, напиши другое ФИО: ')
#=============================================================




    
    
    