import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

print("Agent work:", config["agent"]["work"])
print("Interval:", config["agent"]["interval_seconds"])
print("Job queue:", config["controller"]["queue_name"])
print("Result queue:", config["controller"]["result_queue"])

