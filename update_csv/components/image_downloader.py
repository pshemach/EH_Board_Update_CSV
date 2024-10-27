import requests


def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"Error downloading image from {url}")
            return False
    except Exception as e:
        print(f"Exception occurred while downloading image from {url}: {e}")
        return False
    return True
