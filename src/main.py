from pathlib import Path

from src.banking.ubs_transactions_reader import UBSTrasactionReader


if __name__ == "__main__":
    ubs_trx_path = Path("/Users/ricky/Downloads/ubs_september_24.csv")
    cat_path = Path("/Users/ricky/Documents/GitHub/my_finances/config/ubs_expenditure_cat.yaml")
    ubs_trxs = UBSTrasactionReader(ubs_trx_path, cat_path)
    ubs_trxs_df = ubs_trxs.get_clean_trx_df()
    ubs_trxs.categorize_trxs(ubs_trxs_df)
