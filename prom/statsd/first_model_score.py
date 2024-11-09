from statsd import StatsClient
import logging

logging.basicConfig(level=logging.INFO)
statsd_client = StatsClient(host='statsd-exporter', port=8125)

# Send the model score metric
model_score = 10000  # Replace this with the actual score logic
statsd_client.gauge('model.score', model_score)
logging.info(f"Sent model.score with value: {model_score}")