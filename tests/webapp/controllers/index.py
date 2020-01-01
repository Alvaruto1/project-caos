from flask import redirect
from tests.core.web import app

@app.route('/')
def index():        
    return redirect('sign_in')