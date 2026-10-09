# Minimal container build example

This small HTTP service demonstrates container interfaces only. Use a production application server and structured logging in real services.

```bash
docker build --tag local/web:dev .
docker image inspect local/web:dev
docker run --rm --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --user 10001:10001 --publish 127.0.0.1:18080:8080 local/web:dev
curl --fail http://127.0.0.1:18080/healthz
```

The port is bound to loopback for the lab. Before production, use a patched and pinned base, lock dependencies, create an SBOM/provenance, scan the image, push to a private registry, and deploy by digest. Set resource limits in the orchestrator and inject secrets at runtime.
