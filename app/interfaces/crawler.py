from abc import ABC, abstractmethod


class Crawler(ABC):
    """Abstract base class for crawlers."""

    @abstractmethod
    def run(self):
        pass
