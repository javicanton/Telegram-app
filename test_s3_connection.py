#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con AWS S3
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_s3_connection():
    """Prueba la conexión con S3 y lista los archivos disponibles."""
    
    print("🔍 Probando conexión con AWS S3...")
    print("=" * 50)
    
    # Verificar variables de entorno
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_BUCKET']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("\n📝 Asegúrate de crear un archivo .env con las siguientes variables:")
        print("AWS_ACCESS_KEY_ID=tu_access_key_id")
        print("AWS_SECRET_ACCESS_KEY=tu_secret_access_key")
        print("AWS_REGION=eu-north-1")
        print("S3_BUCKET=monitoria-data")
        return False
    
    print("✅ Variables de entorno configuradas correctamente")
    print(f"   - Región: {os.environ.get('AWS_REGION')}")
    print(f"   - Bucket: {os.environ.get('S3_BUCKET')}")
    
    try:
        # Importar el cliente S3
        from backend.s3_client import get_s3_client
        
        print("\n🔌 Inicializando cliente S3...")
        s3_client = get_s3_client()
        
        print("✅ Cliente S3 inicializado correctamente")
        
        # Probar conexión
        print("\n🌐 Probando conexión con S3...")
        if s3_client.check_connection():
            print("✅ Conexión con S3 exitosa")
        else:
            print("❌ Error de conexión con S3")
            return False
        
        # Listar archivos
        print("\n📁 Listando archivos en el bucket...")
        files = s3_client.list_files()
        
        if files:
            print(f"✅ Se encontraron {len(files)} archivos:")
            for i, file in enumerate(files[:10], 1):  # Mostrar solo los primeros 10
                print(f"   {i}. {file}")
            
            if len(files) > 10:
                print(f"   ... y {len(files) - 10} archivos más")
        else:
            print("⚠️  No se encontraron archivos en el bucket")
        
        # Buscar archivo de mensajes
        print("\n🔍 Buscando archivo de mensajes...")
        messages_file = None
        for file in files:
            if 'telegram_messages' in file.lower():
                if file.endswith('.json'):
                    messages_file = file
                    break
                elif file.endswith('.csv') and not messages_file:
                    messages_file = file
        
        if messages_file:
            print(f"✅ Archivo de mensajes encontrado: {messages_file}")
            
            # Intentar cargar el archivo
            print(f"\n📖 Probando carga del archivo {messages_file}...")
            try:
                if messages_file.endswith('.json'):
                    data = s3_client.load_json_from_s3(messages_file)
                    if 'messages' in data:
                        print(f"✅ Archivo JSON cargado correctamente")
                        print(f"   - Número de mensajes: {len(data['messages'])}")
                        
                        # Mostrar estructura del primer mensaje
                        if data['messages']:
                            first_msg = data['messages'][0]
                            print(f"   - Columnas disponibles: {list(first_msg.keys())}")
                    else:
                        print("⚠️  El archivo JSON no tiene la estructura esperada")
                elif messages_file.endswith('.csv'):
                    df = s3_client.load_csv_from_s3(messages_file)
                    print(f"✅ Archivo CSV cargado correctamente")
                    print(f"   - Número de filas: {len(df)}")
                    print(f"   - Columnas disponibles: {list(df.columns)}")
                
            except Exception as e:
                print(f"❌ Error al cargar el archivo: {e}")
        else:
            print("⚠️  No se encontró archivo de mensajes en el bucket")
            print("   - Asegúrate de que exista un archivo llamado 'telegram_messages.json' o 'telegram_messages.csv'")
        
        print("\n🎉 Prueba de conexión completada exitosamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print("   - Asegúrate de haber instalado las dependencias: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 Iniciando pruebas de conexión con AWS S3")
    print("=" * 60)
    
    success = test_s3_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 Todas las pruebas pasaron correctamente")
        print("   Tu aplicación está lista para usar S3")
    else:
        print("💥 Algunas pruebas fallaron")
        print("   Revisa los errores arriba y corrige la configuración")
    
    print("\n📚 Para más información, consulta el README.md")

if __name__ == "__main__":
    main()
