import re
from bs4 import BeautifulSoup
from stablehorde import generate_image

URL_PATTERN = r'url\(["\']?(?P<url>[^\)]+?)["\']?\)'

def generate_images(html_content, STABLEHORDE_API_KEY, local_directory):
    soup = BeautifulSoup(html_content, "html.parser")
    image_elements = soup.find_all("img")

    for image_element in image_elements:
        alt = image_element.get("alt")
        img_src = image_element["src"]
        style = image_element.get("style", None)
        image_path = generate_image(style, alt, img_src, STABLEHORDE_API_KEY, local_directory)
        image_name = image_path.split("/")[-1]
        image_element["src"] = f"./images/{image_name}"

    # Process images in CSS
    style_elements = soup.find_all("style")
    for style_element in style_elements:
        css_content = style_element.string
        if css_content:
            css_urls = re.findall(URL_PATTERN, css_content)
            for css_url in css_urls:
                image_path = generate_image(None, "backgroung image with the name :"+css_url, css_url, STABLEHORDE_API_KEY, local_directory)
                image_name = image_path.split("/")[-1]
                new_url = f'./images/{image_name}'
                css_content = css_content.replace(css_url, new_url)
            style_element.string.replace_with(css_content)

    return str(soup)
