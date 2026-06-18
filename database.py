import aiosqlite


DB_NAME = "database.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0,
            referrer INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS promocodes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            reward REAL,
            uses INTEGER,
            activated INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            amount REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            name TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS bonus(
            user_id INTEGER PRIMARY KEY,
            last_bonus INTEGER
        )
        """)

        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (user_id, username)
            VALUES (?, ?)
            """,
            (user_id, username)
        )
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        return await cursor.fetchone()


async def get_balance(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0


async def add_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id=?
            """,
            (amount, user_id)
        )
        await db.commit()


async def remove_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE user_id=?
            """,
            (amount, user_id)
        )
        await db.commit()


async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )
        row = await cursor.fetchone()
        return row[0]


async def add_channel(channel):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO channels(channel) VALUES(?)",
            (channel,)
        )
        await db.commit()


async def get_channels():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT channel FROM channels"
        )
        return await cursor.fetchall()


async def remove_channel(channel):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM channels WHERE channel=?",
            (channel,)
        )
        await db.commit()