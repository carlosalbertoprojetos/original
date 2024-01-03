#!/bin/bash
# Diretorio e arquivo de log
set -e
LOGFILE=/tmp/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
# Numero de processo simultaneo, modifique de acordo com seu processador
NUM_WORKERS=2
# Usuario/Grupo que vai rodar o gunicorn
USER=deploy
#GROUP=root
# Endereço local que o gunicorn irá rodar
ADDRESS=0.0.0.0:8000
# Ativando ambiente virtual e executando o gunicorn para este projeto
source ~/.virtualenvs/original/bin/activate
cd /home/deploy/projetos/original/src/project/
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn   --max-requests=100  -w $NUM_WORKERS --bind=$ADDRESS --user=$USER --log-level=error --log-file=$LOGFILE 2>>$LOGFILE project.wsgi
