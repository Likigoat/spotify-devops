Actividad en clase 28/04/2026
Solución DevOps completa que integra control de versiones, contenedores, automatización, validación continua e infraestructura como código para una plataforma de reproducción de contenido digital.

Estructura del Proyecto
spotify-devops/
├── app/                        # Aplicación Flask principal
│   ├── app.py
│   └── Dockerfile
├── helper/                     # Servicio auxiliar de estado
│   ├── helper.py
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI con GitHub Actions
├── setup_project.sh            # Script de preparación del entorno
├── project_report.py           # Reporte de estado del proyecto
├── docker-compose.yml          # Orquestación de contenedores
├── infraestructura-base.yaml   # Plantilla CloudFormation para AWS
└── README.md

Contenedores y sus funciones
Contenedor 1 – Aplicación Principal (app/)
•	Tecnología: Flask (Python)
•	Puerto: 5000
•	Ruta principal: GET / → Devuelve un mensaje de bienvenida de la plataforma
•	Problema que resuelve: Estandariza el entorno de ejecución de la aplicación principal, eliminando inconsistencias entre equipos de desarrollo ("funciona en mi máquina").
Contenedor 2 – Servicio Auxiliar (helper/)
•	Tecnología: Flask (Python)
•	Puerto: 5001
•	Ruta principal: GET /status → Devuelve información del sistema y estado del proyecto
•	Problema que resuelve: Separa la responsabilidad de monitoreo y diagnóstico de la lógica de negocio principal, permitiendo consultar el estado del proyecto sin afectar la app principal.
¿Por qué separar en dos contenedores?
•	Separación de responsabilidades: Cada servicio tiene un único propósito claro.
•	Escalabilidad independiente: Se puede escalar la app principal sin tocar el servicio auxiliar.
•	Tolerancia a fallos: Si el servicio auxiliar cae, la app principal sigue funcionando.
•	Mantenimiento aislado: Se pueden actualizar, reiniciar o depurar de forma independiente.

Cómo ejecutar el proyecto
Prerequisitos
•	Docker
•	Docker Compose
Levantar ambos servicios
docker-compose up --build
Acceder a los servicios
Servicio	URL
App principal	http://localhost:5000
Servicio auxiliar	http://localhost:5001/status
Detener los servicios
docker-compose down

Scripts de Automatización
setup_project.sh
Simula la preparación del entorno Linux para el proyecto. Ejecuta:
bash setup_project.sh
project_report.py
Genera un reporte de estado del proyecto verificando que todos los archivos clave existen:
python3 project_report.py

Infraestructura en AWS (infraestructura-base.yaml)
La plantilla CloudFormation define:
Instancia EC2
•	Servicio: Ejecuta los contenedores Docker de la app principal y el servicio auxiliar mediante Docker Compose.
•	Sistema Operativo: Amazon Linux 2
•	Acceso: SSH mediante par de llaves
Bucket S3
•	Uso: Almacenamiento de artefactos del build (código comprimido, logs de deploy, reportes del pipeline).
•	Acceso: Privado, solo lectura desde EC2 mediante IAM Role
Cómo apoya el despliegue futuro
1.	GitHub Actions valida el código y genera artefactos
2.	Los artefactos se suben al bucket S3
3.	La instancia EC2 descarga los artefactos desde S3
4.	EC2 ejecuta docker-compose up para levantar los servicios actualizados

Estrategia de Monitoreo con CloudWatch
Métricas a observar
#	Métrica	Descripción
1	CPUUtilization	Uso de CPU de la instancia EC2. Alerta si supera 80% por 5 min.
2	HTTPCode_Target_5XX_Count	Errores 5xx en los contenedores. Indica fallos en la aplicación.
3	MemoryUtilization	Uso de memoria RAM. Valores altos pueden indicar memory leaks.
Alerta definida
•	Nombre: HighCPUAlarm
•	Condición: CPU > 80% durante 2 períodos consecutivos de 5 minutos
•	Acción: Enviar notificación SNS al equipo de operaciones
Acción sugerida ante falla
Si HTTPCode_Target_5XX_Count supera 10 errores en 1 minuto:
1.	CloudWatch dispara la alarma
2.	SNS notifica al equipo vía correo/Slack
3.	El equipo revisa logs con docker logs <container>
4.	Si persiste, se hace rollback al último tag de imagen estable en ECR
Relación con el caso de estudio
Si nadie los monitorea, los errores en producción pueden pasar desapercibidos por horas. CloudWatch permite detectar problemas del servicio de forma proactiva y reaccionar antes de que el usuario final lo perciba, algo muy importannte en plataformas de streaming como Spotify.

 Diseño de Despliegue en AWS
Flujo conceptual de despliegue
Developer → GitHub Push → GitHub Actions (CI)
                               ↓
                    Validación de archivos
                    Simulación del pipeline
                               ↓
                    [Si todo pasa] → Artefacto a S3
                               ↓
                    EC2 descarga desde S3
                               ↓
                    docker-compose up --build
                               ↓
                    App en http://<EC2-IP>:5000
                    Helper en http://<EC2-IP>:5001
•	EC2: Corre Docker Engine + Docker Compose con ambos contenedores
•	Código desde GitHub: GitHub Actions empaqueta el repo y lo sube a S3; EC2 lo descarga con AWS CLI
•	GitHub Actions: Valida que todos los archivos existen y el pipeline es correcto ANTES de permitir el despliegue



Conclusión Técnica
El uso de contenedores Docker resulta clave para eliminar las inconsistencias entre entornos de desarrollo, integración y producción, ya que encapsulan la aplicación junto con todas sus dependencias en una misma imagen. Esto garantiza que el comportamiento sea idéntico en cualquier lugar donde se ejecute, eliminando de raíz el clásico problema de “funciona en mi máquina”. A partir de esto, GitHub Actions fortalece el flujo del proyecto al automatizar las validaciones necesarias en cada cambio, asegurando que todos los pushes pasen por las mismas verificaciones sin importar quién los realice. Esto no solo da consistencia, sino que también ofrece retroalimentación rápida al desarrollador, permitiéndole detectar errores en minutos y actuando como un filtro de calidad antes de llegar a producción. Además, la separación de responsabilidades en dos contenedores distintos aporta mayor robustez al sistema, ya que permite aislar fallos, escalar componentes de manera independiente y simplificar el mantenimiento. A diferencia de un proceso manual único, esta arquitectura reduce el riesgo de caídas totales y, gracias a herramientas como Docker Compose, mantiene una operación sencilla mediante un solo comando, combinando simplicidad con las ventajas de una solución basada en contenedores.

Estrategia de Ramas
Rama	            Propósito
main	            Código en producción, protegida
develop	            Integración de features
feature-containers	Desarrollo de Dockerfiles y Compose
feature-actions	    Desarrollo del workflow de CI

