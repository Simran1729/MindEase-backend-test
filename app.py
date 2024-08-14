from flask import Flask, request,jsonify
from dotenv import load_dotenv
import os
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv() #loads the .env file

#getting api_key from env file
openai_api_key = os.getenv('API_KEY')

if not openai_api_key:
    print("api_key not set")
    exit(1)


#test route
@app.route('/', methods = ['GET'])
def get_route():
    return jsonify({"message" : "Server is running"})


#openai Client
client = openai.OpenAI(api_key=openai_api_key)

conversations = []

@app.route('/v1/chat/completions', methods = ['POST'])
def converse():
    try:
        #getting user prompt from body
        user_prompt = request.get_json()['prompt']
        if not user_prompt or len(user_prompt)>2000:
            return jsonify({"message" : "Invalid input"}), 400
        message = {"role" : "user", "content" : user_prompt}
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= [message],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format= {"type": "text"}
        )

        response_text = response.choices[0].message.content
        conversations.append({"user" : user_prompt, "ai" : response_text})
        return jsonify({"response" : response_text, "conversation" : conversations})
    except openai.OpenAIError as e :
        return jsonify({"error" : str(e)}), 500
    except KeyError:
        return jsonify({"error" : "Inavlid request body"}), 400
    
