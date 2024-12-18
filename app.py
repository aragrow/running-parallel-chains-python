#Utilities
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, make_response, url_for, render_template_string
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import json
# Custom Imports
from info_form import GetInfoForm
from google_api_call import GoogleAPICall

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()
app.config['STATIC_FOLDER'] = 'static'
app.config['STATIC_URL'] = '/static'

print('I am executing Resume Job Optimizer - app.py')

class PublicIndex(Resource):

    def get(self):
        print('-- PlublicIndex.get')
        try:
            form = GetInfoForm()
            html_content = form.main()
            return html_content
        except Exception as e:
            # Handle errors and display on screen
            error_message = f"<h1>Error</h1><p>{str(e)}</p>"
            return make_response(error_message), 500  # HTTP 500 Internal Server Error

class PrivateIndex(Resource):
    #@auth.login_required
    def post(self):
        print('-- PrivateIndex.post')
        try:
            form = GoogleAPICall()
            html_content = form.main()

            # Wrap the HTML content in a JSON-compatible dictionary
            response_data = {"html_content": html_content}
            print("Response data:", response_data)

            # Use jsonify to generate a JSON response
            return response_data, 200
    
        except Exception as e:
            # Handle errors and display on screen
            error_message = f"<h1>Error</h1><p>{str(e)}</p>"
            return make_response(error_message), 500  # HTTP 500 Internal Server Error '''


api.add_resource(PublicIndex, '/')
api.add_resource(PrivateIndex, '/') 

if (__name__) == "__main__":
    app.run(debug=True, port=5600, ssl_context=("/Users/david/.ssl/cert.pem","/Users/david/.ssl/key.pem"))


