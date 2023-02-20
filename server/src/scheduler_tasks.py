import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from max_size_dict import MaxSizeLRU
from constants import *

IN_MEMORY_HISTORICAL_USAGE = MaxSizeLRU(30)


def get_system_stats():
    # total: total physical memory available.
    # available: the memory that can be given instantly to processes without the system going into swap. This is calculated by summing different memory values depending on the platform and it is supposed to be used to monitor actual memory usage in a cross platform fashion.
    # percent: the percentage usage calculated as (total - available) / total * 100
    # used: memory used, calculated differently depending on the platform and designed for informational purposes only: macOS: active + wired BSD: active + wired + cached Linux: total - free
    # free: memory not being used at all (zeroed) that is readily available; note that this doesn't reflect the actual memory available (use 'available' instead)
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent()
    # Getting virtual_memory in GB
    item = {
        "total": memory.total/BYTES_PER_GB,  # GB
        "available": memory.available/BYTES_PER_GB,  # GB
        "usage_percent": memory.percent,  # %
        "used": memory.used/BYTES_PER_GB,  # GB
        "free": memory.free/BYTES_PER_GB,  # GB
        "cpu_percent": cpu_percent  # GB
    }
    IN_MEMORY_HISTORICAL_USAGE.store(item
                                     )
    print('STORED: ', item)


scheduler = BackgroundScheduler()
# Automatically store last 30 minbutes
scheduler.add_job(func=get_system_stats, trigger="interval", seconds=5)
scheduler.start()
