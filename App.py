from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar', methods=['POST'])
def cargar_archivo():
    if 'archivo' not in request.files:
        return "No se seleccionó ningún archivo", 400
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return "Nombre de archivo vacío", 400
    
    if archivo and archivo.filename.endswith('.xml'):
        ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], 'configuracion.xml')
        archivo.save(ruta_guardado)
        return render_template('index.html', mensaje="¡Archivo cargado exitosamente!")
    else:
        return "Por favor, sube un archivo con extensión .xml", 400

if __name__ == '__main__':
    app.run(debug=True)