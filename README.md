
# Bienvenido a Proyecto con CDK c:

Este es un pequeño manual para ejecutar diferentes comandos necesiarios al momento de realizar un deploy
al servucio de aws.

Verificar que tenemos instalado node.

```
node -v
```

Verificar que tenemos instalado python.

```
python --version
```

Instalar cdk, libreria nativa de AWS te creara un entorno virtual asi que debes de activarlo,
Nota: Crear una carpeta interna si no te deja correr el comando, además puedes eliminar tests ya que no veremos nada de eso.

```
cdk init app --language python
```

Nota: Después de ejecutar este comando todo lo genereado lo dejé en la carpeta raíz

Comando para crear un entorno virtual: No es necesario ejecutar ya que el cdk init crea tu entorno virtual.
En caso de necesitar generarlo el comando que debes de utilizar es el siguiente.

```
python -m venv .venv
```

Activador entorno virtual para windows - Ejecutar desde la carpeta raiz

```
.venv\Scripts\activate.bat
```

Activador para otros OS

```
source .venv/bin/activate
```

Ejecutamos este comando para instalar los requerimientos

```
pip install -r .\requirements.txt
```

Puedes generar un bucket en tu ApplicationStack para comprobar que el deploy puede realizarse correctamente 
recuerda importar aws_s3 as s3
bucket = s3.Bucket(self, "MyFirstBucket")

Confirma que funcione:

```
aws sts get-caller-identity
```

Cloudformation stacks, crear nuestra pila,

```
cdk bootstrap aws://**********/us-west-2
```

## PARA CREAR UN REPOSITORIO DE DOCKER EN AWS
Ir a Eastic Container Regestry (ECR), crear un contenedor "nombre-contenedor" y toda la configuracion defautl


## Donde encontrar los recursos que generas 
CloudFormation - pilas: muestra progrso de actualizacion 
S3 - buckets 
ECS - cluster generado con la etiqueta correspondiente - definciiones de tareas para ver version 
ecs tambien crea una task definition al hacer una actualizacion, en este caso v2 
VPC - virtual private cloud 
EC2 - balanceadores de carga - el dns, ya funciona 
ECR - contenedor llamado "nombre-contenedor"


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

c:
