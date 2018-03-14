import json
import random
import string
import time

generate = lambda k: ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
current_milli = lambda: int(round(time.time() * 1000))
emotes = ["😆", "😮", "👎", "😢", "😍", "😠"]

"""
TEMPLATE
{"type":"message","attachments":[],"body":"...",
"threadType":"GROUP","messageID":"...","senderID":"...",
"threadID":"...","messageReactions":[{"reaction":"😆","userID":"..."}],
"isSponsered":false,"timestamp":"..."}
"""
# 10 users
ids = [generate(5) for _ in range(10)]
threadId = "1337"

N_MESSAGE = 100
msgs = []
for i in range(N_MESSAGE):
    msgs.append({'type': 'message',
                 'attachments': [],
                 'body': generate(10),
                 'threadType': 'GROUP',
                 'messageID': str(i),
                 'senderID': random.choice(ids),
                 'threadID': threadId,
                 'isSponsered': False,
                 'timestamp': current_milli() - i,
                 'messageReactions': [{'reaction': random.choice(emotes),
                                       'userID': random.choice(ids)}]})
with open('fake.json', 'w') as f:
    json.dump(msgs, f)
