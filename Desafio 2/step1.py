from bs4 import BeautifulSoup
import requests
import pandas as pd
import tabula
import zipfile

def downloadPDF(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

count = 1
for link in pdf_links:
    if 'Anexo' in link.text: 
        pdf_url = link['href']
        filename = f'Anexo {count}.pdf'  
        downloadPDF(pdf_url, filename)
        count += 1  
    
print("Extração realizada com sucesso!")

def gettable(pdf_file):
    tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
    
    df_list = []
    for table in tables:
        df_list.append(table)  
    df = pd.concat(df_list)
    
    return df

pdf_file_anexo1 = 'Anexo 1.pdf' 

anexo1_df = gettable(pdf_file_anexo1)
anexo1_df.rename(columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=True)
csv_filename = 'dados_anexo1.csv'
anexo1_df.to_csv(csv_filename, index=False)
print(f'Dados extraídos do Anexo I e salvos em {csv_filename}')

zip_filename = 'Teste_Pedro_italo_Campos.zip'

with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(csv_filename)

print(f'Arquivo CSV adicionado ao arquivo ZIP: {zip_filename}')
