provider "kubernetes" {
  config_context = "minikube"
}

provider "kubernetes-alpha" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

resource "kubernetes_namespace" "main" {
  metadata {
    name = var.namespace
  }
}

module "traefik" {
  source = "../traefik"

  name      = var.prefix
  namespace = var.namespace

  depends_on = [
    kubernetes_namespace.main
  ]
}

module "conda-store" {
  source = "../conda-store"

  name      = var.prefix
  namespace = var.namespace

  depends_on = [
    kubernetes_namespace.main
  ]
}

module "jupyterhub" {
  source = "../jupyterhub"

  name      = var.prefix
  namespace = var.namespace

  services = [
    "dask_gateway"
  ]

  extraConfig = file("${path.module}/files/jupyterhub_config.py")

  depends_on = [
    kubernetes_namespace.main
  ]
}

module "dask-gateway" {
  source = "../dask-gateway"

  name      = var.prefix
  namespace = var.namespace

  jupyterhub_api_token = module.jupyterhub.api_tokens.dask_gateway
  jupyterhub_api_url   = "${module.jupyterhub.internal_proxy_url}/hub/api"

  depends_on = [
    kubernetes_namespace.main,
    module.jupyterhub
  ]
}
