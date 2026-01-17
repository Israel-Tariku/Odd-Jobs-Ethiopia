# handlers/post_job.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config

router = Router()

# 👋 Greeting when user starts the bot
@router.message(Command("start"))
async def start_command(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="📋 Post a Job", callback_data="start_postjob")
    await message.answer(
        "👋 Welcome to Odd Jobs Ethiopia!\n\n"
        "Here you can post jobs and find helpers.\n"
        "Click below to get started:",
        reply_markup=kb.as_markup()
    )

# Handle the "Post a Job" button
@router.callback_query(lambda c: c.data == "start_postjob")
async def start_postjob_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📋 Enter the job title:")
    await state.set_state(JobForm.title)
    await callback.answer()

class JobForm(StatesGroup):
    title = State()
    description = State()
    pay = State()
    deadline = State()

@router.message(JobForm.title)
async def job_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("✍️ Enter the job description:")
    await state.set_state(JobForm.description)

@router.message(JobForm.description)
async def job_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("💰 Enter the pay:")
    await state.set_state(JobForm.pay)

@router.message(JobForm.pay)
async def job_pay(message: types.Message, state: FSMContext):
    await state.update_data(pay=message.text)
    await message.answer("📅 Enter the deadline:")
    await state.set_state(JobForm.deadline)

@router.message(JobForm.deadline)
async def job_deadline(message: types.Message, state: FSMContext, bot):
    await state.update_data(deadline=message.text)
    data = await state.get_data()

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Approve", callback_data=f"approve:{message.from_user.id}")
    kb.button(text="❌ Reject", callback_data=f"reject:{message.from_user.id}")

    await bot.send_message(
        chat_id=config.ADMIN_GROUP_ID,
        text=(
            f"🆕 Job Request from {message.from_user.full_name}\n\n"
            f"📌 Title: {data['title']}\n"
            f"📝 Description: {data['description']}\n"
            f"💰 Pay: {data['pay']}\n"
            f"📅 Deadline: {data['deadline']}"
        ),
        reply_markup=kb.as_markup()
    )

    await message.answer("✅ Your job request has been sent to admins for approval.")
    await state.clear()
