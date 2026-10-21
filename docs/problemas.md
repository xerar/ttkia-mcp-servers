# Problemas habituales

Casi todos los fallos se ven al pulsar **Test** en el perfil, que enseña el error tal como lo devuelve el servidor.

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| No aparece «External MCP servers» en el perfil | No tienes el permiso | Pídeselo a un administrador de TTKIA |
| Rechazo al dar de alta | URL `http://`, puerto distinto de 443, usuario en la URL, redirección o dirección interna | HTTPS público en el 443 y la URL exacta del endpoint, sin redirecciones |
| «requires authentication» | El servidor exige credenciales y no las has puesto (GitHub exige token siempre) | Añadir el token; si el proveedor pide iniciar sesión en su página, usar **Sign in** ([cómo](inicio-de-sesion.md)) |
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

## Inicio de sesión (OAuth)

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| «The browser blocked the sign-in window» | El navegador bloquea las ventanas emergentes de TTKIA | Permitirlas para TTKIA y pulsar **Sign in** otra vez |
| **Sign in** no se puede pulsar | Has escrito un token | Vaciar el campo del token: o token o inicio de sesión |
| «sign-in could not start: the server did not ask for sign-in» | El servidor no usa inicio de sesión | Darlo de alta con **Test** (y un token si lo pide) |
| «sign-in could not start» con otro motivo | El proveedor no publica sus metadatos o no admite registro dinámico de clientes | Si exige registrar antes una aplicación (Google, Microsoft 365), no se puede conectar. Ver [qué tiene que ofrecer el servidor](inicio-de-sesion.md#qué-tiene-que-ofrecer-el-servidor) |
| «the authorization page is not https» | El proveedor manda a una página sin HTTPS | No se puede conectar |
| «connection not allowed to …» | El servicio de autorización, el de token o el de registro está en una dirección interna o privada | No se puede conectar: todas sus direcciones tienen que ser públicas |
| «the sign-in expired or was not started» | Pasaron más de 10 minutos en la página del proveedor, o cerraste la ventana | Volver a pulsar **Sign in** |
| «browser sign-in is not available» | Falta configuración en TTKIA (el origen de la web) | Avisar a un administrador de TTKIA |
| Estado «sign in required» | La sesión caducó sin poder renovarse, o la retiraste en el proveedor | **Sign in** en la fila del servidor |
| «the sign-in has expired or was revoked» al responder | Lo mismo, visto en mitad de una respuesta | **Sign in** en el perfil y repetir la pregunta |

¿No está aquí? Abre una incidencia en este repositorio con el error que muestra el perfil.
