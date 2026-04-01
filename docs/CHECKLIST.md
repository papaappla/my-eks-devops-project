# ✅ Comprehensive Technical Gap & Roadmap Checklist

본 프로젝트를 기반으로 **금융/플랫폼**, **AI 서비스**, **전통적 인프라/IoT** 등 다양한 기술 선도 기업의 요구사항에 도달하기 위한 기술적 공백 점검표입니다.

---

## 🏗️ 1. Cloud Infrastructure & Platform (Multi-Cloud/IaC)
| 상태 | 항목 | 상세 내용 및 기술적 요구사항 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **AWS EKS 운영** | 클러스터/노드 그룹 구축, 장애 대응 및 온콜(On-call) 핸들링 | `eks.tf` |
| ✅ | **Terraform IaC** | HCL 기반 인프라 표준화 및 재사용 가능한 모듈 설계 | `vpc.tf`, `eks.tf` |
| ⬜ | **ECS 기반 서비스** | ECS Cluster, Task Definition, Service 운영 및 관리 | - |
| ⬜ | **Multi-Cloud (NCP)** | NCP(Naver Cloud) 인프라 설계 및 AWS와의 멀티 클라우드 연동 | - |
| ⬜ | **OpenStack** | IaaS 플랫폼 자체의 설계/개발 및 OpenStack 기반 인프라 운영 | - |
| ⬜ | **Multi-Account** | Organizations 기반 멀티 AWS 계정 표준화 및 운영 정책 수립 | - |
| ✅ | **Core Resources** | **EC2, S3, RDS, Redis** 등 핵심 리소스 운영 및 최적화 | `eks.tf` |
| ⬜ | **FinOps** | 리소스 분석을 통한 비용 최적화 및 FinOps 정책 적용 | - |

---

## 💻 2. Systems Programming & Inhouse Development
| 상태 | 항목 | 상세 내용 및 기술적 요구사항 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **Python 숙련도** | FastAPI 비동기 프로그래밍 및 운영 자동화 툴 개발 | `main.py` |
| ✅ | **Golang/C 숙련도** | 고성능/저수준 시스템 프로그래밍 및 오픈소스 기능 확장 | - |
| ⬜ | **Inhouse Dev** | 오픈소스를 기반으로 사내 환경에 맞춘 기능 확장 및 성능 최적화 | - |
| ✅ | **REST API Design** | 리소스 중심 API 설계 및 API 응답 속도 최적화 | `main.py` |
| ⬜ | **OS/Kernel/Storage** | Linux 커널 아키텍처, 프로세스 스케줄링, 분산 스토리지(Ceph 등) 전문성 | - |
| ⬜ | **Deep Networking** | L4/L7 LB, BGP, VXLAN, eBPF 등 클라우드 네트워크 심화 지식 | - |

---

## 🤖 3. AI Service Interface & UX (Frontend/Backend Integration)
| 상태 | 항목 | 상세 내용 및 기술적 요구사항 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ⬜ | **Real-time Interface** | **SSE, WebSocket** 기반 실시간 데이터/AI 답변 스트리밍 구현 | - |
| ⬜ | **AI Agent Integration** | **MCP(Model Context Protocol), A2A** 연계 및 멀티 에이전트 구조 설계 | - |
| ⬜ | **BFF Architecture** | Frontend 최적화를 위한 BFF 계층 설계 및 경량 백엔드 구현 | - |
| ⬜ | **Bot Interface** | **Slack Bot (Slack Bolt SDK)** 기반 멀티 플랫폼 인터페이스 개발 | - |
| ⬜ | **Admin Tool/CMS** | Context DB 관리용 웹 인터페이스 및 AI 운영 도구 설계 | - |
| ⬜ | **UX Optimization** | 응답 지연 처리, 실패/재시도 UX 설계 및 AI 결과 시각화 | - |

---

## 📊 4. Data Engineering & Statistical Analysis
| 상태 | 항목 | 상세 내용 및 기술적 요구사항 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ⬜ | **Database Transaction** | ACID 트랜잭션의 깊은 이해 및 대규모 트래픽 동시성 제어 | - |
| ⬜ | **SQL & Statistics** | 복잡한 쿼리 작성 및 서비스 데이터 통계/분석 (SQL 전문성) | - |
| ✅ | **Data Collection** | 플랫폼 관리 및 상태 모니터링을 위한 데이터 수집 자동화 | `main.py` |

---

## 🚀 5. DevOps, Security & Observability
| 상태 | 항목 | 상세 내용 및 기술적 요구사항 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **GitHub Actions** | SaaS 기반 CI/CD 구축 및 배포 환경 관리 | `.github/workflows/` |
| ✅ | **Helm Charts** | K8s 리소스 패키징 및 선언적 배포 관리 | `my-api-chart/` |
| ⬜ | **ArgoCD** | GitOps 기반의 선언적 지속적 배포(CD) 환경 구축 | - |
| ⬜ | **Access Control** | **Okta, Keycloak (SSO/EAM)** 연동 및 권한 분리/접근제어 | - |
| ✅ | **Observability** | **Prometheus, Grafana, ELK/OpenSearch** 기반 가시성 확보 | `monitoring/`, `monitor.yaml` |
| ⬜ | **Security Automation** | DevOps 관점의 보안 정책 수립 및 운영 자동화 | - |

---

## 📈 Roadmap (Technical Gap Resolution)

### 🔴 Phase 1: 플랫폼 개발 및 고수준 시스템 역량 (Infrastructure Dev)
- [x] **Golang/C 연마**: K8s 커스텀 컨트롤러(Operator) 개발 및 오픈소스 기여. (Status Operator 초기화 완료)
- [ ] **OpenStack/IaaS 탐구**: 클라우드 플랫폼 자체의 아키텍처 분석 및 가상화 제어 실습.
- [ ] **OS/Network 심화**: Linux 커널 파라미터 튜닝 및 eBPF 기반 네트워크 가시성 확보.

### 🔵 Phase 2: AI 인터페이스 및 실시간성 (Application Dev)
- [ ] **실시간 통신**: FastAPI SSE를 활용한 AI 스트리밍 서비스 및 Slack Bot 연동.
- [ ] **BFF & CMS**: 프론트엔드 요구사항에 맞춰 여러 인프라 API를 취합해 전달하는 BFF 계층 구축.
- [ ] **프로토콜 연계**: MCP, A2A 등 최신 AI 상호작용 프로토콜 연구 및 적용.

### 🟢 Phase 3: 데이터 분석 및 보안/운영 최적화 (SRE/SecOps)
- [ ] **데이터 통계**: 인프라 메트릭 데이터를 SQL로 분석하여 가용성 보고서 자동 생성.
- [ ] **SSO 연동**: Keycloak 등을 활용한 통합 인증(EAM) 및 정교한 RBAC 시스템 구축.
- [ ] **ArgoCD & Observability**: Helm + ArgoCD 기반 GitOps 완성 및 통합 대시보드 구축.
