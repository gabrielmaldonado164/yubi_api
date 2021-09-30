yubi
=============

build project

    docker-compose -f local.yml build

and run

    docker-compose -f local.yml run

debugin

    docker-compose -f local.yml ps
    docker rm -f yubi_django_1
    docker-compose -f local.yml run --rm --service-ports django
