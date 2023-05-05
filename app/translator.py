import sys
import os
sys.path.append('../Translation')
from run_translation import main
from flask import Flask, render_template


app = Flask(__name__, 
            template_folder='front_end',
            static_folder='front_end/static/')



@app.route('/')
def index():
    # return render_template(os.path.abspath("front_end/index.html"))
    return render_template("index.html")    

# @app.route("/")
# def home():
#     return 'Flask server is running HEHE'




if __name__ == "__main__":
    app.run(debug=True)