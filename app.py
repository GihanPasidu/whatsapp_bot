from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configure OpenAI API key (set your actual API key as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Endpoint for haiku generation
@app.route('/whatsapp', methods=['POST'])
def generate_haiku():
    # Get the message from the request
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # Call OpenAI API to generate a haiku
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change this to a model you have access to
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes haikus."},
                {"role": "user", "content": user_message}
            ]
        )
        haiku = response['choices'][0]['message']['content'].strip()

    except openai.error.RateLimitError:
        # Fallback haiku response when quota is exceeded
        haiku = "Function calls itself,\nLayers deep, endless descent,\nCode mirrors the soul."

    # Return the haiku in JSON format
    return jsonify({"reply": haiku})

if __name__ == '__main__':
    app.run(debug=True)
