from flask import Flask, request, jsonify
import speech_recognition as sr
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})
    except sr.RequestError:
        return jsonify({"error": "Could not request results from Google Speech Recognition service"})

@app.route('/command', methods=['POST'])
def process_command():
    data = request.json
    command_text = data.get("text")
    doc = nlp(command_text)
    # Example command processing
    if "open" in command_text:
        # Execute system command
        pass
    return jsonify({"response": "Command executed"})

if __name__ == '__main__':
    app.run(debug=True)
