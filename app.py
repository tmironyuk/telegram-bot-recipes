from utils.set_bot_commands import set_default_commands

from loader import db


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    try:
        db.create_table_users()
    except Exception as e:
        print(e)
    try:
        db.create_table_reviews()
    except Exception as e:
        print(e)
    try:
        db.create_table_statistics()
        db.set_table_statistics()
    except Exception as e:
        print(e)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
