import json
import redis as redis
from flask import Flask, request
from loguru import logger
import requests


HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

# create a Flask server, and allow us to interact with it using the app variable
app = Flask(__name__)


@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(
        f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200



@app.route('/collect', methods=['POST'])
def collect_engine_temperature():

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)

    sum_tempeture = sum(float(value) for value in engine_temperature_values)
    average_engine_temperature = sum_tempeture/len(engine_temperature_values)

    logger.info(f"current_engine_temperature: {engine_temperature_values[0]}")
    logger.info(f"average_engine_temperature: {average_engine_temperature}")

    return {
        "current_engine_temperature": engine_temperature_values[0],
        "average_engine_temperature" :average_engine_temperature
        }, 200

