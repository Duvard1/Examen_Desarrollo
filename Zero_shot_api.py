from transformers import pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

history = []

@app.route('/clasificar', methods=['POST'])
def classify_text():
    data = request.get_json()
    codigo = data.get('codigo','')
    texto = data.get('valor', '')
    candidate_labels = ['Política', 'Religión', 'Cine']

    if not texto or not candidate_labels:
        return jsonify({'error': 'Debe proporcionar texto y etiquetas para clasificar'}), 400

    resultado_clasificacion = classifier(texto, candidate_labels)
    labels_scores = {label: score for label, score in zip(resultado_clasificacion['labels'], resultado_clasificacion['scores'])}
    
    if not labels_scores:
        return jsonify({'mensaje':"No puedo generar una etiqueta por que solo tengo el entrenamiento en politica, religión y cine"})    
    
    resultado = {'codigo':codigo, 'respuesta':labels_scores}
    history.append(resultado)

    return jsonify({'resultado': resultado, 'historial':history})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)
