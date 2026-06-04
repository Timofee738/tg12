from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.users.handler import AdminReview

from app.config import settings

from app.users.dao import UsersDao

from app.admin.calendar import get_calendar






admins_router = Router()



@admins_router.message(Command('admin'))
async def admin_cmd(message: Message):
    user = await UsersDao.find_one_or_none(tg_id=message.from_user.id)
    
    
    if user.is_tutor:
        await message.answer("Добро пожаловать в панель админа")
        
        
@admins_router.callback_query(AdminReview.filter())
async def capture_call(callback: CallbackQuery, callback_data: AdminReview, bot: Bot):
    callback.answer()
    if callback.from_user.id != settings.ADMIN:
        await callback.message.answer("У вас недостаточно прав для этого действия")
    
    student_id = callback_data.user_id
    action = callback_data.action
    
    if action == 'accept':
        await UsersDao.edit_acception(tg_id=student_id, new_status=True)
        await callback.message.edit_text(f"Пользователь: {student_id} принят")
        
        calendar_kb = get_calendar()
        
        try:
            await bot.send_message(
                chat_id=student_id,
                text="🎉 <b>Репетитор подтвердил вашу заявку!</b>\n\n"
                     "Теперь вам доступна запись на занятия. "
                     "Пожалуйста, выберите подходящий день недели ниже 👇:",
                parse_mode="HTML",
                reply_markup=calendar_kb
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение ученику {student_id}: {e}")
        
        return
    
    
    if action == "reject":
        await callback.message.edit_text(f"Пользователь: {student_id} отклонен")
        try:
            await bot.send_message(chat_id=student_id, text="❌ К сожалению, ваша заявка была отклонена.")
        except Exception:
            pass
    
    