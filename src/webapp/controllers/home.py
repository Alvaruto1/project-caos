from src.core.web import app, render_view

@app.route('/home')
def home():        
    return render_view('home.html')