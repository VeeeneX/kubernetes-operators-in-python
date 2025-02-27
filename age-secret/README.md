# Age Secret

Tool that encrypts and decrypts yaml files in this format:

```yaml
apiVersion: pyvo.io/v1
kind: AgeSecret
metadata:
  name: my-secret
spec:
  secretKey: numbers
  secret: "Hello world"
```

## Encrypt 🔒

```shell
uv run age.py encrypt --file decrypted.example.yaml \
  -r age1rmupn8vj5ykfp33w9ln8dp58u899j3n6wj527yueul2twrl55s7qy2m26t \
  -r age1rmupn8vj5ykfp33w9ln8dp58u899j3n6wj527yueul2twrl55s7qy2m26t

# To save output use >

uv run age.py encrypt --file decrypted.example.yaml \
  -r age1rmupn8vj5ykfp33w9ln8dp58u899j3n6wj527yueul2twrl55s7qy2m26t \
  -r age1rmupn8vj5ykfp33w9ln8dp58u899j3n6wj527yueul2twrl55s7qy2m26t > encrypted.example.yaml
```

## Decrypt 🔓

```shell
uv run age.py decrypt --file encrypted.example.yaml -k "AGE-..."
```
