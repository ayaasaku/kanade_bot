import aiosqlite
from utility.utils import errEmbed

        
async def check_user_account(discord_id: int, db):
    cursor = await db.cursor()
    await cursor.execute('SELECT discord_id FROM user_acc WHERE discord_id = ?', (discord_id,))
    result = await cursor.fetchone()
    await db.commit()
    if result is None:
        return False
    else:
        return True
    