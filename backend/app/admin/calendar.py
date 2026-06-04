from datetime import datetime, timedelta
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class CalendarDayCallback(CallbackData, prefix='calendar_day'):
    date_str: str
    
class CalendarTimeCallback(CallbackData, prefix='calenar_time'):
    date_str: str
    time_str: str
    
WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def get_calendar():
    builder = InlineKeyboardBuilder()
    start_date = datetime.now().date()
    
    for i in range(1, 6):
        current_date = start_date + timedelta(days=i)
        weekday = WEEKDAYS[current_date.weekday()]
        formatted_date = current_date.strftime("%d.%m")
        
        button_text = f"{weekday} ({formatted_date})"
        builder.button(
            text=button_text,
            callback_data=CalendarDayCallback(date_str=current_date.isoformat())
        )
        
    builder.adjust(1)
    return builder.as_markup()

def get_day_time(chosen_date: str, busy_slots: list[str], current_user_id: int):
    builder = InlineKeyboardBuilder()
    
    WORKINGHOURS = ['10-00', '11-30', '13-00', '15-00', '16-30', '18-00']
    busy_times = {slot["time"]: slot["user_id"] for slot in busy_slots}
    
    for slot in WORKINGHOURS:
        check_slot = slot.replace("-", ":")
        if check_slot in busy_times:
            slot_owner = busy_times[check_slot]
            if slot_owner == current_user_id:
                builder.button(
                    text=f"👤 Ваша запись ({slot})", 
                    callback_data="ignore_my_own_slot" # Пустышка или можно сделать кнопку "Отменить запись"
                )
            else:
                builder.button(
                    text=f"❌ {slot}", 
                    callback_data="ignore_busy_slot"
                )
            
        else: 
            builder.button(
                text=f"⏰ {slot}",
                callback_data=CalendarTimeCallback(
                    date_str=chosen_date, 
                    time_str=slot
                )
            )
            
    builder.button(
        text="⬅️ Назад к дням", 
        callback_data="back_to_days"
    )
    
    builder.adjust(2)
    
    
    return builder.as_markup()
    
        