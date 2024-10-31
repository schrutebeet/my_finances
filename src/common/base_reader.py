from pathlib import Path
from typing import Union
from abc import ABC, abstractmethod

import pandas as pd


class BaseReader(ABC):

    def __init__(self, input_path: Union[str, Path]) -> None:
        pass

    @staticmethod
    def _load_transaction_file(input_path: Union[str, Path]) -> pd.DataFrame:
        input_path = BaseTransactionReader.__convert_to_pathlib_path(input_path)
        if input_path.suffix == ".csv":
            input_df = pd.read_csv(input_path)
        else:
            raise ValueError("Please, provide a .csv file.")
        return trx_df
    
    @staticmethod
    def _convert_to_pathlib_path(input_path: str) -> Path:
        """Convert any string to a Path object.

        Args:
            input_path (str): string path to the file to be loaded.

        Returns:
            Path: A Path object with the path of the file to be loaded.
        """
        if not isinstance(input_path, Path):
            input_path = Path(input_path)
        return input_path
