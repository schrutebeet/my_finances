from typing import Union
from pathlib import Path
from abc import ABC, abstractmethod

from src.common.base_reader import BaseReader


class BinanceReader(BaseReader):

    def __init__(self, input_path: Union[str, Path]) -> None:
        super().__init__(input_path)
        self.input_path = input_path
    
    def get_df(self):
        trx_df = self._load_file(self.input_path)
        return trx_df
