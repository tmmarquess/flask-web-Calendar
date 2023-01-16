from src.modules.controllers.home_controller import *
from src.modules.controllers.event_controller import *
from src.modules.controllers.user_controller import *
from src.resources.app import *
from get_ip import get_ip


if __name__ == "__main__":
    app.run(host=get_ip(), port=5000, debug=False, threaded=True)
