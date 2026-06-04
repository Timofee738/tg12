from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.classes.dao import ClassesDao
from app.admin.calendar import CalendarDayCallback, CalendarTimeCallback, get_day_time, get_calendar
from app.keyboards.users import back_builder

from datetime import datetime

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
async def capture_time(callback: CallbackQuery, callback_data: CalendarTimeCallback):
    await callback.answer()
    
    full_datetime = f"{callback_data.date_str} {callback_data.time_str}"
    timestamp = datetime.strptime(full_datetime, "%Y-%m-%d %H-%M")
    await ClassesDao.add(
        lesson_timestamp=timestamp,
        reserved=True,
        user_id=callback.from_user.id
    )
    await callback.message.edit_text(
        text=f"✅ Урок запланирован\n\nДень: {callback_data.date_str}\nВремя: {callback_data.time_str}",
        reply_markup=back_builder.as_markup()
    )
