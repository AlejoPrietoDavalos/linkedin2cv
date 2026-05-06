## Curriculum Automático a partir de los datos de Linkedin.
<img src="assets/photo_title.png" alt="Example output" style="max-width: 35%; height: auto;">

---

<img src="plots/files.png" alt="LinkedIn data files" style="max-width: 150px; width: 100%; height: auto;">
<p style="width: 100%"><em><b>Figura 1:</b> Muestra de los datos extraídos de LinkedIn.</em></p>

## Quickstart
#### Exportá tus datos de LinkedIna `.csv`
1. Exportar la data de tu perfil en Linkedin.
2. `Click en tu imágen > Ajustes y privacidad`.
3. `Privacidad de datos > Obtener una copia de tus datos`.
4. Click en "Descarga un archivo de datos más grande,...
5. Esperás un par de minutos/horas, y en el mismo lugar podés descargar los datos.
6. Poner dentro de `data/` y extraer.


#### Crear y editar el `.env`.
```bash
cp .env.example .env
```


#### Ejecutar el script.
```bash
# El CV se guarda en `data/`.
python3 main.py
```

Nota: si no tenés `ghostscript` (`gs`) instalado, el script genera el PDF igual y omite la compresión final.

#### Instalar Ghostscript (opcional, para comprimir el PDF final)
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y ghostscript

# Fedora
sudo dnf install -y ghostscript

# Arch Linux
sudo pacman -S ghostscript

# macOS (Homebrew)
brew install ghostscript
```
