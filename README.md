# 🚀 AWS EKS 기반 클라우드 네이티브 & AI 모니터링 프로젝트

이 프로젝트는 온프레미스 엔지니어에서 **AWS/DevOps 엔지니어**로 거듭나기 위한 기술적 여정을 담은 **End-to-End 클라우드 네이티브 아키텍처** 실습 프로젝트입니다. 

기본적인 **IaC(Terraform)** 및 **CI/CD(GitHub Actions)**를 넘어, **Go 언어 기반의 Kubernetes Operator** 개발과 **Gemini 3 Flash AI를 활용한 지능형 모니터링 리포팅 시스템**을 구축하는 것이 핵심입니다.

---

## 🏗️ System Architecture

현재 프로젝트의 아키텍처는 IaC(Terraform)로 구축된 EKS 환경 위에서 **Go 기반 오퍼레이터**와 **AI 기반 모니터링**이 결합된 형태입니다.

```mermaid
graph TD
    subgraph "External Services"
        GAI[Gemini 3 Flash API]
        SLK[Slack Webhook]
        ECR[Amazon ECR]
    end

    subgraph "GitHub Cloud"
        GHA[GitHub Actions]
        GHA -- "1. Build & Push" --> ECR
        GHA -- "2. Deploy & Recovery" --> EKS
    end

    subgraph "AWS EKS (ap-northeast-2)"
        direction TB
        EKS["EKS Cluster (portfolio-cluster)"]
        
        subgraph "Monitoring Layer"
            PROM[Prometheus]
            GRAF[Grafana]
        end
        
        subgraph "Application Layer"
            API[FastAPI Server]
            OPT[Status Operator (Go)]
        end
        
        subgraph "AI Reporting Layer"
            CJ[AI Reporter CronJob]
        end
    end

    %% Flow
    PROM -- "Collect Metrics" --> API
    PROM -- "Collect Metrics" --> OPT
    CJ -- "Query Data" --> PROM
    CJ -- "Analyze Metrics" --> GAI
    GAI -- "Generate Insight" --> CJ
    CJ -- "Post Report" --> SLK
    GRAF -- "Visualize" --> PROM
```

---

## 🌟 Key Features

### 1. 지능형 AI 관측성 (AI Observability)
- **Gemini 3 Flash 연동**: Prometheus에서 수집한 실시간 메트릭 데이터를 AI가 분석하여 SRE 관점의 인사이트를 생성합니다.
- **자동 리포팅**: 매일 아침 9시(KST) Kubernetes CronJob이 실행되어 분석 결과와 시스템 건강 상태를 Slack으로 자동 전송합니다.

### 2. Go 기반 Kubernetes Operator
- **Custom Controller**: `StatusDashboard`라는 CRD(Custom Resource Definition)를 정의하고, 클러스터 상태를 선언적으로 관리하는 오퍼레이터를 Go 언어로 직접 개발하였습니다.
- **Status Management**: 리소스의 상태를 감시하고 조율하는 Reconciliation Loop 로직을 구현하였습니다.

### 3. 완전 자동 복구 (Auto Infra Recovery)
- **버튼 하나로 복구**: 비용 절감을 위해 인프라를 삭제(`Destroy`)한 후 다시 생성(`Apply`)했을 때, Helm 차트, Secret, AI Reporter 등을 한 번에 정상화하는 전용 GitHub Actions 워크플로우를 구축하였습니다.

### 4. 실무 수준의 보안 및 IaC
- **Secret Management**: API Key, Webhook URL 등 민감 정보를 K8s Secret으로 관리하고, GitHub Push Protection을 통해 보안 사고를 사전에 방지합니다.
- **Modular IaC**: Terraform을 통해 네트워크(VPC)부터 클러스터(EKS), 저장소(ECR)까지 전 과정을 코드로 표준화하였습니다.

---

## 🛠️ Tech Stack

- **Cloud Platform**: AWS (EKS, ECR, VPC, IAM)
- **Infrastructure**: Terraform (IaC)
- **Languages**: Go (Operator), Python (API & AI Reporter)
- **Observability**: Prometheus, Grafana, Gemini 3 Flash
- **CI/CD**: GitHub Actions, Helm
- **Bot Interface**: Slack Incoming Webhooks

---

## 🚀 Quick Start

### 1. 인프라 구축
```bash
terraform init
terraform apply -auto-approve
```

### 2. 자동 복구 및 앱 배포
1. GitHub 저장소의 `Actions` 탭으로 이동합니다.
2. `Auto Infra Recovery` 워크플로우를 실행하여 모든 모니터링 인프라와 앱을 배포합니다.

### 3. 모니터링 확인
```bash
# Grafana 접속 (비밀번호: admin)
kubectl port-forward deployment/prometheus-grafana -n monitoring 3000:3000
```

---

## 📁 Project Structure
```text
.
├── .github/workflows/      # CI/CD 및 자동 복구 워크플로우
├── app/                    # FastAPI 서버 및 AI Reporter (Python)
├── charts/                 # Helm Charts (K8s Manifests)
├── operators/              # Go 기반 Kubernetes Operator
├── terraform/              # Infrastructure as Code (VPC, EKS)
└── docs/                   # 가이드 및 체크리스트 (Recovery, Operator 등)
```
