import redis
import json
import uuid

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
ps = client.pubsub()

def publish_problem(coords):
    p_id = str(uuid.uuid4())
    client.set(f"{p_id}_problem", json.dumps(coords))
    client.publish("problems", p_id)
    return p_id


def get_solution(message):
    if message["type"] != "message":
        return
    
    s_id = message["data"]
    raw = client.get(f"{s_id}_solution")
    return json.loads(raw)

def is_solved(p_id):
    return client.get(f"{p_id}_solution") is not None

ps.subscribe("solutions")
id_1 = publish_problem([(0, 0), (1, 1)])
id_2 = publish_problem([(0, 2), (1, 1)])

print("Client listening...")
for message in ps.listen():
    print(message["data"])
    print(get_solution(message))
