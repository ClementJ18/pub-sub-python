import json
import redis
from math import sqrt
from solver import calculate_pairwise_distance


client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
ps = client.pubsub()

"""
[
    (x, y),
    (x, y),
    ...
]

"""

def solve_problem(message):
    #if it's not a 'message' type then it's not a problem
    if message["type"] != "message":
        return
    
    #retrieve the problem stored by the client
    problem_id = message["data"]
    raw = client.get(f"{problem_id}_problem")
    coords = json.loads(raw)

    distances = calculate_pairwise_distance(coords)
    if distances:
        distances = distances[0]
    
    client.set(f"{problem_id}_solution", json.dumps(distances))
    client.publish("solutions", problem_id)

ps.subscribe(problems=solve_problem)
print("Worker listening")
thread = ps.run_in_thread(sleep_time=0.001)
