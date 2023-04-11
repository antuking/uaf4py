from typing import Optional
from uaf.factories.driver.abstract_factory.abstract_products.abstract_web.abstract_msedge import (
    AbstractMsedge,
)
from selenium.webdriver.edge.options import Options as MsEdgeOptions
from . import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class ConcreteMsedgeDriver(AbstractMsedge):
    """Concrete implementation class of msedge web driver"""

    def get_web_driver(self, *, options: Optional[MsEdgeOptions] = None):
        """Concrete implementation method of fetching msedge web driver

        Args:
            capabilities (dict[str, Any]): _description_

        Returns:
            WebDriver: msedge webdriver instance
        """
        if options is None:
            options = MsEdgeOptions()

        return webdriver.Edge(
            options=options,
            service=Service(executable_path=EdgeChromiumDriverManager().install()),
        )