from flask import Flask,request,jsonify

app=Flask(__name__)
USERS={'1':{'name':'alice','data':'secret1'},'2':{'name':'bob','data':'secret2'}}

@app.route('/user/<uid>/data')
def get_data(uid):
    auth=request.headers.get('X-User-ID')
    if not auth:
        return jsonify({'error':'not authenticated'}),401
    return jsonify({'data':USERS.get(uid,{}).get('data')})
