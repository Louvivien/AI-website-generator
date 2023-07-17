from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from main import make_changes_and_push
from statistics import mean
import time
import threading

app = Flask(__name__)

processing_times = []

def calculate_average_time():
    if not processing_times:
        return 115
    return mean(processing_times)

def background_task():
    while True:
        print("Doing nothing...")
        time.sleep(600)  # Delay for 10 minutes

@app.route('/generate', methods=['POST'])
def generate():
    start_time = time.time()
    print('Average processing time:', processing_times)
    input_text = request.form['input_text']
    try:
        make_changes_and_push(input_text, style='Bootstrap')
        processing_time = time.time() - start_time
        print('Processing time:', processing_time)
        processing_times.append(processing_time)
        return jsonify({"status": "success", "message": "HTML content generated and pushed to GitHub successfully!<br>The content has been deployed on Vercel. <br><br>GitHub Repository: <a href='https://github.com/Louvivien/test' target='_blank'>https://github.com/Louvivien/test</a> <br>Vercel URL: <a href='https://test-louvivien.vercel.app/' target='_blank'>https://test-louvivien.vercel.app/</a>"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "An error occurred. Please try again."})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["input_text"]
        make_changes_and_push(input_text, style='Bootstrap')
        return redirect(url_for("success"))
    avg_time = calculate_average_time()
    return render_template("index.html", avg_time=avg_time)

@app.route("/success")
def success():
    return "HTML content generated and pushed to GitHub successfully!<br>The content has been deployed on Vercel. <br><br>GitHub Repository: <a href='https://github.com/Louvivien/test' target='_blank'>https://github.com/Louvivien/test</a> <br>Vercel URL: <a href='https://test-louvivien.vercel.app/' target='_blank'>https://test-louvivien.vercel.app/</a>"

if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()
    app.run(debug=True)
