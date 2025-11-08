
## Proyecto: customagentlivekit

Este repositorio contiene un agente de voz basado en LiveKit Agents que usa plugins de STT/TTS/LLM (Deepgram, ElevenLabs, OpenAI y Silero). El agente utiliza un `config.json` para cargar el prompt del sistema y otras opciones (por ejemplo, el idioma de transcripción).

## Requisitos

- Python: >= 3.13 (ver `pyproject.toml`)
- Git (opcional)
- Acceso a las APIs correspondientes (Deepgram, ElevenLabs, OpenAI, LiveKit) y sus credenciales si quieres usar los servicios remotos.

## Instalación (local)

1. Clona el repositorio (si no lo hiciste ya):

```bash
git clone <repo-url>
cd customAgentLiveKit
```

2. Crea un entorno virtual y actívalo (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Actualiza pip e instala dependencias desde `pyproject.toml` usando pip (modo editable opcional):

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

Nota: también puedes usar tu gestor preferido (Poetry, pipx, pip) siempre que instales las dependencias listadas en `pyproject.toml`.

4. Crea un archivo `.env` con las variables de entorno necesarias para los plugins (por ejemplo claves/URLs). El proyecto usa `python-dotenv`, así que `.env` será cargado automáticamente al ejecutar `run_agent.py`.

Ejemplo mínimo de `.env` (modifica según tus credenciales):

```env
# LIVEKIT_URL or similar
# DEEPGRAM_API_KEY=your_deepgram_key
# ELEVENLABS_API_KEY=your_elevenlabs_key
# OPENAI_API_KEY=your_openai_key
```

## Configuración: `config.json`

El archivo `config.json` contiene el `system_prompt` que será pasado como instrucciones al agente, y otras opciones como `stt_language`.

Ejemplo relevante ya incluido en el repo:

```json
{
	"system_prompt": "...",
	"stt_language": "es"
}
```

- `system_prompt`: texto largo que define rol, personalidad y comportamiento del agente.
- `stt_language`: idioma o locale para la transcripción (p. ej. `"es"` o `"es-CO"`). Valor por defecto: `"es"`.

Si `config.json` no existe o no contiene estas claves, el script usa valores por defecto y mostrará una advertencia.

## Ejecutar localmente

Con el venv activado y las dependencias instaladas, ejecuta:

```bash
python3 run_agent.py
```

Esto iniciará el worker del agente. Asegúrate de tener las variables de entorno/capacidades necesarias para conectar a LiveKit y a los proveedores de STT/TTS/LLM.

## Personalización y pruebas

- Para cambiar el idioma de transcripción, edita `config.json` y ajusta `stt_language`.
- Para cambiar las instrucciones del agente, edita `system_prompt` en `config.json`.
- Si quieres depurar localmente, puedes agregar `print(AGENT_INSTRUCTIONS)` en `run_agent.py` antes de crear el `Agent`.

### Uso del script `setup.sh` (instalación rápida)

Puedes usar el instalador rápido para crear el entorno y descargar dependencias:

```bash
./setup.sh
```

Después, activa el entorno e inicia el agente:

```bash
source .venv/bin/activate
python3 run_agent.py
```

### Sobreescritura por variable de entorno

Si prefieres no editar `config.json`, puedes sobreescribir el idioma de transcripción mediante la variable de entorno `STT_LANGUAGE` (por ejemplo, `es-CO`):

```bash
export STT_LANGUAGE=es-CO
source .venv/bin/activate
python3 run_agent.py
```

El orden de prioridad para `STT_LANGUAGE` es:
1. Variable de entorno `STT_LANGUAGE` (si está definida)
2. `stt_language` en `config.json`
3. Valor por defecto `"es"`

## Depuración y problemas comunes

- Error de credenciales o conexión: revisa tu `.env` y las claves de API.
- El plugin STT no reconoce el parámetro `language`: verifica la versión del paquete `livekit-plugins-deepgram` y la firma del constructor (según `pyproject.toml` se requiere >=1.2.18).
- Mensaje de advertencia sobre `config.json`: si aparece, el archivo no fue leído correctamente; verifica permisos y formato JSON.
