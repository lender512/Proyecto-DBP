# Desarrollo Basado en Plataformas Sección 2.01 - Proyecto 1

Foobar is a Python library for dealing with word pluralization.

## Integrantes

| <a target="_blank">**Luis Berrospi**</a> | <a target="_blank">**Mauricio Nieto**</a> | <a target="_blank">**Julio Sarazu**</a> |<a target="_blank">**Adrián Boza**</a> |
| :---: | :---:| :---:| :---:|
| ![Luis](https://avatars2.githubusercontent.com/u/52045791?v=3&s=150) | ![Mauricio](https://avatars.githubusercontent.com/u/63524901?v=4) | ![Julio](https://avatars.githubusercontent.com/u/40171658?s=64&v=4) | ![Adrian](https://avatars.githubusercontent.com/u/40300535?v=4) |
| <a href="https://github.com/lender512" target="_blank">`github.com/lender512`</a> | <a href="https://github.com/Elmau1618" target="_blank">`github.com/Elmau1618`</a> | <a href="https://github.com/kalehtfree123" target="_blank">`github.com/kalehtfree123`</a> |<a href="https://github.com/adrianboza" target="_blank">`github.com/adrianboza`</a> |

## Descripción del proyecto

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Objetivos principales / Misión / Visión
### Misión:

### Visión:

### Objetivos principales:

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```
## Información acerca de las tecnologías utilizadas en Front-end, Back-end y Base de datos
### Front-end:
HTML, CSS
### Back-end:
flask, SQLAlchemy,
### Base de datos:
Postgresql, Heroku

## El nombre del script a ejecutar para iniciar la base de datos con datos
Se ejecuta app.py que recibe los modelos y las tablas que se crearan de models.py
'app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False'

db = SQLAlchemy(app)


## Información acerca de los API. Requests y respuestas de cada endpoint utilizado en el sistema
Utilizamos muchos @app.route para crear, editar y eliminar información en la base de datos.

## Hosts
Utilizamos el localhost:8080
## Forma de Autenticación

## Manejo de errores HTTP: 500, 400, 300, 200, 100, etc

## Cómo ejecutar el sistema (Deployment scripts)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
