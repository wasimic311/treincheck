import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.config import settings
from core.models import RawResponse

NS_DISRUPTIONS_URL = "https://gateway.apiportal.ns.nl/disruptions/v3"


engine = create_engine(settings.database_url)


def poll_once() -> None:
      resp = httpx.get(
          NS_DISRUPTIONS_URL,
          headers={"Ocp-Apim-Subscription-Key": settings.ns_api_key},
          timeout=10.0,
      )
      try:
          payload = resp.json()
      except ValueError:
          payload = None

      with Session(engine) as session:
          session.add(RawResponse(status_code=resp.status_code, payload=payload))
          session.commit()