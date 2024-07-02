import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # flask_cors 모듈에서 CORS를 가져옵니다
import crawling
import htmlRepository as HtmlRepository
from bs4 import BeautifulSoup
import requests
import time
from auth import *

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/search": {"origins": "*"}})

@app.route('/search', methods=['GET'])
def getRegistPage():
    htmlRepository = HtmlRepository.HtmlRepository()

    # ------------------------------------------------------- 스크래핑 -------------------------------------------------------
    documentNumber = request.args.get('no')
    if htmlRepository.isExist(documentNumber):
        with open('scrapped/' + documentNumber + '.html.html', 'r', encoding='utf-8') as file:
            original = file.read()
    else:
        original = crawling.getOriginal(documentNumber)
    print("스크랩 완료")

    # ------------------------------------------------------- 편집 -------------------------------------------------------
    soup = BeautifulSoup(original, 'html.parser')
    body = str(soup.body)
    body = body.replace('\n  ', '')
    body = body.replace('</a>     <a', '</a>\n<a')
    body = body.replace('</a> <a ', '</a>\n<a')
    body = body.replace('</a>          <a ', '</a>\n<a')
    body = body.replace('     ', ' ')
    body = body.replace('    ', ' ')
    file = open("edited/" + documentNumber + ".html","w",encoding="utf-8")
    file.write(body)
    print("편집 완료")

    # ------------------------------------------------------- 번역 -------------------------------------------------------
    if not os.path.exists('translated/' + documentNumber + '.html'):
        translate(documentNumber, "KO")
        print("번역 완료")

    if os.path.exists('translated/' + documentNumber + '.html'):
        print("이미 번역됨")
        with open('translated/' + documentNumber + '.html', 'r', encoding='utf-8') as file:
                translated = file.read()
                return jsonify({'success': True, 'original': original, 'translated': translated})
    else: 
        return jsonify({'success': False, 'original': original})

def translate(documentNumber, target_lang):    
    # HTML 파일 읽기
    with open("edited/" + documentNumber + ".html", 'r', encoding='utf-8') as file:
        html_content = file.read()
        
    # DeepL API에 요청
    url = "https://api.deepl.com/v2/document"
    headers = {
        'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}'
    }
    files = {
        'file': ('input.html', html_content, 'text/html')
    }
    data = {
        'source_lang': 'EN',
        'target_lang': target_lang,
    }
    
    response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        document_id = response.json()['document_id']
        document_key = response.json()['document_key']
        print(document_id, " " ,document_key)
        # 번역 상태 확인
        status_url = f"https://api.deepl.com/v2/document/{document_id}"
        status_headers = {
            'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
            'Content-Type': 'application/json'
        }
        status_data = {
            'document_key': document_key
        }
        
        # 상태가 'done'이 될 때까지 대기
        while True:
            status_response = requests.post(status_url, headers=status_headers, json=status_data)
            if status_response.status_code == 200:
                status_result = status_response.json()
                if 'status' in status_result:
                    if status_result['status'] == 'done':
                        break
                    elif status_result['status'] == 'error':
                        print("번역 중 오류 발생:", status_result)
                        return
                else:
                    print("오류: 상태 응답에서 'status'를 찾을 수 없습니다.")
                    return
            else:
                print("상태 확인 오류:", status_response.status_code, status_response.text)
                return
            
            time.sleep(2)
        
        # 번역된 파일 다운로드
        download_url = f"https://api.deepl.com/v2/document/{document_id}/result"
        download_response = requests.get(download_url, headers=status_headers, params=status_data)
        
        if download_response.status_code == 200:
            with open("translated/" + documentNumber + ".html", 'w', encoding='utf-8') as file:
                corrected_text = download_response.text.encode('latin1').decode('utf-8')
                file.write(corrected_text)
        else:
            print("번역 파일 다운로드 오류:", download_response.status_code, download_response.text)
    elif response.status_code == 403:
        print("Forbidden: API 키와 구독 레벨을 확인해주세요.")
    else:
        print("오류:", response.status_code, response.text)

# 실행 ---------------------------------------------------------
if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=False, threaded=True)