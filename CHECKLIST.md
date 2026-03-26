# ✅ Job Requirement Match & Project Checklist

본 프로젝트가 주요 기업(토스, 넥슨, 헤리트 등)의 채용 공고 요구사항과 얼마나 일치하는지 점검한 체크리스트입니다.

---

## 🏗️ 1. Cloud Infrastructure (AWS/IaC)
| 상태 | 항목 | 상세 내용 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **AWS EKS 운영** | EKS 클러스터 및 노드 그룹 구축 및 운영 | `eks.tf` |
| ✅ | **Terraform 기반 IaC** | VPC, Subnet, IGW 등 인프라 전체 코드화 | `vpc.tf`, `eks.tf` |
| ✅ | **VPC/Network 설계** | 멀티 AZ 서브넷 배치 및 라우팅 테이블 구성 | `vpc.tf` |
| ✅ | **IAM/RBAC 권한 관리** | 최소 권한 원칙 기반 IAM Role 및 K8s RBAC 적용 | `rbac.yaml`, `eks.tf` |
| ⬜ | **Database 운영** | RDS, Redis 구축 및 운영 경험 (Next Step) | - |
| ⬜ | **멀티 클라우드/계정** | NCP 연동 또는 AWS Multi-Account 환경 (Next Step) | - |

---

## 🚀 2. CI/CD & DevOps Automation
| 상태 | 항목 | 상세 내용 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **GitHub Actions** | Build -> Push -> Deploy 전 과정 자동화 파이프라인 | `.github/workflows/` |
| ✅ | **Helm Charts** | K8s 리소스 패키징 및 환경 변수 주입 자동화 | `my-api-chart/` |
| ✅ | **Containerization** | Docker를 활용한 어플리케이션 이미지 최적화 | `Dockerfile` |
| ⬜ | **ArgoCD (GitOps)** | Declarative CD 환경 구성 (Next Step) | - |
| ⬜ | **Observability** | Prometheus, Grafana, ELK 기반 모니터링 (Next Step) | - |

---

## 🐍 3. Development & Automation (Python/API)
| 상태 | 항목 | 상세 내용 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **Python 스크립트** | K8s API 연동 및 운영 자동화 툴 개발 | `main.py` |
| ✅ | **REST API 개발** | FastAPI 기반의 인프라 정보 조회 인터페이스 구현 | `main.py` |
| ✅ | **YAML/Bash 활용** | 배포 Manifest 설계 및 스크립트 기반 자동화 | `deploy.yml` |
| ⬜ | **AI Integration** | LLM 연동 및 AI DevOps Assistant 기능 (In Progress) | - |

---

## 🛠️ 4. Problem Solving & Experience (Soft Skills)
| 상태 | 항목 | 상세 내용 | 관련 파일 |
| :---: | :--- | :--- | :--- |
| ✅ | **장애 대응 및 디버깅** | InvalidImageName, RBAC 권한 오류 등 실전 해결 기록 | `디버깅3단계` |
| ✅ | **운영 프로세스 문서화** | 인프라 구조 및 배포 절차 정리 | `README.md` |
| ✅ | **현대화(Modernization)** | 온프레미스에서 클라우드 네이티브로의 전환 과정 | `진행상황` |

---

## 🎯 면접 핵심 키워드 (Matching)
- **토스**: "Cloud Native 관점의 문제 해결", "EKS 클러스터 운영", "Terraform IaC"
- **넥슨**: "AI 활용 기반 구축", "Python 숙련도", "Kubernetes에 대한 깊은 이해"
- **헤리트**: "데이터 수집 자동화 툴 개발", "Linux/Network 이해", "Docker/Container"

---

## 📈 Roadmap (Next Step)
- [ ] **Database**: Terraform으로 `RDS(PostgreSQL)` 및 `ElastiCache(Redis)` 추가
- [ ] **Observability**: Helm으로 `Prometheus` & `Grafana` 스택 배포 및 대시보드 구성
- [ ] **AI Assistant**: OpenAI API 연동하여 Pod Error Log 분석 기능 추가 (넥슨 AI Hub 타겟)
