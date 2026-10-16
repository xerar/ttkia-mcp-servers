# Plantilla: mcp-certs

Servidor MCP de ejemplo para TTKIA. Comprueba cuándo caduca el certificado TLS de un host. Cópialo y cambia las partes 1, 2 y 3 de `src/main.py` por tu script: [guía paso a paso](../docs/servidor-propio.md).

Preguntas de TTKIA que responde:

- «¿Cuándo caduca el certificado de www.example.com?»
- «¿Quién emite el certificado de mi-servicio.example.com?»

## Herramientas

- `cert_expiry`: sujeto, emisor, fechas de validez y días que faltan para la caducidad del certificado TLS de un host.

## Qué necesita

- `MCP_AUTH_TOKEN`: el token que pondrás al darlo de alta en TTKIA. Ver `.env.example`.
- Salida a internet hacia los hosts que consulta, por el puerto TLS que se le indique.

## Ficheros

| Fichero | Para qué |
| --- | --- |
| `src/main.py` | El servidor |
| `probar.py` | Lo prueba como lo haría TTKIA |
| `prueba.json` | La llamada que hace la revisión automática |
| `requirements.txt` | Dependencias, con versiones fijadas |
| `Dockerfile` | Imagen del servidor |
| `docker-compose.yml`, `Caddyfile` | Servidor + Caddy para publicarlo con HTTPS |
| `.env.example` | Variables que necesita, vacías |

## Mantiene

[@xerar](https://github.com/xerar)
