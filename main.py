from github import Github
from dotenv import load_dotenv
import os
import subprocess
import openai

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set GitHub access token and repository name
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
REPO_NAME = os.environ["GITHUB_REPO_NAME"]


def get_repo(access_token, repo_name):
    github = Github(access_token)
    user = github.get_user()
    repo = user.get_repo(repo_name)
    return repo


def make_changes_and_push(repo, local_directory, commit_message, input_text):
    # Generate HTML content using OpenAI API
    prompt = f"I want you to create HTML code based on the input text: {input_text}. Reply only with HTML code no other comments. Please include CSS and images. For the images, you must specify the size and include a custom alt text different for each image and with at least 100 words to describe the image."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a programmer only producting high quality code"},
            {"role": "user", "content": "I want you to create HTML code based on the input text: Hello World Page. Reply only with HTML code no other comments"},
            {"role": "assistant", "content": """<!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>Hello World Page</title>
                                                </head>
                                                <body>
                                                    <h1>Hello World</h1>
                                                </body>
                                                </html>}""",
            },
            {"role": "user", "content": prompt},
        ],
        n=1,
        temperature=0.5,
    )

    
    # Print the response
    print(response['choices'][0]['message']['content'])

    # Parse the response and extract the HTML code
    html_content = response['choices'][0]['message']['content']
    if "<!DOCTYPE html>" not in html_content or "</html>" not in html_content:
        raise ValueError("Response does not contain valid HTML code")
    else:
        start_index = html_content.index("<!DOCTYPE html>")
        end_index = html_content.index("</html>") + len("</html>")
        html_content = html_content[start_index:end_index]
    
    # Clone or pull the repository
    if os.path.exists(local_directory):
        subprocess.run(f"git -C {local_directory} pull", shell=True)
    else:
        subprocess.run(f"git clone {repo.git_url.replace('git://', f'https://{GITHUB_ACCESS_TOKEN}@')} {local_directory}", shell=True)
    
    # Add, commit, and push the changes
    with open(os.path.join(local_directory, "index.html"), "w") as f:
        f.write(html_content)
    subprocess.run(f"git -C {local_directory} add .", shell=True)
    subprocess.run(f'git -C {local_directory} commit -m "{commit_message}"', shell=True)
    subprocess.run(f"git -C {local_directory} push", shell=True)





if __name__ == "__main__":
    # Get input from user
    input_text = input("Enter text to generate HTML content: ")
    
    # Set up repository and commit message
    repo = get_repo(GITHUB_ACCESS_TOKEN, REPO_NAME)
    commit_message = f"Add HTML file based on input text: {input_text}"
    
    # Set up local directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    local_directory = os.path.join(script_directory, "cloned_repo")
    
    # Make changes and push to GitHub
    make_changes_and_push(repo, local_directory, commit_message, input_text)
