from misc import load_config
from directory_handler import check_directory_structure
from websocket_handler import orderbook_download
import asyncio



config = load_config()
    
check_directory_structure(config['data_warehouse_path'], config['symbols'])

for pair in config['symbols']:
    asyncio.run(orderbook_download(pair, config['data_warehouse_path']))


# for pair in config['symbols']:
#     orderbook_download(pair, config['data_warehouse_path'])