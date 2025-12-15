import ccxt
from flask import Blueprint, request, jsonify
from utils.crypto import decrypt
from db import get_db

auto_trading_pro_bp = Blueprint("auto_trading_pro", __name__)
