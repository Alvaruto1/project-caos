from flask import redirect
from src.core.web import app

@app.route('/')
def index():        
    return redirect('sign_in')