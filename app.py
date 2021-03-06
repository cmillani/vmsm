from flask import Flask
from routes import videogame_route

def create_app():
   app = Flask(__name__)

   @app.route('/')
   def hello_world():
       return 'Hello, World!'

   app.register_blueprint(videogame_route)

   return app


if __name__ == "__main__":
   app = create_app()
   app.run(host='0.0.0.0', debug=True)
