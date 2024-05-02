# back-restaurant

#### Dependencias
- Docker
- Python 3.11
- Django 5.0.4

#### Para compilar/levantar el proyecto:
- ```docker-compose up --build```

#### Crear usuario admin (nos servirá para entrar al panel administrativo y documentación api)
- ```docker-compose run web python manage.py createsuperuser```

#### Documentación api
- ```http://localhost:8000/api/doc/```

#### Panel administrativo
- ```http://localhost:8000/admin/```

#### Ejecutar los tests
- ```docker-compose run web python manage.py test```