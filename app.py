from src.modules.controllers.home_controller import *
from src.modules.controllers.event_controller import *
from src.modules.controllers.user_controller import *
from src.resources.app import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
