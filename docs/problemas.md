# Problemas habituales

Casi todos los fallos se ven al pulsar **Test** en el perfil, que enseña el error tal como lo devuelve el servidor.

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| No aparece «External MCP servers» en el perfil | No tienes el permiso | Pídeselo a un administrador de TTKIA |
| Rechazo al dar de alta | URL `http://`, puerto distinto de 443, usuario en la URL, redirección o dirección interna | HTTPS público en el 443 y la URL exacta del endpoint, sin redirecciones |
| «requires authentication» | El servidor exige token y no lo has puesto (GitHub lo exige siempre) | Añadir el token; si solo admite OAuth, hoy no se puede dar de alta |
| «the token was rejected» | Token no válido o caducado; en tu servidor, no coincide con `MCP_AUTH_TOKEN` | Revisar el token o el `.env` del servidor y volver a darlo de alta |
| «access denied» | El token no tiene permisos para eso | Ampliar los permisos de lectura del token |
| Tu servidor no arranca: «MCP_AUTH_TOKEN vacío» | Falta el token en el `.env` | Añadirlo y volver a arrancar |
| El contenedor sale como `unhealthy` | El `HEALTHCHECK` apunta a otro puerto | Mismo puerto en `EXPOSE`, `HEALTHCHECK` y el servidor |
| Tu servidor rechaza la petición por la cabecera Host | Falta `host="0.0.0.0"` en `streamable_http_app` | Añadirlo |
| Herramienta bloqueada al probar | No declara `read_only_hint=True` | Declararlo si de verdad solo lee; si escribe, no se puede usar |
| Ninguna herramienta activable | El servidor no declara anotaciones | No se puede usar como servidor externo |
| Estado «changed — review» | El servidor cambió sus herramientas o instrucciones | **Review** en el perfil y aprobar de nuevo |
| No se usa en las respuestas | No responde, está en «changed» o desactivado, o sus instrucciones no dejan claro cuándo usarlo | Mirar el estado y el último error en el perfil; mejorar «Cuándo usarlo» |
| Error por tiempo | La herramienta tarda más de 30 s | Que devuelva antes, aunque sea un resultado parcial |
| Respuesta cortada | Supera los 150.000 caracteres | Filtrar o paginar en el servidor |
| «SSE stream ended without a response» | Respuesta de más de 1 MiB en un solo evento | Usar herramientas o argumentos que devuelvan menos |

¿No está aquí? Abre una incidencia en este repositorio con el error que muestra el perfil.
