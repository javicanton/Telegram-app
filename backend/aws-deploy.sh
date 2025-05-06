#!/bin/bash

# Variables
ECR_REPOSITORY_NAME="monitoria-backend"
ECR_REPOSITORY_URI="tu-cuenta.dkr.ecr.us-east-1.amazonaws.com/$ECR_REPOSITORY_NAME"
CLUSTER_NAME="monitoria-cluster"
SERVICE_NAME="monitoria-backend-service"
REGION="us-east-1"

# Login a ECR
echo "Iniciando sesión en ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY_URI

# Construir y subir la imagen
echo "Construyendo y subiendo la imagen..."
docker build -t $ECR_REPOSITORY_NAME .
docker tag $ECR_REPOSITORY_NAME:latest $ECR_REPOSITORY_URI:latest
docker push $ECR_REPOSITORY_URI:latest

# Actualizar la definición de tarea
echo "Actualizando la definición de tarea..."
TASK_DEFINITION=$(aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json)
TASK_REVISION=$(echo $TASK_DEFINITION | jq -r '.taskDefinition.revision')

# Actualizar el servicio
echo "Actualizando el servicio..."
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --task-definition monitoria-backend:$TASK_REVISION --force-new-deployment

echo "¡Despliegue completado!" 