import requests
import os
import json
from datetime import datetime
from google import genai

# 설정
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus-kube-prometheus-prometheus.monitoring:9090")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_prometheus_metric(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query})
        results = response.json()['data']['result']
        if results:
            return results[0]['value'][1]
        return "0"
    except Exception as e:
        print(f"Error fetching metric: {e}")
        return "0"

def generate_ai_insight(cpu, mem, running, total):
    if not GEMINI_API_KEY:
        return "Gemini API Key가 설정되지 않아 기본 메시지를 출력합니다. 현재 상태는 안정적입니다."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
        당신은 숙련된 SRE(Site Reliability Engineer)입니다. 
        다음은 EKS 클러스터의 현재 메트릭입니다:
        - CPU 사용률: {cpu}%
        - 메모리 사용률: {mem}%
        - Pod 상태: {running} / {total} (Running / Total)

        이 데이터를 바탕으로 현재 시스템의 건강 상태를 진단하고, 
        인프라 엔지니어에게 도움이 될 만한 인사이트를 한 줄로 짧고 멋지게 작성해 주세요. 
        (친절하고 전문적인 말투 사용, 이모지 포함)
        """
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return "".join([part.text for part in response.candidates[0].content.parts if part.text]).strip()
    except Exception as e:
        return f"AI 인사이트 생성 중 오류 발생: {e}"

def generate_report():
    cpu_usage = float(get_prometheus_metric('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) / sum(kube_node_status_allocatable:cpu:core) * 100'))
    mem_usage = float(get_prometheus_metric('sum(container_memory_working_set_bytes) / sum(kube_node_status_allocatable:memory:bytes) * 100'))
    total_pods = get_prometheus_metric('count(kube_pod_info)')
    running_pods = get_prometheus_metric('count(kube_pod_status_phase{phase="Running"})')

    ai_insight = generate_ai_insight(cpu_usage, mem_usage, running_pods, total_pods)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_emoji = "✅" if cpu_usage < 80 else "⚠️"

    report_text = f"""
*🚀 [EKS AI Reporter] 인프라 자동 분석 리포트*
--------------------------------------------------
*📅 분석 일시:* {now}
*🌐 클러스터 상태:* {status_emoji} 정상 가동 중

*📊 핵심 메트릭 요약:*
• *CPU 사용률:* {cpu_usage:.2f}%
• *메모리 사용률:* {mem_usage:.2f}%
• *Pod 상태:* {running_pods} / {total_pods} (Running / Total)

*🤖 AI SRE의 인사이트:*
"{ai_insight}"
--------------------------------------------------
"""
    return report_text

def send_to_slack(text):
    payload = {"text": text}
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

if __name__ == "__main__":
    report = generate_report()
    send_to_slack(report)
    print("Slack 보고 완료!")

