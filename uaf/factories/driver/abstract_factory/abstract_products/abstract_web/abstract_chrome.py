from abc import ABC, abstractmethod
from typing import Optional, Any
from selenium.webdriver.chrome.options import Options as ChromeOptions


class AbstractChrome(ABC):
    """Distinct chrome web base interface"""

    @abstractmethod
    def get_web_driver(self, *, options: Optional[ChromeOptions] = None):
        """Abstract skeleton method for fetching chrome driver

        Args:
            caps (Optional[dict[str, Any]], optional): _description_. Defaults to None.
        """