from kubernetes import client, config as k8s_config
import random
import time
import argparse
import dacite
import yaml
from dataclasses import dataclass


@dataclass
class Pl8gueConfig:
    frequency: float = 5  # Seconds between pod creation attempts
    image: str = "nginx:latest"


def main():
    # Load config from yaml file
    parser = argparse.ArgumentParser("pl8gue")
    parser.add_argument("--config", type=str, default="config.yml")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
    config = dacite.from_dict(data_class=Pl8gueConfig, data=config)
    k8s_config.load_incluster_config()
    while True:
        create_pod(config.image)
        time.sleep(config.frequency)


def create_pod(image):
    v1 = client.CoreV1Api()
    pod = client.V1Pod()
    pod_name = "pl8gue-" + str(random.randint(1, 10000))
    pod.metadata = client.V1ObjectMeta(name=pod_name)
    pod.spec = client.V1PodSpec(containers=[client.V1Container(name=pod_name, image=image)])
    namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
    v1.create_namespaced_pod(namespace=namespace, body=pod)
    print("Pod created.")


if __name__ == '__main__':
    main()
    time.sleep(60)
