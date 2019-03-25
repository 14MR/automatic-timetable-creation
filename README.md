# Automatic timetable creation
## Development version

1. Install [Docker](https://www.docker.com/) Community Edition
2. Install [git](https://git-scm.com/)
3. [Clone project](https://git-scm.com/docs/git-clone)
4. Login in Docker registry: `docker login registry.gitlab.com` ([see more about docker cli](https://docs.docker.com/engine/reference/commandline/cli/))
5. Run project in docker-environment - `docker-compose up`, wait when project starts
([see more about docker-compose](https://docs.docker.com/compose/))
6. Login into container: `docker exec -it backend_python_1 bash` (container's name may changed, check it in list - `docker ps`,
[see more about docker exec](https://docs.docker.com/engine/reference/commandline/exec/))
7. Install packages from pip: `pip install`
8. DB migration applying: `python ./manage.py migrate` (in the directory with manage.py)
9. Open website: [http://localhost](http://localhost) (address may changed, depends on environment)


__Rebuilding container:__

    docker build -t registry.gitlab.com/automatic-timetable-creation/backend:latest -f docker/app/Dockerfile .



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

