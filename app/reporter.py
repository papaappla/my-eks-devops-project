# -*- coding: utf-8 -*-
import requests
import os
import sys
from datetime import datetime
import google.generativeai as genai

# VERSION: 4.1 (STABLE & STEP-BY-STEP)
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus-kube-prometheus-prometheus.monitoring:9090").strip()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def get_prometheus_metric(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query}, timeout=15)
        response.raise_for_status()
        data = response.json()
        results = data.get('data', {}).get('result', [])
        if results:
            return results[0]['value'][1]
        return "0"
    except Exception as e:
        print(f"Metrics fetch error: {repr(e)}")
        return "0"

def generate_report():
    # 쿼리 단순화 (호환성 우선)
    cpu_q = 'avg(instance:node_cpu_utilization:ratio * 100) or vector(0)'
    mem_q = 'avg(instance:node_memory_utilization:ratio * 100) or vector(0)'
    total_q = 'count(kube_pod_info) or vector(0)'
    running_q = 'count(kube_pod_status_phase{phase="Running"}) or vector(0)'

    cpu = float(get_prometheus_metric(cpu_q))
    mem = float(get_prometheus_metric(mem_q))
    total = int(float(get_prometheus_metric(total_q)))
    running = int(float(get_prometheus_metric(running_q)))

    ai_insight = "AI Analysis Skipped"
    if not GEMINI_API_KEY:
        ai_insight = "Error: GEMINI_API_KEY is Empty"
    else:
        try:
            genai.configure(api_key=GEMINI_API_KEY.strip())
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = (
                f"EKS Status: CPU {cpu:.1f}%, Mem {mem:.1f}%, Pods {running}/{total}. "
                "Give a 1-sentence SRE insight in English. No emojis."
            )
            response = model.generate_content(prompt)
            
            if response and response.text:
                ai_insight = response.text.strip()
            else:
                ai_insight = "AI API: (Empty response)"
        except Exception as e:
            # 유니코드 에러 방지를 위해 repr() 사용
            ai_insight = f"AI API Error: {repr(e)[:100]}"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
*🚀 [EKS AI Reporter V4.1] Analysis*
--------------------------------------------------
*📅 Date:* {now}
*🌐 Status:* {'✅ Stable' if running == total else '⚠️ Warning'}

*📊 Metrics:*
• CPU: {cpu:.2f}%
• Mem: {mem:.2f}%
• Pods: {running} / {total}

*🤖 AI SRE Insight:*
"{ai_insight}"
--------------------------------------------------
"""
    return report

def send_to_slack(text):
    if not SLACK_WEBHOOK_URL:
        return
    try:
        # json= 파라미터가 자동으로 UTF-8 인코딩을 처리합니다.
        requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=10)
    except Exception as e:
        print(f"Slack Error: {repr(e)}")

if __name__ == "__main__":
    report = generate_report()
    send_to_slack(report)
    print(report)
