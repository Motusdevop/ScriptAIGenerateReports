from loguru import logger
import pycurl
from io import BytesIO
from urllib.parse import urlencode
from typing import Optional


class HTTPClient:
    """Простой HTTP клиент для pycurl"""

    def request(
        self,
        url: str,
        post_data: Optional[dict] = None,
        cookiejar: Optional[str] = None,
    ) -> str:
        logger.debug(f"HTTP request → {url}")

        buffer = BytesIO()
        curl = pycurl.Curl()

        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, buffer)
        curl.setopt(curl.SSL_VERIFYPEER, 0)
        curl.setopt(curl.SSLVERSION, pycurl.SSLVERSION_TLSv1)
        curl.setopt(curl.FOLLOWLOCATION, 1)
        curl.setopt(curl.COOKIEFILE, cookiejar or "")
        curl.setopt(curl.COOKIEJAR, cookiejar or "")
        curl.setopt(
            curl.HTTPHEADER,
            [
                "User-Agent: Mozilla/5.0",
                "Referer: https://fanfan.softium-deti.ru:820/admin/default.htm",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            ],
        )

        if post_data:
            logger.debug(f"POST data: {post_data}")
            curl.setopt(curl.POST, 1)
            curl.setopt(curl.POSTFIELDS, urlencode(post_data))

        curl.perform()
        curl.close()

        html = buffer.getvalue().decode("windows-1251", errors="replace")
        logger.debug(f"HTTP response length: {len(html)} chars")

        return html
