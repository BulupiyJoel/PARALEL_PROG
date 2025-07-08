# Déploiement Kubernetes pour Django + Celery + MySQL + RabbitMQ

## Déploiement
```sh
kubectl apply -f mysql-deployment.yaml
kubectl apply -f rabbitmq-deployment.yaml
kubectl apply -f phpmyadmin-deployment.yaml   # optionnel
kubectl apply -f media-pvc.yaml
kubectl apply -f django-deployment.yaml
kubectl apply -f celery-deployment.yaml
```

## Accès
- Django : http://<minikube-ip>:30000
- phpMyAdmin : http://<minikube-ip>:30081

## Commandes utiles
- Migrations : `kubectl exec -it deployment/django-web -- python manage.py migrate`
- Superuser : `kubectl exec -it deployment/django-web -- python manage.py createsuperuser`
- Logs : `kubectl logs deployment/django-web`

## Remarques
- Le volume media est partagé entre Django et Celery.
- Pour la production, utilisez des Secrets pour les mots de passe. 