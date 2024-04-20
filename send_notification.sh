#!/bin/bash

# Variables
SERVER_URL="http://34.136.150.204:8000"
MESSAGE='{"title": "Añade nuevas canciones a tus listas!", "body": "Recuerda que pueden añadir nuevas canciones a tus listas cuando quieras"}'


# Enviar la notificación al servidor
curl -X POST \
  -H "Content-Type: application/json" \
  -d "$MESSAGE" \
  "$SERVER_URL/notifications"

