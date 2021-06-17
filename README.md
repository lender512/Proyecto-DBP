# Desarrollo Basado en Plataformas Sección 2.01 - Proyecto 1

## Nombre del proyecto: Party On

## Integrantes

| <a target="_blank">**Luis Berrospi**</a> | <a target="_blank">**Mauricio Nieto**</a> | <a target="_blank">**Julio Sarazu**</a> |<a target="_blank">**Adrián Boza**</a> |
| :---: | :---:| :---:| :---:|
| ![Luis](https://avatars2.githubusercontent.com/u/52045791?v=3&s=150) | ![Mauricio](https://avatars.githubusercontent.com/u/63524901?v=4) | ![Julio](https://avatars.githubusercontent.com/u/40171658?s=64&v=4) | ![Adrian](https://avatars.githubusercontent.com/u/40300535?v=4) |
| <a href="https://github.com/lender512" target="_blank">`github.com/lender512`</a> | <a href="https://github.com/Elmau1618" target="_blank">`github.com/Elmau1618`</a> | <a href="https://github.com/kalehtfree123" target="_blank">`github.com/kalehtfree123`</a> |<a href="https://github.com/adrianboza" target="_blank">`github.com/adrianboza`</a> |

## Descripción del proyecto

En esta primera entrega hicimos una página web que le permite a las personas publicar o buscar una fiesta.

## Objetivos principales / Misión / Visión
### Misión:
- 

### Visión:
- Lograr que la personas se sientan satisfechas con el uso de nuestra plataforma web.

### Objetivos principales:
- Tener un login y sign in que permita a los usuarios tener una cuenta personal.
- Tener un CRUD para los posts.
- Dar al usuario la posibilidad de tener más de una dirección.

## Información acerca de las tecnologías utilizadas en Front-end, Back-end y Base de datos
### Front-end:
HTML, CSS
### Back-end:
flask, SQLAlchemy, operator, render_template, request, jsonify, flask.helpers, flash, url_for, flask.wrappers, Request, Response, flask_login, LoginManager, login_user, current_user, passlib.hash, pbkdf2_sha256, os, json, flask_login.utils, login_required, sqlalchemy.orm, query, werkzeug.utils, redirect, flask_migrate, migrate, sys y re
### Base de datos:
Postgresql, Heroku

## El nombre del script a ejecutar para iniciar la base de datos con datos

`app.py` importando `models.py`

## Información acerca de los API. Requests y respuestas de cada endpoint utilizado en el sistema
Utilizamos muchos @app.route para crear, editar y eliminar información en la base de datos y para hacer un login y signin.
## Hosts
Utilizamos el localhost:8080
## Forma de Autenticación
Se verifica que el usuario esté registrado, mediante el login se debe verificar que los datos sean los correctos.  
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

## Cómo ejecutar el sistema (Deployment scripts)
La primera vez se debe implementar el intéprete de python en Visual Studio Code.  
Usar el requirements.txt para saber qué instalar y que todo corra bien.  
Correr dentro de `app.py`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
