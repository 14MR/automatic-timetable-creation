# Automatic timetable creation
## Development version

1. Install [Docker](https://www.docker.com/) Community Edition
2. Install [git](https://git-scm.com/)
3. [Clone project](https://git-scm.com/docs/git-clone)
4. Login in Docker registry: `docker login registry.gitlab.com` ([see more about docker cli](https://docs.docker.com/engine/reference/commandline/cli/))
5. Run project in docker-environment - `docker-compose up`, wait when project starts
([see more about docker-compose](https://docs.docker.com/compose/))
6. Open website: [http://localhost](http://localhost) (address may changed, depends on environment)


__Rebuilding container:__

    docker build -t registry.gitlab.com/automatic-timetable-creation/backend:latest -f docker/app/Dockerfile .
    
__Login into container:__
    `docker exec -it backend_python_1 bash`
    
__Applying migrations:__
    While in container enter `python manage.py migrate`


###Testing
In order to benefit more gain in combining functional and unit testing we agreed to use [pytest-django](https://pytest-django.readthedocs.io/en/latest) plugin on top of [pytest](https://docs.pytest.org/en/latest/contents.html) framework. 


We follow some conventions according to testing:
1. Test files are named `test_*.py`
2. Test classes are named `Test*`
3. Test methods are named `test_*`

### Celery
* Celery tasks - regular python functions
```
from celery.decorators import task

@app.task(name="test_celery_task")
def t_celery_task():
    logger.info("test_celery_task")
    return t_celery()
```
* Run task asynchronously with
```
t_celery.delay()
```

