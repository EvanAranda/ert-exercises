import os
from datetime import datetime, timedelta
from time import sleep, time

from croniter import croniter

from rtsw.persist import connect_db_from_env
from rtsw.persist.query import sync_rtsw_hourly

# frequency of calls to the RTSW API
freq = os.getenv("RTSW_SYNC_FREQ", "* * * * *")
delay = float(os.getenv("RTSW_SYNC_DELAY", "5"))
once = os.getenv("RTSW_SYNC_ONCE", "false").lower() == "true"

assert croniter.is_valid(freq), f"invalid cron frequency: {freq}"

with connect_db_from_env() as conn:
    schedule = croniter(freq)
    while True:
        sleep_time = schedule.get_next(float) - time()
        sleep(sleep_time)
        sleep(delay)
        print(f"sync - {datetime.now()}")
        sync_rtsw_hourly(conn)
        conn.commit()

        if once:
            break
