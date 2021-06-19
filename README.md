# Desarrollo Basado en Plataformas Sección 2.01 - Proyecto 1

## Nombre del proyecto: Party On

## Integrantes

| <a target="_blank">**Luis Berrospi**</a> | <a target="_blank">**Mauricio Nieto**</a> | <a target="_blank">**Julio Sarazu**</a> |<a target="_blank">**Adrián Boza**</a> |
| :---: | :---:| :---:| :---:|
| ![Luis](https://avatars2.githubusercontent.com/u/52045791?v=3&s=150) | ![Mauricio](https://avatars.githubusercontent.com/u/63524901?v=4) | ![Julio](https://avatars.githubusercontent.com/u/40171658?s=64&v=4) | ![Adrian](https://avatars.githubusercontent.com/u/40300535?v=4) |
| <a href="https://github.com/lender512" target="_blank">`github.com/lender512`</a> | <a href="https://github.com/Elmau1618" target="_blank">`github.com/Elmau1618`</a> | <a href="https://github.com/kalehtfree123" target="_blank">`github.com/kalehtfree123`</a> |<a href="https://github.com/adrianboza" target="_blank">`github.com/adrianboza`</a> |

## Descripción del proyecto

En esta primera entrega hicimos una página web que le permite a las personas publicar, buscar o unirse a una fiesta.

## Objetivos principales / Misión / Visión
### Misión:
- Nuestra misión es convertir las invitaciones a fiestas en algo rápido y sencillo, que sea escalable y de fácil uso.

### Visión:
- Construir el megáfono por el que la gente pueda conseguir invitados para sus grandes reuniones y dar las herramientas para facilitar la construcción de las mismas.

### Objetivos principales:
- Tener un login y sign in que permita a los usuarios tener una cuenta personal.
- Tener un CRUD para los posts.
- Dar al usuario la posibilidad de tener más de una dirección.
## Diagrama de casos de uso  
![alt text](https://i.imgur.com/G7AARH3.jpg)

## Información acerca de las tecnologías utilizadas en Front-end, Back-end y Base de datos
### Front-end:
HTML, CSS
#### - index.html:  
Es la página predeterminada que nos permite registrar o iniciar sesión.
#### - register.html:  
Dentro de esta página las personas se pueden registrar.
#### - login.html:  
Permite a los usuarios registrados iniciar sesión.
#### - main.html:  
Es la página principal que permite al usuario crear una dirección, crear un post con la dirección que desee y/o elegir ir a una fiesta.
#### - edit.html:  
Permite al usuario logueado editar o eliminar el post que creó anteriormente.
#### - search.html:  
Permite a los usuarios logueados buscar una fiesta a través de una dirección.
### Back-end:
- flask: Framework que permite crear el servidor.
- flask.helpers: Módulo de flask que permite pasar un string message al request y generar una URL usando el método pasado.
- flask_login: Proporciona gestión de sesiones de usuario para Flask.
- passlib.hash: Algoritmo de encriptación de contraseñas.
- os: Permite interactuar con el Sistema Operativo.
- json: Crear listas de diccionarios.
- flask_login.utils: Hacer necesario el login para acceder al main.
- sqlalchemy.orm: Acceder a una base de datos relacional.
- models: Permite importar los modelos creados para la base de datos.
- werkzeug.utils: Permite redirigir a otra página.
- flask_migrate: Permite manejar las migraciones de la base de datos.
- operator: Exportar funciones. operator.add(x, y) = x+y

#### - models.py:  
Permite crear las tablas persons, apartments, posts y likes.  
#### - app.py:
Permite implementar el back-end usando flask y más herramientas, además de tomar models.py para el uso de los modelos y lograr que la página web funcione correctamente junto a la base de datos.
#### - test.py:
Permite realizar el unit testing
### Base de datos:
Postgresql alojado en Heroku.

## El nombre del script a ejecutar para iniciar la base de datos con datos

No es necesario un script relacionado a las tablas debido a que está alojado en Heroku.

## Información acerca de los API. Requests y respuestas de cada endpoint utilizado en el sistema
Utilizamos muchos @app.route para crear, editar y eliminar información en la base de datos y para hacer un login y signin.
## Hosts
Utilizamos el localhost:8080
## Forma de Autenticación
Se verifica que el usuario esté registrado, mediante el login se debe verificar que los datos sean los correctos.  
Si el usuario no se loguea no podrá acceder al main, le aparecerá un error pidiéndole que se loguee.
Además, la contraseña está encriptada.
```python
@app.route('/logIn', methods=['POST'])
def logIn():

    response = {}
    error = False

    email = request.get_json()['email']
    password = request.get_json()['password']
    try: 
        person = Person.query.filter_by(email=email).first()
        if person is None:
            error = True
            response['error_msg'] = 'Invalid email'
        elif not pbkdf2_sha256.verify(password, person.password):
            error = True
            response['error_msg'] = 'Invalid password'
            
        else:
            login_user(person)
    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        
    finally:
        response['error'] = error

    return jsonify(response)'
```


## Manejo de errores HTTP: 500, 400, 300, 200, 100, etc
De manera amigable se le muestra una alerta o muestra un error al usuario.  
**Alertas**
- Cuando no se ingresa nada en el registro.
- Cuando se registra con un correo ya registrado.
- Cuando la contraseña no es mayor de 8 dígitos.
- Cuando las contraseñas no son las mismas.
- Cuando no se ingresa nada en el login.
- Cuando no se ingresa un correo correcto y registrado.
- Cuando la contraseña no coincide con el correo registrado.
- Cuando se intenta publicar un post vacío. 
- Cuando se intenta añadir una dirección vacía.
- Cuando se intenta crear un post sin elegir una dirección.
- Cuando se intenta editar un post y guardarlo vacío.  
### Error 401 Unauthorized: Aparecerá cuando se intenta acceder al main sin antes loguearse.
### Error 404 Not Found: Aparecerá cuando no encuentra algo en la página.
### Error 410 Gone: Aparecerá cuando un recurso es solicitado pero ya no está disponible.
### Error 500 Internal Server Error: Aparecerá cuando el servidor falle.


## Cómo ejecutar el sistema (Deployment scripts)
*Recomendamos abrir desde carpeta app*  
La primera vez se debe implementar el intéprete de python en Visual Studio Code.  
Usar el requirements.txt para saber qué instalar y que todo corra bien.  
Correr dentro de `app.py`.


