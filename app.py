from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from main import make_changes_and_push, get_repo, GITHUB_ACCESS_TOKEN, REPO_NAME

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form['input_text']
    repo = get_repo(GITHUB_ACCESS_TOKEN, REPO_NAME)
    commit_message = f"Add HTML file based on input text: {input_text}"
    script_directory = os.path.dirname(os.path.abspath(__file__))
    local_directory = os.path.join(script_directory, "cloned_repo")
    make_changes_and_push(repo, local_directory, commit_message, input_text)
    return jsonify({"status": "success"})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["input_text"]
        repo = get_repo(GITHUB_ACCESS_TOKEN, REPO_NAME)
        commit_message = f"Add HTML file based on input text: {input_text}"
        script_directory = os.path.dirname(os.path.abspath(__file__))
        local_directory = os.path.join(script_directory, "cloned_repo")
        make_changes_and_push(repo, local_directory, commit_message, input_text)
        return redirect(url_for("success"))
    return render_template("index.html")

@app.route("/success")
def success():
    return "HTML content generated and pushed to GitHub successfully! "

if __name__ == "__main__":
    app.run(debug=True)
