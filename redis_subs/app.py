import redis # type: ignore

# Connect to Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Subscribe to a channel
pubsub = redis_client.pubsub()
pubsub.subscribe("mychannel")

print("Subscribed to 'mychannel'. Waiting for messages...")

# Read messages in real-time
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")