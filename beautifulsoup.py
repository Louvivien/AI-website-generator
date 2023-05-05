from bs4 import BeautifulSoup
from stablehorde import generate_image


def generate_images(html_content, STABLEHORDE_API_KEY, local_directory):
    soup = BeautifulSoup(html_content, "html.parser")
    image_elements = soup.find_all("img")

    for image_element in image_elements:
        alt = image_element.get("alt")
        img_src = image_element["src"]
        style = image_element.get("style", None) 
        image_path = generate_image(style, alt, img_src, STABLEHORDE_API_KEY, local_directory)
        image_name = image_path.split("/")[-1]
        image_element["src"] = image_name
    return str(soup)
