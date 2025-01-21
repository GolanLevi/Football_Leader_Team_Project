from flask import Flask, jsonify
from flasgger import Swagger
from flask_restful import Api
from database import db
from routes.matches import matches_bp  # Blueprint for matches
from routes.teams import teams_bp  # Blueprint for teams

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)

# Home route
@app.route('/')
def home():
    return "Welcome to Football Leader API"

# Handle favicon.ico requests
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

# Database check route
@app.route('/db-check', methods=['GET'])
def db_check():
    """
    Check database connection and list collections.
    ---
    responses:
      200:
        description: Database is connected and collections are listed
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Database is connected"
            collections:
              type: array
              items:
                type: string
      500:
        description: Internal server error.
    """
    try:
        collections = db.list_collection_names()
        return jsonify({"message": "Database is connected", "collections": collections}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Register Blueprints
app.register_blueprint(matches_bp, url_prefix="/matches")
app.register_blueprint(teams_bp, url_prefix="/teams")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
