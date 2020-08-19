# Configure addresses
c.KubeController.address = ":8000"
c.KubeController.api_url = 'http://{{ include "dask-gateway.apiName" . }}.{{ .Release.Namespace }}:8000/api'
c.KubeController.gateway_instance = '{{ include "dask-gateway.fullname" . }}'
c.KubeController.proxy_prefix = "{{ .Values.gateway.prefix }}"
c.KubeController.proxy_web_middlewares = [
  {"name": '{{ include "dask-gateway.fullname" . | printf "clusters-prefix-%s" | trunc 63 | trimSuffix "-" }}',
  "namespace": '{{ .Release.Namespace }}'}
]
c.KubeController.log_level = "{{ .Values.controller.loglevel }}"
c.KubeController.completed_cluster_max_age = {{ .Values.controller.completedClusterMaxAge }}
c.KubeController.completed_cluster_cleanup_period = {{ .Values.controller.completedClusterCleanupPeriod }}
c.KubeController.backoff_base_delay = {{ .Values.controller.backoffBaseDelay }}
c.KubeController.backoff_max_delay = {{ .Values.controller.backoffMaxDelay }}
c.KubeController.k8s_api_rate_limit = {{ .Values.controller.k8sApiRateLimit }}
c.KubeController.k8s_api_rate_limit_burst = {{ .Values.controller.k8sApiRateLimitBurst }}
{{- if eq (toString .Values.traefik.service.ports.tcp.port) "web" }}
c.KubeController.proxy_tcp_entrypoint = "web"
