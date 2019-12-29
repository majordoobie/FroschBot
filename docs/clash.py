import coc
import asyncio
loop = asyncio.get_event_loop()
client = coc.login('sgtmajorjay@gmail.com', 'xUjpuw-jyrxe5-mydjum')
print(dir(client))
player = loop.run_until_complete(client.get_player('#QULC2GV9'))
season_list = loop.run_until_complete(client.get_seasons(player.league.id))
#player2 = loop.run_until_complete(client.get_player('#9P9PRYQJ'))    

print(season_list[-1]['id'])
print(player.league.id)
# List of locations
await client.search_locations()
# List of leagues
await client.search_leagues() 

# Clash of stats
# https://www.clashofstats.com/players/jaguar__-Y9J80QRC/achievements

# List of leagues
# await client.get_location_players() 
# await client.get_location_clan() 
# load = await client.get_season_rankings('29000022', '2019-11')
# legend = loop.run_until_complete(load)
# print(legend)
#legend = loop.run_until_complete(client.get_season_rankings(player.league.id, '2019-11'))
#print(legend)
##9P9PRYQJ sgtmajordoobie-9P9PRYQJ
client.close()