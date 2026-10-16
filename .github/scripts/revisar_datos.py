"""Busca en el repositorio datos que no pueden publicarse: direcciones IP
privadas o internas. Los secretos (tokens, claves) los busca gitleaks.

Sale con código 1 si encuentra alguna, indicando fichero y línea.
"""
import ipaddress
import re
import subprocess
import sys

IP = re.compile(r"(?<![\d.])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?![\d.])")
PERMITIDAS = {"0.0.0.0", "127.0.0.1"}
# CGNAT (rango compartido de operadora, /10): Python no la marca como privada
CGNAT = ipaddress.ip_network((0x64400000, 10))


def interna(texto: str) -> bool:
    if texto in PERMITIDAS:
        return False
    try:
        ip = ipaddress.ip_address(texto)
    except ValueError:
        return False
    return ip.is_private or ip.is_link_local or ip in CGNAT


ficheros = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split()
hallazgos = 0
for f in ficheros:
    try:
        lineas = open(f, encoding="utf-8").read().splitlines()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        continue  # binarios (imágenes)
    for n, linea in enumerate(lineas, 1):
        for ip in IP.findall(linea):
            if interna(ip):
                print(f"{f}:{n}: dirección interna o privada {ip}")
                hallazgos += 1

if hallazgos:
    print(f"\n{hallazgos} dirección(es) que no pueden publicarse. Usa nombres de ejemplo "
          "(mcp.tudominio.com) o variables de entorno.")
    sys.exit(1)
print("Sin direcciones internas ni privadas.")
