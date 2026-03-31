# 🚀 Kubernetes Status Operator 가이드

이 가이드는 Go 언어로 작성된 Custom Controller(Operator)인 `status-operator`의 구조와 사용 방법을 설명합니다.

---

## 1. 개요 (What is an Operator?)

Kubernetes Operator는 **"특정 리소스의 상태를 지속적으로 감시하고, 원하는 상태(Desired State)로 유지하려는 무한 루프 프로그램"**입니다.

이 프로젝트의 `status-operator`는 `StatusDashboard`라는 커스텀 리소스를 감시하며, 인프라(EKS, VPC 등)의 상태 정보를 수집하여 리소스의 `status` 필드에 업데이트해주는 역할을 합니다.

---

## 2. 프로젝트 구조 (Project Structure)

Kubebuilder로 생성된 이 프로젝트의 핵심 파일들은 다음과 같습니다:

- **`api/v1alpha1/statusdashboard_types.go`**: 
  - 우리가 정의한 `StatusDashboard` 리소스의 데이터 구조체(Schema)가 정의되어 있습니다.
  - `Spec`: 사용자가 설정하는 값 (예: 갱신 주기)
  - `Status`: 오퍼레이터가 채워넣는 값 (예: 현재 상태, 마지막 업데이트 시간)

- **`internal/controller/statusdashboard_controller.go`**: 
  - **가장 중요한 로직**이 들어있는 곳입니다. 
  - `Reconcile` 함수가 주기적으로 실행되며, 클러스터의 상태를 확인하고 `Status` 필드를 업데이트합니다.

- **`config/samples/`**: 
  - 실제로 리소스를 생성할 때 사용할 예시 YAML 파일들이 들어있습니다.

---

## 3. 사전 준비 (Prerequisites)

이 오퍼레이터를 실행하려면 다음이 필요합니다:
1.  **Go 1.24.1+** (설치 완료)
2.  **Kubebuilder 4.0.0** (설치 완료)
3.  **동작 중인 Kubernetes 클러스터** (EKS 등)
4.  **kubectl** (클러스터에 연결된 상태)

---

## 4. 실행 및 테스트 방법 (Step-by-Step)

모든 명령은 `operators/status-operator/` 디렉토리 내에서 실행합니다.

### 1단계: CRD 설치 (K8s에게 알려주기)
Kubernetes가 `StatusDashboard`라는 새로운 언어를 알아들을 수 있게 정의(Custom Resource Definition)를 설치합니다.
```bash
make install
```

### 2단계: 오퍼레이터 실행 (로컬 모드)
실제 Go 프로그램을 실행합니다. 이 프로그램은 클러스터의 API 서버와 통신하며 리소스를 감시합니다.
```bash
# 별도의 터미널 세션에서 실행 권장
export PATH=$PATH:/usr/local/go/bin
make run
```

### 3단계: 샘플 리소스 생성
오퍼레이터가 감시할 대상(인스턴스)을 하나 만듭니다.
```bash
# 새 터미널에서 실행
kubectl apply -f config/samples/infra_v1alpha1_statusdashboard.yaml
```

### 4단계: 결과 확인
오퍼레이터가 리소스의 `status` 필드를 정상적으로 업데이트했는지 확인합니다.
```bash
kubectl get statusdashboard main-dashboard -o yaml
```

출력 결과 중 아래와 같은 부분이 있다면 성공입니다!
```yaml
status:
  overallHealth: Healthy
  lastUpdated: "2026-03-31T09:20:00Z"
  componentStatuses:
  - name: EKS Cluster
    status: Healthy
    message: All nodes are ready
```

---

## 5. 주요 Go 문법 팁 (For Beginners)

- **`if err != nil { ... }`**: Go에서는 함수 실행 후 에러가 발생했는지 항상 체크하는 것이 관례입니다.
- **`Reconcile` 함수**: 이 함수는 리소스가 생성/수정/삭제될 때마다 호출됩니다. 또한 코드 끝에 `RequeueAfter`를 설정하여 정해진 시간마다 강제로 다시 실행되게 할 수 있습니다.
- **`logger.Info`**: 오퍼레이터가 현재 무엇을 하고 있는지 로그를 남길 때 사용합니다. `make run`을 실행 중인 터미널에서 확인할 수 있습니다.

---

## 6. 다음 단계 제안
현재는 고정된 "Healthy" 데이터만 보여주고 있습니다. `internal/controller/statusdashboard_controller.go` 코드를 수정하여 실제 클러스터의 Node 개수나 Pod 상태를 조회하는 로직을 추가해 보세요!

---

## 7. 부록: EKS 클러스터 연결 설정 (Troubleshooting)

`kubectl` 실행 시 `Service Unavailable` 에러가 발생하거나 클러스터 연결이 끊긴 경우 아래 단계를 따르세요.

### 1단계: 클러스터 이름 확인
Terraform으로 생성된 클러스터 이름을 확인합니다.
```bash
# terraform 디렉토리에서 실행
terraform output cluster_name
# 또는 AWS CLI로 전체 목록 조회
aws eks list-clusters --region ap-northeast-2
```

### 2단계: kubeconfig 업데이트
확인된 클러스터 이름을 사용하여 로컬의 인증 정보를 갱신합니다.
```bash
aws eks update-kubeconfig --region ap-northeast-2 --name <클러스터_이름>
```

### 3단계: 연결 확인
```bash
kubectl get nodes
```
노드 목록이 정상적으로 출력되면 오퍼레이터를 실행할 준비가 된 것입니다.
