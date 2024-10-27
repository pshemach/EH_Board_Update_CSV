import pandas as pd
from update_csv.prediction.get_predictions import predictions_df
from update_csv.constant import DF_SPLITS_ROW, OUTPUT_CSV, OUTPUT_FOLDER
from update_csv.utils import remove_brackets
from update_csv.utils import make_dir

make_dir(OUTPUT_CSV)


def process_df(df):
    try:
        df = pd.read_csv(df)
        for i in range(0, len(df), DF_SPLITS_ROW):
            proc_df = df.iloc[i : i + DF_SPLITS_ROW]

            preds = predictions_df(proc_df)

            proc_df["Prediction"] = preds
            proc_df["Prediction"] = proc_df["Prediction"].apply(remove_brackets)

            csv_name = f"{OUTPUT_FOLDER}/output_{i}.csv"
            proc_df.to_csv(csv_name, index=False)
            return csv_name
    except Exception as e:
        raise Exception(f"Error processing CSV file: {str(e)}")
