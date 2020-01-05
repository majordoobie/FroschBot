async def get_discord_user(pool, obj):
    async with pool.acquire() as con:
        member_record = con.fetchrow('''
            SELECT * 
            FROM discord_user 
            WHERE discord_id  = $1
            OR LOWER(discord_name) = $1
            OR LOWER(discord_nickname) = $1
            OR LOWER(discord_discriminator) = $1''', obj.lower())
        if member_record:
            return member_record
        member_id = con.fetchrow('''
            SELECT discord_id
            FROM clash_account
            WHERE LOWER(clash_tag) = $1''', obj.lower())
        if member_id:
            return con.fetchrow('''
            SELECT * 
            FROM discord_user
            WHERE discord_id = $1''', member_id)

