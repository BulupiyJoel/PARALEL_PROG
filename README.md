# Kubernetes Deployment for Django Blog Project

## Prerequisites
- Docker image for your Django app pushed to a registry (update `yourusername/django-blog:latest` in YAMLs)
- Kubernetes cluster (minikube, kind, or cloud)
- `kubectl` installed and configured

## Deploy Steps

1. **Apply MySQL (with persistent storage):**
   ```sh
   kubectl apply -f mysql-deployment.yaml
   ```
2. **Apply RabbitMQ:**
   ```sh
   kubectl apply -f rabbitmq-deployment.yaml
   ```
3. **Apply phpMyAdmin (optional):**
   ```sh
   kubectl apply -f phpmyadmin-deployment.yaml
   ```
4. **Apply Django Web App:**
   ```sh
   kubectl apply -f django-deployment.yaml
   ```
5. **Apply Celery Worker:**
   ```sh
   kubectl apply -f celery-deployment.yaml
   ```

## Accessing Services
- **Django:** NodePort 30000 (http://<node-ip>:30000)
- **phpMyAdmin:** NodePort 30080 (http://<node-ip>:30080)
- **RabbitMQ UI:** NodePort 15672 (edit YAML to expose if needed)

## Notes
- Update image names as needed.
- For production, use Ingress and Secrets for sensitive data.
- For static/media files, add a PersistentVolume and mount it in Django/Celery deployments. 