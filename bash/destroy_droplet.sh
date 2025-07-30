# destroy_droplet.sh
#!/usr/bin/env bash
set -eo pipefail


if [ -z "${API_TOKEN:-}" ]; then
  echo "❌ Error: API_TOKEN no definido."
  exit 1
fi


if [ ! -f droplet_id.txt ]; then
  echo "❌ Error: droplet_id.txt no encontrado. ¿Creaste primero el droplet?"
  exit 1
fi

DROPLET_ID=$(<droplet_id.txt)
echo "🗑️  Destruyendo droplet ID=${DROPLET_ID}..."


curl -sSL -X DELETE "https://api.digitalocean.com/v2/droplets/${DROPLET_ID}" \
  -H "Authorization: Bearer ${API_TOKEN}"


rm -f droplet_id.txt droplet_ip.txt

echo "✅ Droplet ${DROPLET_ID} destruido."
