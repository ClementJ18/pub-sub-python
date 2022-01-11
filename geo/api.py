import redis

from flask import Flask
from flask import request

import json
from math import sqrt
from typing import List
from collections import namedtuple

app = Flask(__name__)
client = redis.Redis(host='localhost', port=6379)

problems        = {}
queue_problems  = []
queue_solutions = []



@app.route("/problems", methods=["POST"], defaults={'problem_id': None})
@app.route("/problems/<problem_id>", methods=["POST"])
def push_problem(problem_id):
    if problem_id is None:
        return False

    coords = request.get_json()
    if not isinstance(coords, list):
        raise ValueError("Request body must be JSON array")

    client.set(f"{problem_id}_problem", json.dumps(coords))
    return 200

@app.route("/solutions", methods=["GET"], defaults={'solution_id': None})
@app.route("/solutions/<solution_id>", methods=["GET"])
def get_solution(solution_id):
    if solution_id is None:
        return False

    distances = client.get(f"{solution_id}_solution")
