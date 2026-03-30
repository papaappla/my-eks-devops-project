from kubernetes import client, config
import os

def load_k8s_config():
    try:
        # 1. EKS 클러스터 내부에서 실행될 때 (우선순위)
        config.load_incluster_config()
    except config.ConfigException:
        try:
            # 2. 로컬 PC에서 실행될 때
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("K8s 설정을 로드할 수 없습니다.")

load_k8s_config()
v1 = client.CoreV1Api()
