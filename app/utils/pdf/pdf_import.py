import tempfile
import os
import webbrowser

def abrir_documento(self):
    if not self.id_seleccionado:
        return

    binario = self.datos_documentos.get(self.id_seleccionado)
    if not binario:
        return

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(binario)
        ruta_temp = tmp.name

    # Abrir archivo (Windows)
    try:
        os.startfile(ruta_temp)  # Solo en Windows
    except AttributeError:
        webbrowser.open_new(ruta_temp)  # En otros SO
