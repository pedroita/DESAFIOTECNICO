from bs4 import BeautifulSoup
import requests
import zipfile
import os

def downloadpdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

pdf_files = []  

count = 1
for link in pdf_links:
    if 'Anexo I' in link.text: 
        pdf_url = link['href']
        filename = f'Anexo {count}.pdf'  
        downloadpdf(pdf_url, filename)
        pdf_files.append(filename)
        print("Anexo: ",count,"BAIXADO!!" )
        count += 1  
 

pdf_files_absolute = [os.path.abspath(filename) for filename in pdf_files]

zip_filename = 'arquivos_compactados.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for pdf_file in pdf_files_absolute:
        zipf.write(pdf_file, os.path.basename(pdf_file))
    print("Arquivos compatado!")

print ("Programa Finalizado!")
