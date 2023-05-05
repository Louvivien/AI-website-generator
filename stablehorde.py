import requests
import json
from time import sleep
import re
import math
import urllib.request



def generate_image(style, alt, img_src, STABLEHORDE_API_KEY, local_directory):
    # Extract width and height from the style string
    width_search = re.search('width: (\d+)px', style)
    height_search = re.search('height: (\d+)px', style)

    if width_search and height_search:
        width = int(width_search.group(1))
        height = int(height_search.group(1))
        # Adjust width and height to the nearest multiple of 64
        width_adjusted = 64 * math.ceil(width / 64)
        height_adjusted = 64 * math.ceil(height / 64)
    else:
        # Default values if width and height are not found in the style string
        width_adjusted = 64 * math.ceil(400 / 64)
        height_adjusted =  64 * math.ceil(300 / 64)
        print("ChatGPT did not generate style requirements")



    # Make a POST request to the Stablehorde API to generate an image
    url = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "Content-Type": "application/json",
        "apikey": STABLEHORDE_API_KEY,
    }
    body = {
        "prompt": alt+"### poorly drawn face, cloned face, poorly drawn animal, disfigured, mutilated, ugly",
        "censor_nsfw": False,
        "failed": False,
        "gathered": False,
        "index": 0,
        "jobId": "",
        "models": ["stable_diffusion"],
        "nsfw": True,
        "params": {
            "steps": 30,
            "n": 1,
            "sampler_name": "k_euler",
            "post_processing": ['GFPGAN'],
            "width": width_adjusted,
            "height": height_adjusted,
            "cfg_scale": 7,
            "seed_variation": 1000,
        },
        "r2": True,
        "shared": False,
        "trusted_workers": False,
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response_json = response.json()
    if "id" not in response_json:
        print("Error: API response does not contain 'id'")
        print(response_json)
        return None
    image_id = response_json["id"]

    # Poll the API to get the generated image URL
    status_url = f"https://stablehorde.net/api/v2/generate/status/{image_id}"
    while True:
        status_response = requests.get(status_url)
        status_data = status_response.json()
        if "done" in status_data and status_data["done"]:
            image_url = status_data["generations"][0]["img"]
            break
        elif "wait_time" in status_data and status_data["wait_time"] > 0:
            wait_time = status_data["wait_time"]
            print(
                f"Waiting {wait_time} seconds for the image to be generated...")
            sleep(wait_time)
        else:
            print("Polling API again without waiting.")
            sleep(1)  # To avoid overwhelming the API with requests

    # Download the image
    local_image_path = f"{local_directory}/{img_src.split('/')[-1].split('.')[0]}.webp"
    urllib.request.urlretrieve(image_url, local_image_path)
    print("Image generated:", local_image_path)

    return local_image_path
