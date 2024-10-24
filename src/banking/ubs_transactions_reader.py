import re
import yaml
from pathlib import Path
from typing import Union

import pandas as pd

from src.banking.base_transactions_reader import BaseTransactionReader


class UBSTrasactionReader(BaseTransactionReader):

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
        with open(input_path, 'r') as file:
            lines = file.readlines()
        # Identify the body of the file (main table containing transactions)
        for idx, line in enumerate(lines):
            if line.count(';') >= min_num_cols:
                start_idx = idx
                break
        df = pd.read_csv(input_path, delimiter=';', skiprows=start_idx)
        return df

    @staticmethod
    def _clean_up_transaction_df(trx_df: pd.DataFrame) -> pd.DataFrame:
        # Drop several columns
        trx_df = trx_df.drop(["Trade date", "Trade time", "Booking date", "Value date", "Currency",
                              "Footnotes", "Unnamed: 14", "Individual amount", "Transaction no."], axis=1)
        # Unite all description columns into one (full_description)
        desc_cols = [col for col in trx_df.columns if col.lower().startswith("description")]
        trx_df['full_description'] = trx_df[desc_cols].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        trx_df = trx_df.drop(desc_cols, axis=1)
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

