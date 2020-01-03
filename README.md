# Frosch Bot
> Frosch Bot is a Dockerize discord bot written in [discord.py](https://github.com/Rapptz/discord.py).
> The bot is not designed to interact with users, instead it is just used
> to continually query the Clash of Clans API using [coc.py](https://github.com/mathsman5133/coc.py)
> and update the Dockerized postgres database. This eliviates some of the 
> resource burden off of the main Zulu Bot.


## Set up
```
  Zulu Bot                           Frosch Bot          
-------------                      -------------
|           |                      |           |
|           |                      |           |
|           |                      |           |
-------------                      -------------
      |                                  |
      |                                  |
      |                                  |
      |                                  |
      |               postgres           |
      |             -------------        |
      |             |           |        |
      |_____________|           |________|
                    |           |
                    -------------

```