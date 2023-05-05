from dotenv import load_dotenv
import os
import subprocess
import openai
from github_utils import get_repo
from openai_utils import generate_html
from beautifulsoup import generate_images


# Load environment variables from .env file
load_dotenv()

# Set GitHub access token and repository name
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
REPO_NAME = os.environ["GITHUB_REPO_NAME"]

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set Stablehorde API key
STABLEHORDE_API_KEY = os.environ["STABLEHORDE_API_KEY"]

# Set prompt for OpenAI API
prompt_template = "I want you to create HTML code based on the input text: {}. Reply only with HTML code no other comments. Please include CSS for the page. For the images, the <img> tags must include at least two attributes: a style attribute with at least the heigh and width in pixel and a custom alt text attribute different for each image and with at least 100 words to describe the image."




def make_changes_and_push(input_text):
    # Set up local directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set up repository and commit message
    repo = get_repo(GITHUB_ACCESS_TOKEN, REPO_NAME)
    commit_message = f"Add HTML file based on input text: {input_text}"
    local_directory = os.path.join(script_directory, "cloned_repo")

    # Generate HTML content using OpenAI API
    prompt = prompt_template.format(input_text)
    html_content = generate_html(prompt)

    # Generate images using Stablehorde API
    html_content = generate_images(html_content, STABLEHORDE_API_KEY, local_directory)


    # Add the script to the HTML content
    script_tag = '''<script id="clhac43dd0002q0vl8ue830mv" data-name="databerry-chat-bubble" src="https://cdn.jsdelivr.net/npm/@databerry/chat-bubble@latest"></script>'''
    html_content = html_content.replace("</body>", f"{script_tag}</body>")

    # Clone or pull the repository
    if os.path.exists(local_directory):
        subprocess.run(f"git -C {local_directory} pull", shell=True)
    else:
        subprocess.run(
            f"git clone {repo.git_url.replace('git://', f'https://{GITHUB_ACCESS_TOKEN}@')} {local_directory}", shell=True)

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
#     make_changes_and_push(repo, local_directory, commit_message, input_text)

