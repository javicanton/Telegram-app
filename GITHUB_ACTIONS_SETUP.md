# Configuración de GitHub Actions para Despliegue Automático

## Resumen de Cambios Implementados

He configurado el despliegue automático con GitHub Actions para tu aplicación. Los siguientes archivos han sido creados/modificados:

### Archivos Creados:
- `.github/workflows/deploy-backend.yml` - Despliegue automático del backend
- `.github/workflows/deploy-frontend.yml` - Despliegue automático del frontend  
- `.github/workflows/deploy-all.yml` - Despliegue completo de la aplicación
- `GITHUB_ACTIONS_SETUP.md` - Este archivo de instrucciones

### Archivos Modificados:
- `backend/ecs-task-definition.json` - Actualizado para usar variables de ECR
- `frontend/ecs-task-definition.json` - Actualizado para usar variables de ECR

## Configuración Requerida

### 1. Secrets de GitHub (OBLIGATORIO)

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions

Agrega los siguientes secrets:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

**Cómo obtener las credenciales:**
1. Ve a AWS IAM → Users → Tu usuario
2. Crea una nueva Access Key si no tienes una
3. Asegúrate de que el usuario tenga los siguientes permisos:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonECS_FullAccess`
   - `AmazonEC2ContainerServiceFullAccess`

### 2. Configurar ECR Repositories

Si no existen, crea los repositorios en ECR:

```bash
# Backend repository
aws ecr create-repository --repository-name monitoria-backend --region eu-north-1

# Frontend repository  
aws ecr create-repository --repository-name monitoria-frontend --region eu-north-1
```

### 3. Verificar Configuración ECS

Asegúrate de que tienes:
- Cluster: `monitoria-cluster`
- Backend Service: `monitoria-backend-service`
- Frontend Service: `monitoria-frontend-service`

## Cómo Funciona

### Triggers Automáticos:
- **Backend**: Se despliega cuando hay cambios en `backend/`
- **Frontend**: Se despliega cuando hay cambios en `frontend/`
- **Todo**: Se despliega cuando hay cambios en ambos o archivos de configuración

### Branches Configurados:
- `deploy-beta`

### Proceso de Despliegue:
1. GitHub Actions detecta cambios
2. Construye la imagen Docker
3. Sube la imagen a ECR
4. Actualiza la task definition de ECS
5. Despliega el servicio en ECS
6. Verifica que el despliegue sea exitoso

## Uso Manual

También puedes disparar el despliegue manualmente:
1. Ve a Actions en tu repositorio GitHub
2. Selecciona el workflow deseado
3. Haz clic en "Run workflow"

## Troubleshooting

### Error: "Repository does not exist"
- Verifica que los repositorios ECR existan
- Ejecuta los comandos de creación de repositorios arriba

### Error: "Access denied"
- Verifica los secrets de GitHub
- Asegúrate de que las credenciales AWS tengan los permisos necesarios

### Error: "Service not found"
- Verifica que los servicios ECS existan con los nombres correctos
- Verifica que el cluster `monitoria-cluster` exista

## Eliminación del Script Manual

Una vez que GitHub Actions esté funcionando correctamente, puedes eliminar:
- `backend/aws-deploy.sh` (script de despliegue manual)

## Monitoreo

Los logs de despliegue estarán disponibles en:
- GitHub → Actions → [Workflow ejecutado] → [Job] → [Step]

Los logs de la aplicación estarán en:
- AWS CloudWatch → Log Groups → `/ecs/monitoria-backend` y `/ecs/monitoria-frontend`
