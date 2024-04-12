from flask import Flask
from flask import request
from flask import Response
from flask import jsonify # Return json form to client
import crawling
import htmlRepository as HtmlRepository
import base64

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def getRegistPage():
    documentNumber = request.args.get('no')
    original = crawling.getOriginal(documentNumber)

    path = "/htmls/" + documentNumber + ".html"
    htmlRepository = HtmlRepository.HtmlRepository()
    htmlRepository.saveOriginalHtml(documentNumber, path)

    return jsonify({'original': original, 'translated':""})

# 실행 ---------------------------------------------------------
if __name__ == '__main__':
    app.run('0.0.0.0',port=8000, debug=True, threaded=True)