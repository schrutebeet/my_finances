from pathlib import Path

import pandas as pd



class UBSTrasactionReader:

    def __init__(self, transaction_path: str) -> None:
        trx_df = self._load_transaction_file(transaction_path)
        trx_df = self._clean_up_transaction_df(trx_df)

    @staticmethod
    def _clean_up_transaction_df(trx_df: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def _load_transaction_file(transaction_path: str) -> pd.DataFrame:
        transaction_path = Path(transaction_path)
        if transaction_path.suffix == ".csv":
            breakpoint()
            trx_df = pd.read_csv(transaction_path, on_bad_lines='skip', sep=";")
        else:
            raise ValueError("Please, provide a .csv file.")
        return trx_df
