# Aportar un ejemplo

Si has convertido un script en un servidor MCP y puede servirle a otros, súbelo a [`ejemplos/`](ejemplos/). Este repositorio es **público**: lo que entra aquí lo puede leer cualquiera, y aunque se borre después queda en el historial. Por eso nada llega a `main` sin pasar la revisión automática y la de una persona.

## Lo que nunca puede ir

- Nombres de clientes, de sus sedes o de sus proyectos.
- Direcciones IP internas o privadas, ni nombres de máquinas internas.
- Credenciales, tokens o claves, tampoco de laboratorio ni «de prueba» reales.
- Configuraciones reales, salidas de equipos, inventarios o volcados de un gestor.
- Capturas con cualquiera de lo anterior.

Las credenciales y direcciones se leen de variables de entorno y se documentan en un `.env.example` **vacío**. Para los ejemplos de uso, nombres inventados: `mcp.tudominio.com`, `equipo-01`, `cliente-ejemplo`.

## Cómo proponerlo

1. Haz tu copia del repositorio (*Fork* en GitHub). No hace falta pedir permisos.
2. Copia `plantilla/` a `ejemplos/<nombre>/`, en minúsculas y con guiones (`ejemplos/certificados-tls`, `ejemplos/estado-bgp`).
3. Adapta las partes 1, 2 y 3 de `src/main.py`, como explica [la guía](docs/servidor-propio.md).
4. Escribe el `README.md` del ejemplo (abajo, qué debe contar).
5. Pruébalo en local con `probar.py`: todas las herramientas tienen que salir con ✓.
6. Abre una *pull request* contra `main` y rellena la lista de comprobación.

## Estructura de un ejemplo

```text
ejemplos/<nombre>/
├── README.md          qué hace, qué necesita, quién lo mantiene
├── src/main.py
├── requirements.txt   versiones fijadas
├── Dockerfile
├── .env.example       variables que necesita, vacías
└── prueba.json        opcional: la llamada que hace la revisión automática
```

`prueba.json` dice qué herramienta llamar y con qué argumentos:

```json
{"herramienta": "cert_expiry", "argumentos": {"host": "github.com"}}
```

Ponlo solo si la herramienta funciona sin credenciales (por ejemplo, contra un servicio público). Si necesita acceso a un sistema, déjalo fuera: la revisión arrancará el servidor y comprobará sus herramientas sin llamarlas.

El servidor tiene que **arrancar solo con `MCP_AUTH_TOKEN`**. Si le faltan otras variables, que lo diga al llamar a la herramienta (con `status: error` y qué falta), no al arrancar.

## README del ejemplo

- **Qué hace**, en una frase, y una o dos preguntas de TTKIA que responde.
- **Herramientas** que publica, una línea cada una.
- **Qué necesita**: variables de entorno, permisos (siempre de solo lectura) y a qué sistema se conecta.
- **Quién lo mantiene**: tu usuario de GitHub. Un ejemplo que se rompe y nadie mantiene se retira.

## Qué se revisa

**Automáticamente**, en cada *pull request*:

- que no haya secretos en ningún commit (gitleaks);
- que no haya direcciones IP internas o privadas;
- que el ejemplo tenga la estructura de arriba, arranque, exija token (401 sin él), publique solo herramientas de solo lectura con esquema `object` y, si tiene `prueba.json`, que la llamada funcione;
- que la imagen Docker se construya.

**Una persona** comprueba además:

- que las herramientas son de solo lectura de verdad, no solo declaradas;
- que las instrucciones dicen con claridad cuándo usarlo y cuándo no;
- que no se cuela nada de la lista de arriba que la revisión automática no ve (un nombre de cliente, una captura).
