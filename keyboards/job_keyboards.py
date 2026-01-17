# keyboards/job_keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def apply_button(job_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📩 Apply", callback_data=f"apply:{job_id}")]]
    )

def applicant_decision(job_id: int, applicant_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Accept", callback_data=f"accept:{job_id}:{applicant_id}"),
                InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_app:{job_id}:{applicant_id}")
            ]
        ]
    )
