/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"fmt"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"

	infrav1alpha1 "infra.local/status-operator/api/v1alpha1"
)

// StatusDashboardReconciler reconciles a StatusDashboard object
type StatusDashboardReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=infra.infra.local,resources=statusdashboards,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=infra.infra.local,resources=statusdashboards/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=infra.infra.local,resources=statusdashboards/finalizers,verbs=update
// +kubebuilder:rbac:groups="",resources=nodes,verbs=get;list;watch

func (r *StatusDashboardReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// 1. StatusDashboard 인스턴스 가져오기
	var statusDashboard infrav1alpha1.StatusDashboard
	if err := r.Get(ctx, req.NamespacedName, &statusDashboard); err != nil {
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	logger.Info("상태판 갱신 중...", "name", statusDashboard.Name)

	// 2. 실제 노드(Node) 목록 조회
	var nodeList corev1.NodeList
	if err := r.List(ctx, &nodeList); err != nil {
		logger.Error(err, "노드 목록을 가져오는 데 실패했습니다.")
		return ctrl.Result{}, err
	}

	// 3. 노드 상태 분석
	nodeCount := len(nodeList.Items)
	readyNodes := 0
	for _, node := range nodeList.Items {
		for _, condition := range node.Status.Conditions {
			if condition.Type == corev1.NodeReady && condition.Status == corev1.ConditionTrue {
				readyNodes++
			}
		}
	}

	// 4. 상태 메시지 구성
	overallHealth := "Healthy"
	if readyNodes < nodeCount {
		overallHealth = "Warning"
	}

	statusDashboard.Status.OverallHealth = overallHealth
	now := metav1.Now()
	statusDashboard.Status.LastUpdated = &now
	statusDashboard.Status.ComponentStatuses = []infrav1alpha1.ComponentStatus{
		{
			Name:    "EKS Cluster",
			Status:  overallHealth,
			Message: fmt.Sprintf("현재 %d개 노드 중 %d개가 Ready 상태입니다.", nodeCount, readyNodes),
		},
		{
			Name:    "VPC",
			Status:  "Healthy",
			Message: "Subnets and Gateways are active (Mock)",
		},
	}

	// 5. 상태 업데이트
	if err := r.Status().Update(ctx, &statusDashboard); err != nil {
		logger.Error(err, "StatusDashboard 상태 업데이트 실패")
		return ctrl.Result{}, err
	}

	// 6. 설정된 주기마다 재실행
	interval := statusDashboard.Spec.RefreshIntervalSeconds
	if interval <= 0 {
		interval = 10 // 기본 10초
	}

	return ctrl.Result{RequeueAfter: time.Duration(interval) * time.Second}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *StatusDashboardReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&infrav1alpha1.StatusDashboard{}).
		Complete(r)
}
