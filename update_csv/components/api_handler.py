import requests
from update_csv.constant import API_ENDPOINT


def get_prediction(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"image": f}
            response = requests.post(API_ENDPOINT, files=files)
            if response.status_code == 200:
                return response.json().get("board_types")
            else:
                print(f"Error with API response: {response.status_code}")
                return "Error"
    except FileNotFoundError:
        print(f"File not found for prediction: {image_path}")
        return "File not found"
    except Exception as e:
        print(f"Exception occurred while getting prediction: {e}")
        return "Error"
