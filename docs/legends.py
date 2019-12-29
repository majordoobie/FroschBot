@discord_client.command(alias=['l'])
async def legend(ctx, *, user=None):
    if user == None:
        query_result = dbconn.get_user_byDiscID((ctx.author.id,))

    else:
        discord_member = await botAPI.user_converter_db(ctx, user)
        query_result = dbconn.get_user_byDiscID((discord_member.id,))

    async with ctx.typing():
        player_tag = query_result[0][0]
        player = await coc_client2.get_player(player_tag)
        if player.league.id != 29000022:
            await ctx.send("Must be in legends to use me")
            return
        seasons_list = await coc_client2.get_seasons(player.league.id)
        prev, prev2, prev3, prev4 = (seasons_list[-1]['id'], seasons_list[-2]['id'], seasons_list[-3]['id'], seasons_list[-4]['id'] )
        
        legend_stats = []

        for season in (prev4, prev3, prev2, prev):
            legends_list = await coc_client2.get_season_rankings(player.league.id, season)
            for legend in legends_list:
                if legend.tag == player.tag:
                    legend_stats.append({
                        "season" : season,
                        "player_name" : legend.name,
                        "attack_wins" : legend.attack_wins,
                        "defense_wins" : legend.defense_wins,
                        "player_rank" : legend.rank,
                        "player_trophy" : legend.trophies,
                        })

    for season in legend_stats:
        data = f"⠀__**Season {season['season']}**__\n"
        data += f"`⠀{'Ranking':<12.12}⠀` `⠀{season['player_rank']:⠀>8}⠀`\n"
        data += f"`⠀{'Trophy':<12.12}⠀` `⠀{season['player_trophy']:⠀>8}⠀`\n"
        data += f"`⠀{'Attack Wins':<12.12}⠀` `⠀{season['attack_wins']:⠀>8}⠀`\n"
        data += f"`⠀{'Defense Wins':<12.12}⠀` `⠀{season['defense_wins']:⠀>8}⠀`\n"
        await ctx.send(data)