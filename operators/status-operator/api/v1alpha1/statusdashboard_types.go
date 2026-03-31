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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// StatusDashboardSpec defines the desired state of StatusDashboard
type StatusDashboardSpec struct {
	// RefreshIntervalSeconds defines how often the operator should refresh the status
	RefreshIntervalSeconds int `json:"refreshIntervalSeconds,omitempty"`
}

// ComponentStatus defines the status of an individual infrastructure component
type ComponentStatus struct {
	Name    string `json:"name"`
	Status  string `json:"status"`
	Message string `json:"message,omitempty"`
}

// StatusDashboardStatus defines the observed state of StatusDashboard
type StatusDashboardStatus struct {
	// OverallHealth can be Healthy, Warning, or Critical
	OverallHealth string `json:"overallHealth,omitempty"`

	// LastUpdated is the last time the dashboard was updated
	LastUpdated *metav1.Time `json:"lastUpdated,omitempty"`

	// ComponentStatuses lists the status of each monitored component
	ComponentStatuses []ComponentStatus `json:"componentStatuses,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// StatusDashboard is the Schema for the statusdashboards API
type StatusDashboard struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   StatusDashboardSpec   `json:"spec,omitempty"`
	Status StatusDashboardStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// StatusDashboardList contains a list of StatusDashboard
type StatusDashboardList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []StatusDashboard `json:"items"`
}

func init() {
	SchemeBuilder.Register(&StatusDashboard{}, &StatusDashboardList{})
}
