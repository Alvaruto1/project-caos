from flask import jsonify,request
from tests.core.web import app, render_view
from tests.db.DAO.mysqlDAO import DAOManagerMysql


@app.route('/search',methods=('GET',))
def search():
    mysqlDM = DAOManagerMysql()   
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    
    if user:
        search = request.args.get('search')
        users = mysqlDM.do(mysqlDM.USER, mysqlDM.GET_ALL,search)
        lista=[]        
        for us in users:
            lista.append({'email':us.email})
            
        return jsonify(lista)

    return render_view('sign_in.html')