# Docker for DevOps

## Mental model

An image is a layered, mostly immutable filesystem plus metadata; a container is an isolated process created from an image. Containers share the host kernel, so they are not equivalent to virtual machines. Registries store images, while orchestration platforms manage placement and lifecycle.

## Build and run

Use a small, trusted base image, pin dependencies, and use a multi-stage build to keep compilers and build tools out of runtime images. Add a `.dockerignore` so local secrets, Git history, and irrelevant files never enter the build context. Run as a non-root user, define a clear entry point, and expose only required ports. Pass configuration at runtime; do not bake credentials into image layers or build arguments.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --chown=10001:10001 . .
USER 10001
CMD ["python", "app.py"]
```

Prefer exec-form `CMD`/`ENTRYPOINT` so signals reach the application. Set resource limits in the runtime platform, add health checks where meaningful, and send logs to stdout/stderr. Use explicit networks and named volumes when persistence is needed.

## Security and reliability

Scan dependencies and images, generate provenance/SBOM where supported, and promote the same immutable digest between environments. Rebuild regularly for patched base images. Avoid mounting the Docker socket into untrusted containers; it grants powerful host control. Understand that tags can move—use digests for reproducibility.

## Practice

Containerize a service with a multi-stage build, non-root runtime, health endpoint, and externalized configuration. Inspect its layers, test graceful shutdown, rebuild after a base-image update, and verify the image contains no credentials.

## Further reading

[Docker documentation](https://docs.docker.com/)
