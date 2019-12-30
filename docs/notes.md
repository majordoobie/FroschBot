# Notes
This file is a collection of notes highlighting 
all the things that I have learned through this project

### Quick coc.py pull
```python
import coc
import asyncio

loop = asyncio.get_event_loop()
client = coc.login('email','pwd')
tag = '#9P9PRYQJ'

player = loop.run_until_complete(client.get_player(tag)) 
```

### Text replacement for db
```python
print(f"ACC_{i.lower().replace(' ','_').replace('!','').replace('-','').replace('.','').replace('&','and')} INTEGER DEFAULT 0,")
```

### Pushing .sql file to target docker
```python
docker exec -it <container-name> psql -U <DB_USER> -d <DB_NAME> -f /file.sql
```