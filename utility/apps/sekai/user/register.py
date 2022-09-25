from sqlite3 import dbapi2
from utility.utils import errEmbed

async def check_user_account(self, discord_id: int):
    global db
    db = self.bot.db
    cursor = await db.cursor()
    await cursor.execute('SELECT discord_id FROM user_accounts WHERE discord_id = ?', (discord_id,))
    result = await cursor.fetchone()
    if result is None:
        return False
    else:
        return True
    
    ''' embed = errEmbed(
            '找不到帳號！',
            f'<@{discord_id}>\n請使用  `/register`  創建一個帳號後再重新執行操作')'''