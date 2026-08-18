# Consola de operaciones · Couriers AR

Dashboard estatico (HTML + JS, sin backend) que se publica en **GitHub Pages** y se
actualiza solo **cada 5 minutos** mediante un **GitHub Action** que baja el CSV de origen,
lo transforma y lo guarda como `data.json` en el propio repo.

> Este diseno evita el problema de **CORS**: el navegador de los visitantes nunca llama al
> servidor externo. Quien baja el CSV es el Action (servidor a servidor, sin CORS), y la
> pagina lee `data.json` desde el mismo dominio de GitHub Pages.

## Estructura del repo (solo 4 archivos)

```
index.html                          el dashboard (lee ./data.json)
data.json                           lo regenera el Action (dashboard, liviano)
export.csv                          lo regenera el Action (una fila por pedido; lo usa el boton Exportar Excel)
scripts/build_data.py               descarga el CSV y genera data.json + export.csv
.github/workflows/update-data.yml   corre build_data.py cada 5 min y commitea data.json
```

## Puesta en marcha

1. Crea un repositorio **publico** en GitHub y subi estos archivos respetando las carpetas.
2. **Settings > Actions > General > Workflow permissions**: elegi **Read and write permissions** y guarda.
3. **Settings > Pages > Source**: **Deploy from a branch**, rama `main`, carpeta `/ (root)`, Save.
4. Pestana **Actions** > **update-data** > **Run workflow** (una vez; despues corre solo cada 5 min).
5. Abri `https://TU-USUARIO.github.io/TU-REPO/`.

## Notas

- La cadencia de los `schedule` de GitHub Actions es best-effort: puede demorarse algunos minutos.
- Si el repo no tiene actividad por 60 dias, GitHub pausa los workflows programados.
- La URL del CSV esta en `scripts/build_data.py` (constante `CSV_URL`).
- El workflow incluye un paso **Diagnostico** que lista los archivos del repo: si algo falla,
  el log muestra que archivos existen realmente.
