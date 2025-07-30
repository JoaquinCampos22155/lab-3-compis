# create_droplet.sh
#!/usr/bin/env bash
set -eo pipefail

# 1) Verifica API_TOKEN
if [ -z "${API_TOKEN:-}" ]; then
  echo "❌ Error: API_TOKEN no definido."
  exit 1
fi


DROPLET_NAME="example-droplet"
REGION="nyc1"
SIZE="s-1vcpu-512mb-10gb"
IMAGE="ubuntu-24-10-x64"

echo "📩 Creando droplet..."


RESPONSE=$(curl -sSL -X POST "https://api.digitalocean.com/v2/droplets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -d "{\"name\":\"${DROPLET_NAME}\",\"region\":\"${REGION}\",\"size\":\"${SIZE}\",\"image\":\"${IMAGE}\"}")


DROPLET_ID=$(echo "${RESPONSE}" | jq -r '.droplet.id')
if [ -z "${DROPLET_ID}" ] || [ "${DROPLET_ID}" = "null" ]; then
  echo "❌ Falló la creación del droplet. Respuesta completa:"
  echo "${RESPONSE}"
  exit 1
fi
echo "🆔 Droplet ID: ${DROPLET_ID}"


echo "⏳ Esperando IP pública..."
DROPLET_IP="N/A"
for i in $(seq 1 12); do
  INFO=$(curl -sSL -H "Authorization: Bearer ${API_TOKEN}" \
    "https://api.digitalocean.com/v2/droplets/${DROPLET_ID}")
  IP=$(echo "${INFO}" | jq -r '.droplet.networks.v4[]? | select(.type=="public") | .ip_address')
  if [ -n "${IP}" ]; then
    DROPLET_IP="${IP}"
    echo "🌐 IP obtenida: ${DROPLET_IP}"
    break
  fi
  echo "⏳ Intento $i/12..."
  sleep 5
done


echo "${DROPLET_ID}" > droplet_id.txt
echo "${DROPLET_IP}" > droplet_ip.txt

echo "✅ Listo: ID=${DROPLET_ID}, IP=${DROPLET_IP}"