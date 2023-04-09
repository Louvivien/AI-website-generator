import openai
import os

def generate_html(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": "You are a programmer only producting high quality code"},
            {"role": "user", "content": "I want you to create HTML code based on the input text: Hello World Page. Reply only with HTML code no other comments"},
            {"role": "assistant", "content": """<!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <title>Hello World Page</title>
                                                </head>
                                                <body>
                                                    <h1>Hello World</h1>
                                                <img src="horse1.jpg" style="height: 300px; width: 400px;" class="img1" alt="Photo of a playful chestnut mare with a short mane and tail, rolling in the dirt. The horse is lying on its back with its legs in the air, looking happy and content."/>
                                                <img src="horse2.jpg" style="height: 300px; width: 400px;" class="img2" alt="Photo of a handsome bay gelding with a short mane and tail, standing in a stable. The horse is looking out of its stall with a calm expression on its face, and its ears perked up."/>
                                                </body>
                                                </html>}""",
             },
            {"role": "user", "content": prompt},
        ],
        n=1,
        temperature=0.5,
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']



