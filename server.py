from flask import Flask
from flask import render_template
from flask_restful import Api, Resource

app = Flask(__name__)
app._static_folder = "./"
api = Api(app)

# flask requires this to be in a subdirectory called templates/
@app.route('/')
def index():
    return render_template('index.html')

# Classes
class HelloWorld(Resource):
    # override
    def get(self):
        # return as json object
        return {None}


# Resources

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port = 80)
    app.run(debug=True)