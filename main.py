from flask import Flask
from views import views

main = Flask(__name__)

main.register_blueprint(views, url_prefix="/")

##if __name__ == '__main__':
    ##app.run(debug=True, port=8000)


