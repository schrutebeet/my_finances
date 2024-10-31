from abc import ABC, abstractmethod


class BaseInvestmentReader(ABC):

    def __init__(self, input_path: Union[str, Path]) -> None: