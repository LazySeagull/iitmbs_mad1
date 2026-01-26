from flask import Flask , request , jsonify , render_template
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app)

class User(Resource):
    
    def get(self):
        return render_template('index.html')


api.add_resource(User , "/users")

if __name__ == "__main__":
    app.run(debug=True)

