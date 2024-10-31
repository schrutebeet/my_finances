from pathlib import Path
from typing import Union
from abc import ABC, abstractmethod

import pandas as pd

from src.common.base_reader import BaseReader


class BaseTransactionReader(BaseReader):

    def __init__(self, input_path: Union[str, Path]) -> None:
        super().__init__(input_path)

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

    @abstractmethod
    def get_clean_trx_df():
        """Get the clean transaction df for a specific money holder.
        """
        pass
