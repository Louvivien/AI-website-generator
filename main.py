from dotenv import load_dotenv
import os
import subprocess
import openai
from github_utils import get_repo
from openai_utils import generate_html
from beautifulsoup import generate_images
import tempfile
import shutil
import datetime



# Load environment variables from .env file
load_dotenv()

# Set GitHub access token and repository name
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
REPO_NAME = os.environ["GITHUB_REPO_NAME"]

# Set GitHub access token and repository name
GIT_USER_EMAIL = os.environ["GIT_USER_EMAIL"]
GIT_USER_NAME = os.environ["GIT_USER_NAME"]

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set Stablehorde API key
STABLEHORDE_API_KEY = os.environ["STABLEHORDE_API_KEY"]

# Set prompt for OpenAI API
current_year = datetime.datetime.now().year

prompt_template = (
    f"Using {{style}}, I want you to create a one page website based on the input text: '{{input_text}}'." 
    f"Reply only with HTML code no other comments. Please include CSS for the page." 
    f"You can use complex UI components from {{style}}" 
    f"For the images, the <img> tags must include at least two attributes: a style attribute with at least the heigh and width in pixel and a custom alt text attribute different for each image and with at least 100 words to describe the image. The image names must be descriptive."
    f"There must be at least 2 paragraphs of text on the page."
    f"At the bottom of the website include the current year ({current_year}) and social network links" 
)
                   
# Too heavy
# prompt_template = (
#     f"Using {{style}}, I want you to create a one page website based on the input text: '{{input_text}}'."
#     f"Reply only with HTML code no other comments. Please include complex components if possible and CSS using a stylish color palette."
#     f"Each section must have a background color." 
#     f"There must be a header section" 
#     f"Always include a beautiful banner with a heading phrase and some text under it." 
#     f"For the images, they must be different and the <img> tags must include at least two attributes: a style attribute with at least the heigh and width in pixel and a custom alt text attribute different for each image and with at least 100 words to describe the image."
#     f"There can be a section about services, products or portfolio with beautiful pictures"
#     f"There can be testimonials that can be display in a carrousel. They can include little picture of the customers."
#     f"There can be an about us section"
#     f"There can be a location section that can include a map or an openstreet map background"
#     f"At the bottom of the website include the current year ({current_year}) and social network links" 

# )


def clean_image_directory(local_directory):
    images_path = os.path.join(local_directory, "images")
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    os.makedirs(images_path)

def make_changes_and_push(input_text, style):
    # # Set up local directory
    # script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set up repository and commit message
    repo = get_repo(GITHUB_ACCESS_TOKEN, REPO_NAME)
    commit_message = f"Add HTML file based on input text: {input_text}"

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        local_directory = os.path.join(temp_dir, "cloned_repo")

        # Clone the repository to the local_directory
        subprocess.run(
            f"git clone --depth 1 {repo.git_url.replace('git://', f'https://{GITHUB_ACCESS_TOKEN}@')} {local_directory}", shell=True)

        # Generate HTML content using OpenAI API
        prompt = prompt_template.format(input_text=input_text, style=style)
        html_content = generate_html(prompt)

        # Clean the images directory before generating new images
        clean_image_directory(local_directory)

        # Generate images using Stablehorde API
        html_content = generate_images(html_content, STABLEHORDE_API_KEY, local_directory)

        # Add the script to the HTML content
        script_tag = '''<script 
                        id="clh7ew6vj0000e9oga0of8r5p"
                        data-name="databerry-chat-bubble"
                        src="https://cdn.jsdelivr.net/npm/@databerry/chat-bubble@latest"
                        ></script>'''
        html_content = html_content.replace("</body>", f"{script_tag}</body>")

        # Clone or pull the repository
        if os.path.exists(local_directory):
            subprocess.run(f"git -C {local_directory} pull", shell=True)
        else:
            subprocess.run(
                f"git clone --depth 1 {repo.git_url.replace('git://', f'https://{GITHUB_ACCESS_TOKEN}@')} {local_directory}", shell=True)
            
        subprocess.run(f"git -C {local_directory} config user.email {GIT_USER_EMAIL}", shell=True)
        subprocess.run(f"git -C {local_directory} config user.name {GIT_USER_NAME}", shell=True)
   

        # Add, commit, and push the changes
        with open(os.path.join(local_directory, "index.html"), "w") as f:
            f.write(html_content)
        subprocess.run(f"git -C {local_directory} add .", shell=True)
        subprocess.run(f'git -C {local_directory} commit -m "{commit_message}"', shell=True)
        subprocess.run(f"git -C {local_directory} push", shell=True)


# if __name__ == "__main__":
#     # Code to be executed when the script is run as the main program

#     # Get input from user
#     input_text = input("Enter text to generate HTML content: ")

#     # Make changes and push to GitHub
#     make_changes_and_push(input_text)

