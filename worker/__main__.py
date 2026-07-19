import logging
import time

from worker.fetch_once import poll_once

POLL_INTERVAL_SECONDS = 20

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("worker")

while True:
    try:
        poll_once()
        log.info("poll stored")
    except Exception:
        log.exception("poll failed, will retry next cycle")
    time.sleep(POLL_INTERVAL_SECONDS)

