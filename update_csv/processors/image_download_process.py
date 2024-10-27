import os
import pandas as pd
from update_csv.downloader.image_downloader import download_image
from update_csv.api_handler.api_handler import get_prediction
from update_csv.constant import IMAGES_DIR


def process_image(row):
    image_url = row["Image"]
    image_name = os.path.basename(image_url)
    image_path = os.path.join(IMAGES_DIR, image_name)

    if download_image(image_url, image_path):
        prediction = get_prediction(image_path)
        os.remove(image_path)
    else:
        prediction = "link not working"

    return prediction
