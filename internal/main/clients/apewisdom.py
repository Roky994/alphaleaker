import enum
import logging

import requests

logger = logging.getLogger(__name__)


class ApeWisdomClientError(Exception):
    pass


class ApeWisdomFilter(enum.Enum):
    ALL = "all"
    CRYPTO = "all-crypto"


class ApeWisdomClient:
    API_URL = "https://apewisdom.io/api/v1.0/filter/{filter}/page/{page}"
    OK_STATUS_CODES = [200]

    def _request(self, filter: ApeWisdomFilter, page: int = 1) -> str:
        response = requests.get(
            self.API_URL.format(filter=filter.value, page=str(page)),
        )
        if response.status_code not in self.OK_STATUS_CODES:
            logger.error("API call failed: {}.".format(response.content))
            raise ApeWisdomClientError(
                "API call failed with code {}".format(response.status_code)
            )

        return response.json()

    def get_tredning_cryptocurrencies(self) -> str:
        return self._request(
            filter=ApeWisdomFilter.CRYPTO,
        )
