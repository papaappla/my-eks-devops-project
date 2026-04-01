# -*- coding: utf-8 -*-
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
        return "Gemini API Key is missing. Infrastructure is stable."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        # 프롬프트를 영어로 구성하고 결과만 한글로 요청하여 인코딩 충돌 최소화
        prompt = f"""
        Act as a Senior SRE and FinOps expert.
        Analyze these EKS metrics (Instance: t3.small, 2 vCPU, 2GB RAM):
        - CPU Usage: {cpu:.2f}%
        - Memory Usage: {mem:.2f}%
        - Pod Status: {running} / {total} (Running/Total)

        Task:
        1. Diagnose system health.
        2. Provide FinOps advice (e.g., downgrade to t3.micro if CPU < 15%).
        3. Write a 1-sentence insight in KOREAN with emojis for a Slack report.
        """
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        insight = "".join([part.text for part in response.candidates[0].content.parts if part.text]).strip()
        return insight
    except Exception as e:
        # 에러 메시지도 영어로 출력하여 인코딩 에러 전파 방지
        print(f"AI Generation Error: {str(e)}")
        return f"AI Insight Error: {str(e)}"

def generate_report():
    cpu_usage = float(get_prometheus_metric('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) / sum(kube_node_status_allocatable:cpu:core) * 100'))
    mem_usage = float(get_prometheus_metric('sum(container_memory_working_set_bytes) / sum(kube_node_status_allocatable:memory:bytes) * 100'))
    total_pods = get_prometheus_metric('count(kube_pod_info)')
    running_pods = get_prometheus_metric('count(kube_pod_status_phase{phase="Running"})')

    ai_insight = generate_ai_insight(cpu_usage, mem_usage, running_pods, total_pods)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_emoji = "✅" if cpu_usage < 80 else "⚠️"

    report_text = f"""
*🚀 [EKS AI Reporter] Infrastructure Analysis*
--------------------------------------------------
*📅 Date:* {now}
*🌐 Status:* {status_emoji} Stable

*📊 Metrics Summary:*
• *CPU:* {cpu_usage:.2f}%
• *Memory:* {mem_usage:.2f}%
• *Pods:* {running_pods} / {total_pods}

*🤖 AI SRE Insight:*
"{ai_insight}"
--------------------------------------------------
"""
    return report_text

def send_to_slack(text):
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL is missing.")
        return
    try:
        payload = {"text": text}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Slack Error: {str(e)}")

if __name__ == "__main__":
    print("Starting AI Infrastructure Analysis...")
    report = generate_report()
    send_to_slack(report)
    print("Report Sent Successfully!")
