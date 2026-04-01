# -*- coding: utf-8 -*-
import requests
import os
import json
import sys
from datetime import datetime
from google import genai

# 시스템 출력 인코딩 강제 설정 (한글 깨짐 방지)
if sys.stdout.encoding != 'utf-8':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 설정 (환경 변수 정제)
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus-kube-prometheus-prometheus.monitoring:9090").strip()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def get_prometheus_metric(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query}, timeout=10)
        response.raise_for_status()
        results = response.json()['data']['result']
        if results:
            return results[0]['value'][1]
        return "0"
    except Exception as e:
        print(f"Metric Fetch Error ({query[:20]}...): {e}")
        return "0"

def generate_ai_insight(cpu, mem, running, total):
    if not GEMINI_API_KEY:
        return "Gemini API Key is missing. Infrastructure is stable."

    try:
        # API Key의 보이지 않는 문자를 제거하기 위해 다시 한번 strip()
        client = genai.Client(api_key=GEMINI_API_KEY.replace('"', '').replace("'", "").strip())
        
        prompt = f"""
        Act as a Senior SRE. Analyze EKS metrics:
        - CPU: {cpu:.2f}%
        - Mem: {mem:.2f}%
        - Pods: {running}/{total}
        
        Task: Write a 1-sentence infrastructure status report in KOREAN with emojis.
        Focus on system health and cost optimization.
        """
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        # 텍스트 추출 시 발생할 수 있는 인코딩 문제 방지
        insight_parts = [part.text for part in response.candidates[0].content.parts if part.text]
        insight = "".join(insight_parts).strip()
        return insight
    except Exception as e:
        # 에러 메시지에 유니코드가 포함될 수 있으므로 안전하게 처리
        error_msg = str(e).encode('utf-8', 'ignore').decode('utf-8')
        print(f"AI Generation Error: {error_msg}")
        return f"AI Insight Generation failed. (Check API Key or Quota)"

def generate_report():
    # 더 범용적인 쿼리로 수정 (Node 기준)
    cpu_query = 'avg(instance:node_cpu_utilization:ratio * 100) or vector(0)'
    mem_query = 'avg(instance:node_memory_utilization:ratio * 100) or vector(0)'
    total_pods_query = 'count(kube_pod_info) or vector(0)'
    running_pods_query = 'count(kube_pod_status_phase{phase="Running"}) or vector(0)'

    cpu_usage = float(get_prometheus_metric(cpu_query))
    mem_usage = float(get_prometheus_metric(mem_query))
    total_pods = int(float(get_prometheus_metric(total_pods_query)))
    running_pods = int(float(get_prometheus_metric(running_pods_query)))

    ai_insight = generate_ai_insight(cpu_usage, mem_usage, running_pods, total_pods)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_emoji = "✅" if cpu_usage < 80 and running_pods == total_pods else "⚠️"

    report_text = f"""
*🚀 [EKS AI Reporter] Infrastructure Analysis*
--------------------------------------------------
*📅 Date:* {now}
*🌐 Status:* {status_emoji} {'Stable' if status_emoji == "✅" else "Warning"}

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
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Slack Error: {e}")

if __name__ == "__main__":
    print("Starting AI Infrastructure Analysis...")
    report = generate_report()
    send_to_slack(report)
    print("Process Finished Successfully!")
