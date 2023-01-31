async def check_user_account(discord_id: str, db, server: str):
    cursor = await db.cursor()
    await cursor.execute(f'SELECT player_id_{server} from user_accounts WHERE discord_id = ?', (str(discord_id),))
    result = await cursor.fetchone()
    await db.commit()
    if result is None:
        return False
    else:
        return True
