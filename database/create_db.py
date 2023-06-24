import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


async def create_bot_database():
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    await sql.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        id BIGINT PRIMARY KEY,
        cash INT,
        pay_id TEXT,
        promocode TEXT
    )""")
    await sql.execute(
        """CREATE TABLE IF NOT EXISTS links (
        linkYoutube TEXT UNIQUE,
        linkID serial PRIMARY KEY,
        linkSender BIGINT
    )""")
    await sql.execute(
        """CREATE TABLE IF NOT EXISTS queue (
        queueID INT
    )""")
    await sql.execute(
        """CREATE TABLE IF NOT EXISTS zaliv (
        linkSender TEXT UNIQUE,
        zalivSender INTEGER
    )""")
    await sql.execute(
        """CREATE TABLE IF NOT EXISTS promocodes(
        promocode TEXT UNIQUE,
        amount INT,
        useCount INT
    )""")
    await sql.execute(
        """CREATE TABLE IF NOT EXISTS stats(
        all_requests INT,
        success_requests INT,
        cancel_requests INT,
        amount_earned INT
        )""")
    find_rows_qount = await sql.fetch("SELECT COUNT(*) FROM queue")
    find_rows_stats = await sql.fetch("SELECT COUNT(*) FROM stats")
    if find_rows_qount[0][0] == 0:
        await sql.execute("INSERT INTO queue(queueid) VALUES ('0')")
    if find_rows_stats[0][0] == 0:
        await sql.execute(
            "INSERT INTO stats(all_requests, success_requests, cancel_requests, amount_earned) VALUES (0, 0, 0, 0)")
    await sql.close()
