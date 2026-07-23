# Consola de operaciones · Couriers AR

Dashboard estático (HTML + JS, sin backend) que se publica en **GitHub Pages** y se
actualiza solo **cada 5 minutos** mediante un **GitHub Action** que baja el CSV de origen,
lo transforma y lo guarda como `data.json` en el propio repo.

> Este diseño evita el problema de **CORS**: el navegador de los visitantes nunca llama al
> servidor externo. Quien baja el CSV es el Action (servidor a servidor, sin CORS), y la
> página lee `data.json` desde el mismo dominio de GitHub Pages.

## Estructura del repo

```
index.html                     ← el dashboard (lee ./data.json)
data.json                      ← lo regenera el Action (podés dejar el inicial que viene incluido)
assets/
  geo.json                     ← coordenadas por código postal (referencia, no cambia)
  part.json                    ← código postal → partido de Bs. As. (referencia, no cambia)
scripts/
  build_data.py                ← descarga el CSV y genera data.json (solo librería estándar)
.github/workflows/
  update-data.yml              ← corre build_data.py cada 5 min y commitea data.json
```

## Puesta en marcha (5 pasos)

1. Creá un repositorio nuevo en GitHub y subí **todos** estos archivos respetando las carpetas.
2. En **Settings → Actions → General → Workflow permissions**, elegí **Read and write permissions** y guardá. (Necesario para que el Action pueda commitear `data.json`.)
3. En **Settings → Pages**, en *Source* elegí **Deploy from a branch → `main` / `(root)`** y guardá.
4. Andá a la pestaña **Actions**, abrí *update-data* y tocá **Run workflow** una vez (para generar el primer `data.json`; después corre solo cada 5 min).
5. Abrí `https://TU-USUARIO.github.io/TU-REPO/`. Listo.

El dashboard muestra arriba a la derecha la hora de la última actualización y la hora de
los datos; además tiene un botón **Actualizar** para refrescar manualmente.

## Notas

- **Cadence real:** los `schedule` de GitHub Actions corren "best-effort"; a veces se demoran
  o se agrupan bajo carga. En la práctica se aproxima a 5 minutos, pero puede variar.
- **Inactividad:** si el repo no tiene actividad por 60 días, GitHub pausa los workflows
  programados. Cualquier commit los reactiva.
- **Fuente del CSV:** está fijada en `scripts/build_data.py` (`CSV_URL`). Si cambia la URL,
  editá esa constante.
- **Historial de git:** `data.json` (~0,9 MB) se commitea en cada corrida con cambios. Si te
  preocupa el crecimiento del historial a largo plazo, se puede migrar a *GitHub Pages con
  deploy por Actions* (`actions/deploy-pages`) para no versionar el archivo. Avisá y te paso
  esa variante.
