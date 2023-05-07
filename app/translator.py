import sys
import os
sys.path.append('../Translation')
from run_translation import *
from flask import Flask, render_template, request
import json
from unzip import unzip_models

sys.path.append('../Neural_Network')
from helpers import custom_standardization

app = Flask(__name__, 
            template_folder='front_end',
            static_folder='front_end/static/')



@app.route('/')
def home():
    # return render_template(os.path.abspath("front_end/index.html"))
    return render_template("index.html")    


@app.route('/translate', methods=['POST'])
def translate():

    unzip_models()

    if 'record' in request.form:
        # get input sentence from microphone
        input_sentence = get_text_mic() 
    else:
        # get input sentence from text input field
        input_sentence = request.form['input_text']
        
    input_language = request.form['input_language_selector']
    output_language = request.form['output_language_selector']
    
    if input_language == 'English' and output_language == 'Spanish':
        # translate english to spanish
        translation = do_translation(input_sentence, input_language='English')
    elif input_language == 'Spanish' and output_language == 'English':
        # translate spanish to english
        translation = do_translation2(input_sentence, input_language='Spanish')
    else:
        # unsupported language pair
        translation = 'Unsupported language pair'
        
    response = {
        'input_text': input_sentence,
        'output_text': translation,
        'input_language_selector': input_language,
        'output_language_selector': output_language,
        'translation': translation
    }
    
    return json.dumps(response)




if __name__ == "__main__":
    app.run(debug=True)