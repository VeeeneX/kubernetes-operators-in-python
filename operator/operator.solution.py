
import kopf
import base64
from kubernetes import client
from pyrage import decrypt, x25519

def create_k8s_secret(name, namespace, key, value):
    api = client.CoreV1Api()
    secret = client.V1Secret(
        metadata=client.V1ObjectMeta(name=name),
        data={key: base64.b64encode(value.encode()).decode('ascii')},
        # https://kubernetes.io/docs/concepts/configuration/secret/#secret-types
        type="Opaque"
    )
    api.create_namespaced_secret(namespace, body=secret)

def read_age_secret(name, namespace):
    api = client.CoreV1Api()
    secret = api.read_namespaced_secret(name, namespace)
    decoded_data = {key: base64.b64decode(value).decode('utf-8') for key, value in secret.data.items()}
    return decoded_data

def decrypt_secret(ageSecretRef, namespace, secret_value):
    data = read_age_secret(ageSecretRef, namespace)
    decrypting_secret = None
    if "secretKey" in data:
        decrypting_secret = x25519.Identity.from_str(data["secretKey"])
    else:
        pass

    if "ENC[" in secret_value:
        secret_value = secret_value[4:-1]
    else:
        pass

    encrypted_secret = base64.b64decode(secret_value)
    decrypted = decrypt(encrypted_secret, [decrypting_secret])
    return decrypted.decode()

@kopf.on.create('pyvo.io', 'v1', 'agesecrets')
def on_create(spec, namespace, **kwargs):
    secret_name = spec.get('secretName')
    secret_key = spec.get('secretKey')
    secret_value = spec.get('secret')
    # Here we need to add custom logic for decrypting that secret
    # After that new secret in Kubernetes can be created
    # todo: Implement decrypting logic
    # todo: Implement creation of native Kubernetes secret

    decrypted_secret = decrypt_secret(spec.get("ageSecretRef"), namespace, secret_value)
    create_k8s_secret(secret_name, namespace, secret_key, decrypted_secret)


def delete_k8s_secret(name, namespace):
    try:
        api = client.CoreV1Api()
        api.delete_namespaced_secret(name, namespace)
    except client.exceptions.ApiException:
        pass

@kopf.on.delete('pyvo.io', 'v1', 'agesecrets')
def on_delete(spec, namespace, **kwargs):
    secret_name = spec.get('secretName')
    delete_k8s_secret(secret_name, namespace)
    
