# handlers/admin.py
from aiogram import Router, types
import config

router = Router()

@router.callback_query(lambda c: c.data.startswith("approve"))
async def approve_job(callback: types.CallbackQuery, bot):
    user_id = int(callback.data.split(":")[1])
    await bot.send_message(user_id, "🎉 Your job has been approved and posted!")

    # Post to channel with Apply button
    apply_button = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="📩 Apply", callback_data=f"apply:{user_id}")]]
    )

    await bot.send_message(
        chat_id=config.CHANNEL_ID,
        text=callback.message.text,
        reply_markup=apply_button
    )
    await callback.answer("Job approved ✅")

@router.callback_query(lambda c: c.data.startswith("reject"))
async def reject_job(callback: types.CallbackQuery, bot):
    user_id = int(callback.data.split(":")[1])
    await bot.send_message(user_id, "❌ Sorry, your job request was rejected by admins.")
    await callback.answer("Job rejected ❌")

# Handle Apply button
@router.callback_query(lambda c: c.data.startswith("apply"))
async def apply_job(callback: types.CallbackQuery, bot):
    poster_id = int(callback.data.split(":")[1])
    applicant = callback.from_user

    # Notify poster
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="✅ Accept", callback_data=f"accept:{poster_id}:{applicant.id}"
                ),
                types.InlineKeyboardButton(
                    text="❌ Reject", callback_data=f"reject_app:{poster_id}:{applicant.id}"
                ),
            ]
        ]
    )

    await bot.send_message(
        chat_id=poster_id,
        text=(
            f"📩 New applicant for your job!\n\n"
            f"👤 {applicant.full_name} (@{applicant.username or 'no username'})"
        ),
        reply_markup=kb
    )

    await callback.answer("Application sent ✅")

# Handle Accept
@router.callback_query(lambda c: c.data.startswith("accept"))
async def accept_applicant(callback: types.CallbackQuery, bot):
    _, poster_id, applicant_id = callback.data.split(":")
    applicant_id = int(applicant_id)

    # Notify applicant
    await bot.send_message(
        chat_id=applicant_id,
        text="🎉 Your application was accepted! The job poster will contact you soon."
    )

    # Forward applicant contact to poster
    await bot.send_message(
        chat_id=int(poster_id),
        text=f"✅ You accepted {callback.from_user.full_name}. You can now chat directly."
    )

    await callback.answer("Applicant accepted ✅")

# Handle Reject
@router.callback_query(lambda c: c.data.startswith("reject_app"))
async def reject_applicant(callback: types.CallbackQuery, bot):
    _, poster_id, applicant_id = callback.data.split(":")
    applicant_id = int(applicant_id)

    # Notify applicant
    await bot.send_message(
        chat_id=applicant_id,
        text="❌ Sorry, your application was rejected."
    )

    await bot.send_message(
        chat_id=int(poster_id),
        text="You rejected this applicant."
    )

    await callback.answer("Applicant rejected ❌")
