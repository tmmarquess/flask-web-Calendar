from flask import Flask
from flask_login import login_manager, LoginManager, login_user
from flask_bcrypt import Bcrypt
from pony.flask import Pony, db_session
from src.modules.database import usuario_repository
import connexion

app = connexion.App(__name__, specification_dir="../")
app.add_api("swagger.yml")

app.app.secret_key = "mySuperSecretKey"
bcrypt = Bcrypt(app.app)

Pony(app.app)
login_manager = LoginManager(app.app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return usuario_repository.get_user_by_id(user_id)


@db_session
def authenticate_user(email, password):
    possible_user = usuario_repository.get_user_by_email(email)
    if not possible_user:
        return False

    if bcrypt.check_password_hash(possible_user.senha, password):
        login_user(possible_user)
        possible_user.set_authenticated(True)
        return True
    else:
        return False
