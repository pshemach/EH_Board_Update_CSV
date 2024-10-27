import os
from tqdm import tqdm
from update_csv.downloader.image_downloader import download_image
from update_csv.components.api_handler import get_prediction
from update_csv.constant import IMAGES_DIR
from update_csv.utils import make_dir

make_dir(IMAGES_DIR)


def predictions_df(df):
    predictions = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        image_url = row["Image"]
        image_name = os.path.basename(image_url)
        image_path = os.path.join(IMAGES_DIR, image_name)

        if not download_image(image_url, image_path):
            predictions.append("Link not working")
            continue

        prediction = get_prediction(image_path)
        predictions.append(prediction)

        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Exception occurred while removing image file: {e}")

    return predictions
