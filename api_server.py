import uvicorn
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# --- Modelo de datos para el prompt ---
# Esto asegura que el JSON que recibimos tenga la forma correcta
class AgentConfig(BaseModel):
    system_prompt: str

CONFIG_FILE = "config.json"

# --- Inicializar el archivo de configuración si no existe ---
try:
    with open(CONFIG_FILE, "r") as f:
        json.load(f)
except FileNotFoundError:
    with open(CONFIG_FILE, "w") as f:
        json.dump({"system_prompt": "Este es un prompt de prueba. Configúralo desde la UI."}, f, indent=2)

# --- Crear la aplicación FastAPI ---
app = FastAPI()

# --- Endpoint para guardar la configuración ---
@app.post("/api/configure")
async def save_configuration(config: AgentConfig):
    """
    Recibe el nuevo prompt del sistema y lo guarda en config.json
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config.model_dump(), f, indent=2)
        return {"status": "success", "message": "Configuración guardada"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Endpoint para leer la configuración actual ---
@app.get("/api/configure")
async def get_configuration():
    """
    Lee la configuración actual de config.json para mostrarla en la UI
    """
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
    return config_data

# --- Servir el archivo HTML (Frontend) ---
@app.get("/")
async def get_index():
    return FileResponse("index.html")

# --- Punto de entrada para correr el servidor ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)