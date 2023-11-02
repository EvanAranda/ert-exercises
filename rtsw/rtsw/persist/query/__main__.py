import os
import argparse
from datetime import datetime, timedelta
from time import sleep, time

from croniter import croniter

from rtsw.persist import connect_db_from_env
from rtsw.persist.query import sync_rtsw
from rtsw.shared import fetch_full_rtsw_json, fetch_hourly_rtsw_json


def sync_new_data():
    # frequency of calls to the RTSW API
    freq = os.getenv("RTSW_SYNC_FREQ", "* * * * *")
    delay = float(os.getenv("RTSW_SYNC_DELAY", "5"))
    once = os.getenv("RTSW_SYNC_ONCE", "false").lower() == "true"
    max_retry = int(os.getenv("RTSW_SYNC_MAX_RETRY", "3"))

    assert croniter.is_valid(freq), f"invalid cron frequency: {freq}"

    failed_count = 0

    print("Syncing new data...")

    with connect_db_from_env() as conn:
        schedule = croniter(freq)
        while True:
            try:
                sleep_time = schedule.get_next(float) - time()
                sleep(sleep_time)
                sleep(delay)
                print(f"sync - {datetime.now()}")
                sync_rtsw(conn, fetch_hourly_rtsw_json())
                conn.commit()

                if once:
                    break

                failed_count = 0
            except Exception as e:
                failed_count += 1
                if failed_count > max_retry:
                    raise e

                print("sync failed, retrying (attempt {failed_count})")


def sync_full_data():
    print("Syncing full data...")

    with connect_db_from_env() as conn:
        sync_rtsw(conn, fetch_full_rtsw_json())
        conn.commit()


parser = argparse.ArgumentParser()
parser.add_argument(
    "--full",
    action="store_true",
    default=False,
    help="Sync full data once instead of new data.",
)
args = parser.parse_args()

if args.full:
    sync_full_data()
else:
    sync_new_data()
