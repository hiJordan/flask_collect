from flask import (
    Blueprint,
)

bp_main = Blueprint('bp_main', __name__)

from . import events, routes