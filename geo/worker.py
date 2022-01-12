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

def solve_problem(message : dict) -> None:
    """Solve a problem, published the answer to the "solution" queue
    
    Parameters
    -----------
    message : dict
        The redis message telling the worker there is a new problem to solve containing the ID.

    """
    #if it's not a 'message' type then it's not a problem
    if message["type"] != "message":
        return
    
    #retrieve the problem stored by the client
    p_id = message["data"]
    problem = json.loads(client.get(p_id))

    distances = calculate_pairwise_distance(problem["problem"])
    if distances:
        distances = distances[0]
    
    problem["solution"] = distances
    problem["solved"] = True
    client.set(p_id, json.dumps(problem))
    client.publish("solutions", p_id)

ps.subscribe(problems=solve_problem)
print("Worker listening")
thread = ps.run_in_thread(sleep_time=0.001)
