from flask import make_response
from src.core.web import app, render_view
from src.db.DAO.mysqlDAO import DAOManagerMysql
from src.utils.temp_toke import PerpetualTimer


@app.route('/logout')
def logout():
    response = make_response(render_view('sign_in.html'))
    response.set_cookie("token",'')
    p = PerpetualTimer()
    p.cancel()
    return response