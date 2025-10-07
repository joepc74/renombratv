# RenombraTV

RenombraTV es una utilidad en Python para renombrar archivos de series/TV usando metadata detectada por `guessit` y acceso opcional a TMDb para obtener títulos y detalles. Está pensada para organizar descargas de episodios con un patrón consistente.

## Contenido del repositorio

- `renombratv.py` - Script principal que realiza el renombrado.
- `renombratv.ini` - Archivo de configuración (opciones como patrones de nombre, API key de TMDb, etc.).
- `requirements.txt` - Dependencias Python necesarias.

## Requisitos

- Python 3.8+ (recomendado 3.10+)
- Windows, macOS o Linux

Dependencias (tal como aparecen en `requirements.txt`):

- guessit==3.8.0
- pick==2.4.0
- tmdbsimple==2.9.1

## Instalación

1. Clona o descarga el repositorio.
2. Abre PowerShell y navega a la carpeta del proyecto:

```powershell
cd e:\codigo\renombratv
```

3. (Opcional) Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

## Configuración

Crea un archivo `renombratv.ini` usando esta plantilla:

```
[General]
tmdbapikey = [KEY_API_TMDB]
carpeta_destino=[RUTA_DESTINO_DE_LOS_ARCHIVOS_RENOMBRADOS]
```

## Uso

Ejecuta el script desde PowerShell:

```powershell
python renombratv.py
```

## Consideraciones y edge cases

- Archivos con nombres ambiguos pueden ser mal identificados por `guessit`.
- Si usas la API de TMDb, cuida la cuota de peticiones y añade tu `tmdb_api_key` en el ini.

## Contribuciones

Si quieres mejorar el script, abre un issue o crea un pull request. Incluye pruebas y descríbenos el comportamiento.
