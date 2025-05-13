#!/bin/bash

# Variables
BACKEND_ECR_REPOSITORY_NAME="monitoria-backend"
FRONTEND_ECR_REPOSITORY_NAME="monitoria-frontend"
BACKEND_ECR_REPOSITORY_URI="tu-cuenta.dkr.ecr.us-east-1.amazonaws.com/$BACKEND_ECR_REPOSITORY_NAME"
FRONTEND_ECR_REPOSITORY_URI="tu-cuenta.dkr.ecr.us-east-1.amazonaws.com/$FRONTEND_ECR_REPOSITORY_NAME"
CLUSTER_NAME="monitoria-cluster"
BACKEND_SERVICE_NAME="monitoria-backend-service"
FRONTEND_SERVICE_NAME="monitoria-frontend-service"
REGION="us-east-1"

# Login a ECR
echo "Iniciando sesión en ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $BACKEND_ECR_REPOSITORY_URI
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $FRONTEND_ECR_REPOSITORY_URI

# Construir y subir la imagen del backend
echo "Construyendo y subiendo la imagen del backend..."
cd ..
docker build -t $BACKEND_ECR_REPOSITORY_NAME .
docker tag $BACKEND_ECR_REPOSITORY_NAME:latest $BACKEND_ECR_REPOSITORY_URI:latest
docker push $BACKEND_ECR_REPOSITORY_URI:latest

# Construir y subir la imagen del frontend
echo "Construyendo y subiendo la imagen del frontend..."
cd frontend
docker build -t $FRONTEND_ECR_REPOSITORY_NAME .
docker tag $FRONTEND_ECR_REPOSITORY_NAME:latest $FRONTEND_ECR_REPOSITORY_URI:latest
docker push $FRONTEND_ECR_REPOSITORY_URI:latest

# Actualizar la definición de tarea del backend
echo "Actualizando la definición de tarea del backend..."
cd ../backend
TASK_DEFINITION=$(aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json)
TASK_REVISION=$(echo $TASK_DEFINITION | jq -r '.taskDefinition.revision')

# Actualizar el servicio del backend
echo "Actualizando el servicio del backend..."
aws ecs update-service --cluster $CLUSTER_NAME --service $BACKEND_SERVICE_NAME --task-definition monitoria-backend:$TASK_REVISION --force-new-deployment

# Actualizar la definición de tarea del frontend
echo "Actualizando la definición de tarea del frontend..."
cd ../frontend
TASK_DEFINITION=$(aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json)
TASK_REVISION=$(echo $TASK_DEFINITION | jq -r '.taskDefinition.revision')

# Actualizar el servicio del frontend
echo "Actualizando el servicio del frontend..."
aws ecs update-service --cluster $CLUSTER_NAME --service $FRONTEND_SERVICE_NAME --task-definition monitoria-frontend:$TASK_REVISION --force-new-deployment

echo "¡Despliegue completado!" 