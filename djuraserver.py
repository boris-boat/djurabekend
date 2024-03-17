from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(120), nullable=False)
    number = db.Column(db.Integer,nullable=False)
    city = db.Column(db.String(80))

    def __repr__(self):
        return f'<User {self.username} {self.number} >'

with app.app_context():
    db.create_all()

@app.route('/login',methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first() 
    if not user:
        return jsonify({'message': 'Password and Username combination incorrect'})
    if user.password == data['password'] :
        return jsonify({'username': user.username,"number":user.number , "id":user.id,"city":user.city})
    else:
         return jsonify({'message': 'Password and Username combination incorrect'})
    
@app.route('/savedata',methods=["POST"])
def saveData():
    data = request.get_json()
    number = 0 if 'number' not in data else data['number']
    new_user = User(
            username=data["username"],
            password=data['password'],
            number=number,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Data saved',"user": new_user.username,"id" : new_user.id})

@app.route('/updatedata',methods=["PUT"])
def updatedata():
    data = request.get_json()
    
    userToUpdate = User.query.get_or_404(data["id"])

    userToUpdate.number = data['number']
    print(userToUpdate)
    db.session.commit()
    return jsonify({'message': 'User data updated',"user": userToUpdate.username})

if __name__ == '__main__':
    app.run()
