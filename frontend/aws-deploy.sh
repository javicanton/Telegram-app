#!/bin/bash

# Variables
BUCKET_NAME="tu-bucket-s3"
DISTRIBUTION_ID="tu-cloudfront-distribution-id"
REGION="us-east-1"  # Cambia esto a tu región preferida

# Construir la aplicación
echo "Construyendo la aplicación..."
npm run build

# Sincronizar con S3
echo "Sincronizando con S3..."
aws s3 sync build/ s3://$BUCKET_NAME/ --delete

# Invalidar caché de CloudFront
echo "Invalidando caché de CloudFront..."
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"

echo "¡Despliegue completado!" 