#!/usr/bin/env python3
"""
MCP Server — Certificados TLS (plantilla de servidor propio para TTKIA)

Tools MCP:
  - cert_expiry → Fecha de caducidad y emisor del certificado TLS de un host

SDK `mcp` 2.1.1, revisión 2026-07-28, streamable HTTP sin sesión.

Para adaptarla a tu script, cambia las partes 1, 2 y 3. La 4 es igual en
todos los servidores.
"""

import asyncio
import hmac
import json
import os
import socket
import ssl
from datetime import datetime, timezone
from typing import Any

import uvicorn
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import mcp_types as types
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.settings import AuthSettings
from mcp.server.lowlevel import Server
from mcp_types import TextContent, Tool

PORT = int(os.getenv("PORT", "8000"))
CONNECT_TIMEOUT = 8          # TTKIA corta cada llamada a los 30 s
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "")

# ── 1. Instrucciones: lo que lee el planificador para decidir si usarlo ────
INSTRUCTIONS = """\
Comprueba certificados TLS de servicios expuestos (caducidad, emisor, sujeto).

Cuándo usarlo: cuando el usuario pregunte cuándo caduca el certificado de un
host o servicio HTTPS, o quién lo emite.

Cuándo no usarlo: para preguntas generales sobre TLS o PKI que no citan un
host concreto.

Cómo usar las herramientas: cert_expiry con el nombre DNS del host; el puerto
es 443 si no se indica.
"""

# ── 2. Herramientas: nombre, descripción, esquema y anotaciones ────────────
# Sin read_only_hint=True, TTKIA no deja activar la herramienta.
READ_ONLY = types.ToolAnnotations(read_only_hint=True, destructive_hint=False,
                                  idempotent_hint=True, open_world_hint=True)


def _tools() -> list[Tool]:
    return [
        Tool(
            name="cert_expiry",
            title="Caducidad de un certificado TLS",
            annotations=READ_ONLY,
            description=("Conecta por TLS a un host y devuelve el sujeto, el emisor, "
                         "las fechas de validez y los días que faltan para que caduque."),
            input_schema={
                "type": "object",
                "properties": {
                    "host": {"type": "string", "description": "Nombre DNS del servicio, p. ej. www.example.com"},
                    "port": {"type": "integer", "description": "Puerto TLS (por defecto 443)"},
                },
                "required": ["host"],
            },
        ),
    ]


# ── 3. La lógica: aquí va tu script ───────────────────────────────────────
def _read_cert(host: str, port: int) -> dict[str, Any]:
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=CONNECT_TIMEOUT) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()
    not_after = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), timezone.utc)
    flat = lambda rdns: {k: v for rdn in rdns for k, v in rdn}
    return {
        "status": "ok",
        "host": host,
        "port": port,
        "subject": flat(cert.get("subject", ())).get("commonName"),
        "issuer": flat(cert.get("issuer", ())).get("organizationName"),
        "not_after": not_after.isoformat(),
        "days_left": (not_after - datetime.now(timezone.utc)).days,
    }


async def call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name != "cert_expiry":
        return {"status": "unknown_tool", "tool": name}
    host, port = (args.get("host") or "").strip(), int(args.get("port") or 443)
    if not host:
        return {"status": "error", "error": "Falta 'host'"}
    try:
        # Código bloqueante (socket, requests, un SDK síncrono) → a un hilo
        return await asyncio.to_thread(_read_cert, host, port)
    except ssl.SSLCertVerificationError as e:
        return {"status": "error", "host": host, "error": f"Certificado no válido: {e.verify_message}"}
    except (OSError, socket.timeout) as e:
        return {"status": "error", "host": host, "error": f"No se pudo conectar a {host}:{port}: {e}"}


# ── 4. Cableado MCP (igual en todos los servidores) ──────────────────────
async def on_list_tools(ctx, params) -> types.ListToolsResult:
    return types.ListToolsResult(tools=_tools())


async def on_call_tool(ctx, params: types.CallToolRequestParams) -> types.CallToolResult:
    payload = await call_tool(params.name, params.arguments or {})
    return types.CallToolResult(
        content=[TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))],
        is_error=payload.get("status") == "error",
    )


mcp_server = Server("mcp-certs", version="1.0.0", title="Certificados TLS",
                    instructions=INSTRUCTIONS,
                    on_list_tools=on_list_tools, on_call_tool=on_call_tool)


class _FixedTokenVerifier:
    """Token fijo (Authorization: Bearer), el mismo que pones al darlo de alta."""

    async def verify_token(self, token: str) -> AccessToken | None:
        if MCP_AUTH_TOKEN and hmac.compare_digest(token.encode(), MCP_AUTH_TOKEN.encode()):
            return AccessToken(token=token, client_id="ttkia", scopes=[])
        return None


async def health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "server": "mcp-certs"})


if not MCP_AUTH_TOKEN:
    raise RuntimeError("MCP_AUTH_TOKEN vacío: el servidor MCP no arranca sin token")

app = mcp_server.streamable_http_app(
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    host="0.0.0.0",   # acepta la cabecera Host de tu dominio (detrás del proxy HTTPS)
    auth=AuthSettings(issuer_url="http://localhost", resource_server_url=None),
    token_verifier=_FixedTokenVerifier(),
    custom_starlette_routes=[Route("/health", endpoint=health)],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
