import subprocess
import webbrowser

# Directorio donde se encuentra el archivo optimizer_display_panel.py
working_directory = "C:\\Users\\jc_ce\\Desktop\\01Proyectos\\hermes\\cuadernos\\"

# Comando para iniciar la aplicación de Bokeh
command = f"bokeh serve {working_directory}optimizer_display_panel.py --show"

# Iniciar la aplicación de Bokeh en segundo plano
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Esperar a que la aplicación se inicie completamente
process.wait()

# Abrir la aplicación en el navegador predeterminado
url = "http://localhost:5006/test"
webbrowser.open(url)
