from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from routes.teams import Teams
from routes.matches import Matches
from routes.statistics import Statistics

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)

api.add_resource(Teams, '/teams')
api.add_resource(Matches, '/match')
api.add_resource(Statistics, '/statistics')

@app.route('/')
def home():
    """
    Home Page
    ---
    responses:
      200:
        description: Welcome message
    """
    return "Welcome to the Football API"

if __name__ == '__main__':
    app.run(debug=True)
