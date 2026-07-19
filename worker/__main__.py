import logging
import time

from core.config import settings
from worker.fetch_once import poll_once

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("worker")


def main() -> None:
    log.info("worker started, polling every %s seconds", settings.poll_interval_seconds)
    while True:
        try:
            poll_once()
            log.info("poll stored")
        except Exception:
            log.exception("poll failed, will retry next cycle")
        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    main()

