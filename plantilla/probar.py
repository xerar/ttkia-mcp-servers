"""Prueba un servidor MCP como lo usaría TTKIA: token, instrucciones,
herramientas con su anotación de solo lectura y, si se indica, una llamada.

Uso:  python probar.py <url> <token> [herramienta] [argumentos JSON]

Sale con código 1 si alguna herramienta no es de solo lectura o si la
llamada devuelve error.
"""
import asyncio
import json
import sys
from contextlib import asynccontextmanager

from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.shared._httpx_utils import create_mcp_http_client


@asynccontextmanager
async def _transport(url: str, token: str):
    async with create_mcp_http_client(headers={"Authorization": f"Bearer {token}"}) as http:
        async with streamable_http_client(url, http_client=http) as streams:
            yield streams


async def main(url: str, token: str, tool: str | None, args: dict) -> int:
    fallos = 0
    async with Client(_transport(url, token), mode="auto") as c:
        print(f"Servidor: {c.server_info.name} {c.server_info.version} · protocolo {c.protocol_version}")
        print(f"Instrucciones ({len(c.instructions or '')} car.):\n{c.instructions}")
        for t in (await c.list_tools()).tools:
            ro = t.annotations.read_only_hint if t.annotations else None
            raiz = t.input_schema.get("type")
            ok = ro is True and raiz == "object"
            fallos += not ok
            print(f"  {'✓' if ok else '✗'} {t.name}  solo lectura={ro}  esquema raíz={raiz}")
        if tool:
            r = await c.call_tool(tool, args)
            print(f"\n{tool} → is_error={r.is_error}")
            for part in r.content:
                print(getattr(part, "text", part))
            fallos += bool(r.is_error)
    return 1 if fallos else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    url, token = sys.argv[1], sys.argv[2]
    tool = sys.argv[3] if len(sys.argv) > 3 else None
    args = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    try:
        sys.exit(asyncio.run(main(url, token, tool, args)))
    except Exception as e:  # el SDK envuelve los fallos en grupos de excepciones
        while isinstance(e, BaseExceptionGroup) and e.exceptions:
            e = e.exceptions[0]
        sys.exit(f"No se pudo hablar con {url}: {e}")
