import asyncio
import aiofiles
import time
import httpx
import ujson
from misc import load_config
from directory_handler import check_directory_structure

date = time.strftime("%Y%m%d")

async def get_snapshot(pair, data_warehouse_path, orderbook_depth):
    
    rest_url = f'https://api.binance.com/api/v3/depth'
    
    rest_params = {
        "symbol": pair.upper(),
        "limit": orderbook_depth,
    }
    
    timestamp = time.strftime("%Y%m%d%H%M%S")

    async with httpx.AsyncClient() as client:
        snapshot = await client.get(rest_url, params=rest_params)

    async with aiofiles.open(f'{data_warehouse_path}/{date}/{pair}/snapshots/{timestamp}.txt', mode='w') as f:
        await f.write(snapshot.text + '\n')


# RUN THIS IN WHILE LOOP EVERY n-TH SECONDS
async def get_snapshots_automatically(data_warehouse_path, symbols, orderbook_depth):
    
    tasks = []
    
    for pair in symbols:
        tasks.append(get_snapshot(pair, data_warehouse_path, orderbook_depth))
        
    await asyncio.gather(*tasks)
    
async def take_snapshot_loop(snapshot_interval):
    
    while True:
        await get_snapshots_automatically(data_warehouse_path, symbols, orderbook_depth)
        await asyncio.sleep(snapshot_interval)



async def get_snapshots_manually(data_warehouse_path, symbols, orderbook_depth):
    tasks = []

    for pair in symbols:
        tasks.append(get_snapshot(pair, data_warehouse_path, orderbook_depth))
        
    await asyncio.gather(*tasks)



if __name__ == '__main__':
        
        config = load_config()
        check_directory_structure(config['data_warehouse_path'], config['symbols'])
    
        data_warehouse_path = config['data_warehouse_path']
        symbols = config['symbols']
        orderbook_depth = config['orderbook_depth']
        snapshot_interval = config['snapshot_interval']
    
        asyncio.run(take_snapshot_loop(snapshot_interval))
