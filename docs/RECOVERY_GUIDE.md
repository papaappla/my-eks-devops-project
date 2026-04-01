# 🔄 인프라 재구축 및 복구 가이드 (Recovery Guide)

비용 절감을 위해 `terraform destroy` 후 다시 `terraform apply`를 수행했을 때, 시스템을 정상화하기 위한 필수 체크리스트입니다.

---

## 1. 클러스터 접속 복구 (Local & CI/CD)
EKS 클러스터가 재생성되면 API Endpoint 주소가 변경됩니다.

*   **로컬 접속 갱신:**
    ```bash
    aws eks update-kubeconfig --region ap-northeast-2 --name portfolio-cluster
    ```
*   **GitHub Actions 확인:**
    `deploy.yml`은 `aws eks update-kubeconfig`를 매번 수행하므로 별도의 수정이 필요 없으나, AWS IAM 사용자의 권한이 유지되고 있는지 확인이 필요합니다.

---

## 2. 필수 모니터링 인프라 재설치
Terraform으로 관리되지 않는 Helm 차트들을 다시 설치해야 합니다.

*   **Prometheus & Grafana 설치:**
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    kubectl create namespace monitoring
    helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --set grafana.adminPassword=admin
    ```

---

## 3. 민감 정보(Secrets) 재등록
`destroy` 시 클러스터 내부의 Secret 데이터도 모두 삭제됩니다. AI 리포터 작동을 위해 다시 생성해야 합니다.

*   **Slack Webhook Secret:**
    ```bash
    kubectl create secret generic slack-secret \
      --from-literal=webhook-url="YOUR_SLACK_WEBHOOK_URL" \
      -n monitoring
    ```
*   **Gemini API Key Secret:**
    ```bash
    kubectl create secret generic gemini-secret \
      --from-literal=api-key="YOUR_GEMINI_API_KEY" \
      -n monitoring
    ```

---

## 4. 애플리케이션 및 자동화 도구 배포
이미 빌드된 이미지가 ECR에 남아있으므로, Helm과 YAML 적용만 수행하면 됩니다.

*   **API 서버 배포 (Helm):**
    GitHub Actions에서 `Workflow Dispatch`를 실행하거나 로컬에서 직접 배포합니다.
    ```bash
    helm upgrade --install my-api ./charts/my-api-chart
    ```
*   **AI 리포터 CronJob 등록:**
    ```bash
    kubectl apply -f app/reporter-cronjob.yaml
    ```
*   **Operator CRD 및 모니터링 연동:**
    ```bash
    kubectl apply -f operators/status-operator/config/crd/bases/
    kubectl apply -f operators/status-operator/config/prometheus/monitor.yaml
    ```

---

## 💡 복구 확인 체크리스트
- [ ] `kubectl get nodes` 결과가 `Ready`인가?
- [ ] `kubectl get pods -n monitoring`에서 Prometheus가 모두 `Running`인가?
- [ ] `kubectl get cronjob -n monitoring`에 `ai-infra-reporter`가 등록되었는가?
- [ ] Grafana 접속이 가능한가? (Port-forward 또는 LoadBalancer 설정 확인)
