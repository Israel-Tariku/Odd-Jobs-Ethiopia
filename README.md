# Odd-Jobs-Ethiopia
want jobs? we got'em

odd_jobs_ethiopia_bot/
│
├── bot.py                # Main entry point (starts the bot)
├── config.py             # Configurations (API token, channel/group IDs)
├── requirements.txt      # Python dependencies
├── README.md             # Documentation for your project
│
├── data/                 # Database & migrations
│   └── jobs.db           # SQLite database (or migrations if using Postgres)
│
├── handlers/             # Bot command & callback handlers
│   ├── __init__.py
│   ├── start.py          # /start command
│   ├── post_job.py       # Job submission logic
│   ├── admin.py          # Admin approval/rejection
│   ├── applicants.py     # Applicant apply/accept/reject flow
│
├── models/               # Database models
│   ├── __init__.py
│   ├── job.py            # Job model
│   ├── applicant.py      # Applicant model
│   └── user.py           # User model (poster/applicant/admin)
│
├── services/             # Utility services
│   ├── __init__.py
│   ├── db.py             # Database connection helpers
│   ├── notifications.py  # Sending messages/alerts
│   └── utils.py          # Helper functions
│
├── keyboards/            # Inline keyboards
│   ├── __init__.py
│   ├── job_keyboards.py  # Apply button, accept/reject buttons
│   └── admin_keyboards.py# Approve/reject buttons
│
└── logs/                 # Logs for debugging
    └── bot.log
