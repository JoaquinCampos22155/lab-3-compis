#!/usr/bin/env python3
import argparse
import json
import os
import time
import requests
from antlr4 import FileStream, CommonTokenStream
from generated.TerraformSubsetLexer import TerraformSubsetLexer
from generated.TerraformSubsetParser import TerraformSubsetParser
from generated.TerraformSubsetVisitor import TerraformSubsetVisitor

STATE_FILE = "terraform_state.json"


class ConfigVisitor(TerraformSubsetVisitor):
    """
    Recolecta los campos del recurso digitalocean_droplet
    """
    def __init__(self):
        self.config = {}

    def visitResource(self, ctx):
        # ctx.STRING(0) es el tipo de recurso, ctx.STRING(1) el nombre lógico
        rtype = ctx.STRING(0).getText().strip('"')
        if rtype == "digitalocean_droplet":
            # Recorre las asignaciones dentro de body()
            for kv in ctx.body().keyValue():
                key = kv.IDENTIFIER().getText()
                expr = kv.expr()
                # Solo nos interesan valores literales STRING
                strNode = expr.STRING()
                if strNode:
                    val = strNode.getText().strip('"')
                    if key in ("name", "region", "size", "image"):
                        self.config[key] = val
        # Continúa el recorrido para otros posibles recursos
        return self.visitChildren(ctx)




def parse_tf(file_path):
    input_stream = FileStream(file_path)
    lexer = TerraformSubsetLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = TerraformSubsetParser(tokens)
    tree = parser.terraform()
    visitor = ConfigVisitor()
    visitor.visit(tree)
    return visitor.config

def create_droplet(config, token):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # omitimos verificación SSL para no bloquearnos en dev
    resp = requests.post(url, headers=headers, json=config, verify=False)
    resp.raise_for_status()
    did = resp.json()["droplet"]["id"]
    # Poll para IP
    ip = None
    for i in range(12):
        info = requests.get(
            f"https://api.digitalocean.com/v2/droplets/{did}",
            headers=headers,
            verify=False
        ).json()
        addrs = info["droplet"]["networks"]["v4"]
        if addrs:
            ip = next((x["ip_address"] for x in addrs if x["type"]=="public"), None)
            if ip:
                break
        time.sleep(5)
    return {"id": did, "ip": ip or "N/A"}



def destroy_droplet(token):
    if not os.path.exists(STATE_FILE):
        print("❌ No existe el statefile.")
        return
    state = json.load(open(STATE_FILE))
    did = state.get("id")
    if not did:
        print("❌ Statefile inválido.")
        return
    url = f"https://api.digitalocean.com/v2/droplets/{did}"
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(url, headers=headers, verify=False).raise_for_status()
    print(f"🗑️  Droplet {did} destruido.")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", metavar="TF", help="Parsea y aplica un .tf")
    p.add_argument("--destroy", action="store_true", help="Destruye droplet de state")
    args = p.parse_args()

    token = os.getenv("API_TOKEN")
    if not token:
        print("❌ Exporta API_TOKEN en tu entorno (en tu Mac, no dentro del contenedor).")
        return

    if args.apply:
        cfg = parse_tf(args.apply)
        droplet = create_droplet(cfg, token)

        # Imprime ID e IP en consola
        print(f"🆔 Droplet creado: {droplet['id']}")
        print(f"🌐 IP encontrada: {droplet['ip']}")

        # Guarda el statefile usando droplet['ip']
        state = {
            "id": droplet["id"],
            "ip": droplet["ip"]
        }
        json.dump(state, open(STATE_FILE, "w"), indent=2)
        print("✅ State guardado en", STATE_FILE)

    elif args.destroy:
        destroy_droplet(token)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
