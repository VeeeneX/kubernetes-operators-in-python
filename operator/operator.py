import kopf
import base64
from kubernetes import client

@kopf.on.create('pyvo.io', 'v1', 'agesecrets')
def on_create(spec, namespace, **kwargs):
    secret_name = spec.get('secretName')
    secret_key = spec.get('secretKey')
    secret_value = spec.get('secret')
    # Here we need to add custom logic for decrypting that secret
    # After that new secret in Kubernetes can be created
    # todo: Implement decrypting logic
    # todo: Implement creation of native Kubernetes secret


@kopf.on.delete('pyvo.io', 'v1', 'agesecrets')
def on_delete(spec, namespace, **kwargs):
    secret_name = spec.get('secretName')
    # todo: Delete k8s secret, when reference is deleted
