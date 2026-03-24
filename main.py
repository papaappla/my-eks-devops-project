from fastapi import FastAPI
from kubernetes import client, config
import asyncio

app = FastAPI()

# K8s 인증 설정 (로컬의 ~/.kube/config 파일을 읽어옵니다)
try:
    config.load_kube_config()
except:
    # 클러스터 내부에서 실행될 경우를 대비
    config.load_incluster_config()

@app.get("/pods")
async def get_pods():
    v1 = client.CoreV1Api()
    
    # 비동기로 Pod 리스트 가져오기 (비동기 처리는 Python의 강점입니다)
    # PHP와 달리 서버가 멈추지 않고 여러 요청을 처리할 수 있죠.
    ret = v1.list_pod_for_all_namespaces(watch=False)
    
    pod_list = []
    for i in ret.items:
        pod_list.append({
            "namespace": i.metadata.namespace,
            "name": i.metadata.name,
            "status": i.status.phase,
            "ip": i.status.pod_ip
        })
        
    return {"total_pods": len(pod_list), "items": pod_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
