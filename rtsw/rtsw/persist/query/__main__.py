import os
from datetime import datetime, timedelta
from time import sleep

from rtsw.persist import connect_db_from_env
from rtsw.persist.query import sync_rtsw_hourly
from rtsw.shared import ticker, parse_time

# frequency of calls to the RTSW API
freq_str = os.getenv("RTSW_SYNC_FREQ", "01:05")
freq = parse_time(freq_str)

once = os.getenv("RTSW_SYNC_ONCE", "false").lower() == "true"

with connect_db_from_env() as conn:
    for i in ticker(freq):
        print(f"sync {i} - {datetime.now()}")
        sync_rtsw_hourly(conn)
        conn.commit()

        if once:
            break
