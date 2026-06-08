from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.classes.dao import ClassesDao
from app.users.dao import UsersDao
from app.admin.calendar import CalendarDayCallback, CalendarTimeCallback, get_day_time, get_calendar
from app.keyboards.users import back_builder, AdminCancelCallback

from datetime import datetime
from app.config import settings

classes_router = Router()

@classes_router.callback_query(CalendarDayCallback.filter())
async def capture_day(callback: CallbackQuery, callback_data: CalendarDayCallback):
    await callback.answer()
    
    target_date = datetime.strptime(callback_data.date_str, "%Y-%m-%d").date()
    busy_slots = await ClassesDao.get_busy_slots_for_day(target_date=target_date)
    user_id = callback.from_user.id
    day_kb = get_day_time(callback_data.date_str, busy_slots=busy_slots, current_user_id=user_id)
    
    await callback.message.edit_text(
        text=f"Выберите время на: {target_date}",
        reply_markup=day_kb
    )
  
  


@classes_router.callback_query(F.data == 'back_to_days')
async def back_to_days(callback: CallbackQuery):
    await callback.answer()
    
    kb = get_calendar()
    
    await callback.message.edit_text(
        text="Пожалуйста, выберите подходящий день недели ниже 👇:",
        parse_mode="HTML",
        reply_markup=kb
    )




  
@classes_router.callback_query(CalendarTimeCallback.filter())
async def capture_time(callback: CallbackQuery, callback_data: CalendarTimeCallback, bot: Bot):
    await callback.answer()
    
    full_datetime = f"{callback_data.date_str} {callback_data.time_str}"
    timestamp = datetime.strptime(full_datetime, "%Y-%m-%d %H-%M")
    
    
    is_busy = await ClassesDao.check_slot_busy(timestamp=timestamp)
    
    if is_busy:
        await callback.answer(
            text="⚠️ К сожалению это время только что забронировал другой ученик ⚠️",
            show_alert=True
        )
        target_date = timestamp.date()
        busy_slots = await ClassesDao.get_busy_slots_for_day(target_date)
        
        
        updated_kb = get_day_time(
            chosen_date=callback_data.date_str, 
            busy_slots=busy_slots, 
            current_user_id=callback.from_user.id
        )
        
        
        await callback.message.edit_text(
            text=f"Вы опоздали! Кто-то занял это время.\nВыберите другое время на: {target_date}",
            reply_markup=updated_kb
        )
        return
    
    await ClassesDao.add(
        lesson_timestamp=timestamp,
        reserved=True,
        user_id=callback.from_user.id
    )
    await callback.message.edit_text(
        text=f"✅ Урок запланирован\n\nДень: {callback_data.date_str}\nВремя: {callback_data.time_str}",
        reply_markup=back_builder.as_markup()
    )
    
    student = await UsersDao.find_one_or_none(tg_id=callback.from_user.id)
    
    
    cancel_builder = InlineKeyboardBuilder()
    cancel_builder.button(
        text="➖ Отменить",
        callback_data=AdminCancelCallback(timestamp=timestamp, user_id=callback.from_user.id)
    )
    
    
    await bot.send_message(
        chat_id=settings.ADMIN,
        text=f"Новое запланированое событие:\n\n⏰ Время: {timestamp}\n👤 Ученик: {student.username}",
        reply_markup=cancel_builder.as_markup()
    )
@classes_router.callback_query(AdminCancelCallback.filter())
async def cancel_class(callback: CallbackQuery, callback_data: AdminCancelCallback, bot: Bot):
    await callback.answer()
    await ClassesDao.delete(lesson_timestamp=callback_data.timestamp, user_id=callback_data.user_id)
    await callback.message.edit_text(
        text=f"Успешно отменено событие:\n\nВремя: {callback_data.timestamp}\nУченик:{callback_data.username}"
    )
    await bot.send_message(
        chat_id=callback_data.user_id,
        text=f"К сожалению отменено событие:\n\nВремя: {callback_data.timestamp}"
    )
