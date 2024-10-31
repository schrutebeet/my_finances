import re
import yaml
from pathlib import Path
from typing import Union

import pandas as pd

from src.banking.base_transactions_reader import BaseTransactionReader


class SabadellTrasactionReader(BaseTransactionReader):

    def __init__(self, input_path: Union[str, Path], cat_path: Union[str, Path]) -> None:
        super().__init__(input_path)
        self.input_path = input_path
        self.categories = self.read_categories_file(cat_path)
    
    def get_clean_trx_df(self):
        trx_df = self._load_transaction_file(self.input_path)
        trx_df = self._clean_up_transaction_df(trx_df)
        return trx_df
    
    def categorize_trxs(self, trx_df: pd.DataFrame) -> pd.DataFrame:
        """Read each transaction description and assign a category to it.

        Args:
            trx_df (pd.DataDrame): Input df without categories.

        Returns:
            pd.DataDrame: Output df with categories.
        """
        cats_so_far = []
        for cat in self.categories.keys():
            is_cat_match_column = [False] * len(trx_df)
            for value in self.categories[cat]:
                is_cat_match_column |= trx_df["full_description"].str.lower().str.contains(value)
            trx_df[cat] = (is_cat_match_column - trx_df[cats_so_far].sum(axis=1)) > 0
            cats_so_far.append(cat)
        return trx_df

    @staticmethod
    def _load_transaction_file(input_path: Union[str, Path], min_num_cols = 6):
        input_path = BaseTransactionReader._convert_to_pathlib_path(input_path)
        find_start = pd.read_excel(input_path).iloc[:, 0] == "F. Operativa"
        start_index = find_start.argmax()
        trx_df = pd.read_excel(input_path, skiprows=start_index+1)
        return trx_df

    @staticmethod
    def _clean_up_transaction_df(trx_df: pd.DataFrame) -> pd.DataFrame:
        # Drop several columns
        trx_df = trx_df.drop(["F. Operativa", "F. Valor", "Referencia 1", "Referencia 2"], axis=1)
        # Rename "Concepto" column into "full_description"
        trx_df = trx_df.rename(columns={"Concepto": "full_description"})
        return trx_df

    @staticmethod
    def read_categories_file(cat_path: Union[str, Path]) -> dict:
        """Read and load the categories file.

        Args:
            cat_path (Union[str, Path]): File where the categories file is located.

        Returns:
            dict: categories are the keys and the names linked to those categories are the values.
        """
        cat_path = BaseTransactionReader._convert_to_pathlib_path(cat_path)
        with open(cat_path) as f:
            cat_file = yaml.safe_load(f)
        return cat_file

