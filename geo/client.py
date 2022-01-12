import redis
import json
import uuid
import argparse

from typing import List, Tuple

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
ps = client.pubsub()

def publish_problem(coords : List[Tuple[int, int]]) -> str:
    """Publish a problem to be solved, takes a list of lat/lon coordinates and returns
    the UUID generated for the problem.

    Parameters
    -----------
    coords : List[Tuple[int, int]]
        The list of lat/lon coordinates that the pairwise distance will be calculated for


    Returns
    --------
    str
        The ID of the problem

    """
    p_id = str(uuid.uuid4())
    client.set(p_id, json.dumps({"id": p_id, "problem": coords, "solution": [], "solved": False}))
    client.publish("problems", p_id)
    return p_id

def get_solution(message : dict) -> List[int]:
    """Retrieve the solution to the problem based on its UUID

    Parameters
    -----------
    message : dict
        The redis message containing the problem ID


    Returns
    --------
    List[int]
        List of pairwise distance that are the solution to the problem, can be empty
    """
    if message["type"] != "message":
        return
    
    p_id = message["data"]
    raw = client.get(p_id)
    return json.loads(raw)["solution"]

def is_solved(p_id : str) -> bool:
    """Check if a problem has been solved based on its ID

    Parameters
    -----------
    p_id : str
        The UUID of the problem to be checked

    Returns
    --------
    bool
        True if the problem has been processed, False if still awaiting

    """
    return json.loads(client.get(p_id))["solved"]


parser = argparse.ArgumentParser(description='Publish some problems')
group = parser.add_mutually_exclusive_group()
group.add_argument('--file', '--f', dest='file', type=argparse.FileType('r'))
group.add_argument('--problem', '--p', dest='problem')
args = parser.parse_args()

ps.subscribe("solutions")
ids = []
if args.file:
    problems = json.load(args.file)
    for p in problems:
        ids.append(publish_problem(p))
elif args.problem:
    ids = [publish_problem(json.loads(args.problem))]

print("Client listening for answers")
for message in ps.listen():
    print(message["data"])
    print(get_solution(message))

    if message["data"] in ids:
        ids.remove(message["data"])

    if not ids:
        break
