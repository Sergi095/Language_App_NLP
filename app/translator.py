import sys
import os
sys.path.append('../Translation')
from run_translation import *
from flask import Flask, render_template, request
import json

sys.path.append('../Neural_Network')
from helpers import custom_standardization

app = Flask(__name__, 
            template_folder='front_end',
            static_folder='front_end/static/')



@app.route('/')
def home():
    # return render_template(os.path.abspath("front_end/index.html"))
    return render_template("index.html")    

# @app.route('/translate', methods=['POST'])
# def translate():
#     input_sentence = ''
#     if 'record' in request.form:
#         input_sentence = get_text_mic()        
#         input_language = request.form['input_language_selector']
#         output_language = request.form['output_language_selector']
#         translation = do_translation(input_sentence)
#         # set the transcribed text in the input text box
#         response = {
#             'input_text': input_sentence,
#             'recorded-text': input_sentence,
#             'output_text': translation,
#             'input_language_selector': input_language,
#             'output_language_selector': output_language,
#             'translation': translation
#         }
#     else:
#         input_sentence = request.form['input_text']
#         input_language = request.form['input_language_selector']
#         output_language = request.form['output_language_selector']
#         translation = do_translation(input_sentence)
#         response = {
#             'input_text': input_sentence,
#             'output_text': translation,
#             'input_language_selector': input_language,
#             'output_language_selector': output_language,
#             'translation': translation
#         }
#     return json.dumps(response)
@app.route('/translate', methods=['POST'])
def translate():
    if 'record' in request.form:
        # get input sentence from microphone
        input_sentence = get_text_mic() 
    else:
        # get input sentence from text input field
        input_sentence = request.form['input_text']
        
    input_language = request.form['input_language_selector']
    output_language = request.form['output_language_selector']
    
    if input_language == 'english' and output_language == 'spanish':
        # translate english to spanish
        translation = do_translation2(input_sentence, input_language='english')
    elif input_language == 'spanish' and output_language == 'english':
        # translate spanish to english
        translation = do_translation2(input_sentence, input_language='spanish')
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