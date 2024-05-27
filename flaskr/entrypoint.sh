#!/bin/sh
# Iniciar Flask en segundo plano

flask run --host=0.0.0.0 --port=5000 &

# Ejecutar el script pubsub.py

python pobsub_worker.py

# Evitar que el contenedor termine inmediatamente
wait -n