from pathlib import Path
from typing import Union
from abc import ABC, abstractmethod

import pandas as pd


class BaseTransactionReader(ABC):

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

    @abstractmethod
    def _clean_up_transaction_df(trx_df: pd.DataFrame) -> pd.DataFrame:
        """Each class must use this method on its own to clean the
           loaded dataframe.

        Args:
            trx_df (pd.DataFrame): Input df with raw data.

        Returns:
            pd.DataFrame: Output df with clean data.
        """
        pass
