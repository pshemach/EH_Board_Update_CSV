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
        image_url = row.get("Image")

        # Validate image_url to ensure it's a non-empty string
        if not isinstance(image_url, str) or not image_url.strip():
            predictions.append("Invalid or missing URL")
            continue

        image_name = os.path.basename(image_url)
        image_path = os.path.join(IMAGES_DIR, image_name)

        # Try downloading the image; if it fails, skip to the next entry
        if not download_image(image_url, image_path):
            predictions.append("Link not working")
            continue

        # Try getting a prediction; if it fails, add an error message
        try:
            prediction = get_prediction(image_path)
            predictions.append(prediction)
        except Exception as e:
            print(f"Error processing image '{image_url}': {e}")
            predictions.append("Prediction error")
            continue

        # Attempt to delete the image file after processing
        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Exception occurred while removing image file: {e}")

    return predictions