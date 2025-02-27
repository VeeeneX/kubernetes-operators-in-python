group "default" {
    targets = ["app"]
}

variable "TAG" {
    default = "latest"
}

target "app" {
    context = "./app"
    dockerfile = "Dockerfile"
    tags = ["app:${TAG}"]
}
