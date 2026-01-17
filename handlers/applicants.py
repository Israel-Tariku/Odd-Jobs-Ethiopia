# handlers/applicants.py
from aiogram import Router, types
from services import db
from keyboards import job_keyboards

router = Router()

@router.callback_query(lambda c: c.data.startswith("apply"))
async def apply_job(callback: types.CallbackQuery, bot):
    job_id = int(callback.data.split(":")[1])
    applicant = callback.from_user

    db.save_applicant(job_id, applicant.id)

    # Find poster ID from job
    from models.job import Job
    session = db.SessionLocal()
    job = session.query(Job).filter(Job.id == job_id).first()
    poster_id = job.poster_id
    session.close()

    await bot.send_message(
        chat_id=poster_id,
        text=(
            f"📩 New applicant for your job '{job.title}'!\n\n"
            f"👤 {applicant.full_name} (@{applicant.username or 'no username'})"
        ),
        reply_markup=job_keyboards.applicant_decision(job_id, applicant.id)
    )
    await callback.answer("Application sent ✅")

@router.callback_query(lambda c: c.data.startswith("accept"))
async def accept_applicant(callback: types.CallbackQuery, bot):
    _, job_id, applicant_id = callback.data.split(":")
    applicant_id = int(applicant_id)

    await bot.send_message(applicant_id, "🎉 Your application was accepted! The job poster will contact you soon.")
    await bot.send_message(callback.from_user.id, f"✅ You accepted applicant {applicant_id}. You can now chat directly.")
    await callback.answer("Applicant accepted ✅")

@router.callback_query(lambda c: c.data.startswith("reject_app"))
async def reject_applicant(callback: types.CallbackQuery, bot):
    _, job_id, applicant_id = callback.data.split(":")
    applicant_id = int(applicant_id)

    await bot.send_message(applicant_id, "❌ Sorry, your application was rejected.")
    await bot.send_message(callback.from_user.id, "You rejected this applicant.")
    await callback.answer("Applicant rejected ❌")
