
from flask import Flask, make_response
#from nonce_tool import NonceTool

class GetInfoForm:

    def __init__(self):

        #self.nonce = NonceTool.generate_nonce()
        self.nonce = 'hello'

    def main(self):

        html_form = f"""
            <h2>Hi, I am the Resume Job Optimizer Assistant</h2>
            <h3>Oops! You are here by mistake, please try again.</h3>
        """

        html_css = """"""
        
        html_content = html_form + html_css
        # Create a response object and set the correct content type
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'  # Ensure the content is treated as HTML
        return response