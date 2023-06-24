from aiogram import types
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


async def infoqueue(message: types.Message):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    find_queue_reserved = await sql.fetch("SELECT queueID from queue")
    await message.answer(f"<b> В данный момент в очереди {find_queue_reserved[0][0]} человек(а) "
                         f"\nОсталось мест: {5 - int(find_queue_reserved[0][0])} шт. "
                         f"\nИнформация: t.me/godseoinfo</b>",
                         parse_mode="html")
    await sql.close()
