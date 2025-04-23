#Autoria: Rodrigo Henrique Schernovski
import barcode as barcode_module
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
import os


class BarcodePF(object):
    def __init__(self, patrimonio : str):
        
        self.patrimonio = patrimonio  # Número do patrimônio em string
        self.path = "etiquetas_geradas/"                # Para salvar os arquivos em outro diretório
        
        self.png_name = os.path.join(self.path, f'codigo_de_barras_{patrimonio}') # Nome do código de barras em .png
        self.pdf_name =  os.path.join(self.path, f'codigo_de_barras_{patrimonio}') # Nome do código de barras em .pdf
        
        self.DPI = 300                                          # DPI do código de barras final
        self.largura_mm = 50                                    # Largura da etiqueta em mm
        self.altura_mm = 23                                     # Altura da etiqueta em mm
        self.texto = "POLÍCIA FEDERAL"                          # Texto da etiqueta
        
        # futuramente colocar mais dados na etiqueta, como denominacao, modelo, serie

        self.gerar_codigo_de_barras()
        self.criar_pdf()
        
    def gerar_codigo_de_barras(self):

        width = 0.25                      # Largura do código de barras
        height = 8.75                     # Altura do código de barras

        # Configurações do ImageWriter para esticar e encurtar o código de barras
        writer = ImageWriter()

        # Cria o objeto do código de barras no formato Code 39
        code39 = barcode_module.codex.Code39(self.patrimonio, writer=writer, add_checksum=False)

        # Salva a imagem do código de barras em um arquivo
        options = {
                    'write_text': False,
                    "module_width":  width, 
                    "module_height": height, 
                    "quiet_zone": 5,
                    'dpi' : 250}

        filename_temp = code39.save(f"{self.png_name}_temp", options) # Arquivo temporário com o código de barras code39
        
        self.add_margins(filename_temp) # Adicionar margens no código de barras e salva em png
 
 
    def add_margins(self, filename):
        # Abre o arquivo temporário com o código de barras para adição de margens
        img = Image.open(f"{filename}")

        # Converte as dimensões para pixels
        nova_largura = int(self.largura_mm * self.DPI / 25.4)  # Largura total em pixels
        nova_altura = int(self.altura_mm * self.DPI / 25.4)    # Altura total em pixels

        # Cria uma nova imagem com as dimensões corretas
        self.nova_img = Image.new("RGB", (nova_largura, nova_altura), "white")

        # Adiciona margens e posiciona o code39 no centro
        dx = 14
        dy = -8
        pos_x = (nova_largura - img.width) // 2 + dx
        pos_y = (nova_altura - img.height) // 2 + dy
        self.nova_img.paste(img, (pos_x, pos_y))
        ImageDraw.Draw(self.nova_img) 

        self.nova_img.save(f"{self.png_name}.png") # Salva a imagem final com o código de barra e as margens
        os.remove(filename)                    # Remove o arquivo temporário

        
    def criar_pdf(self):
        ###########################################

        # Converte as dimensões de mm para pontos (1 mm = 2.83465 pontos)
        pdf_width_pts = self.largura_mm * mm
        pdf_height_pts = self.altura_mm * mm

        # Cria o canvas do PDF com o tamanho exato da imagem
        pdf_canvas = canvas.Canvas(f"{self.pdf_name}.pdf", pagesize=(pdf_width_pts, pdf_height_pts))

        # Adiciona a imagem png ao PDF (com as margens)
        pdf_canvas.drawImage(f"{self.png_name}.png", 0, 0, width=pdf_width_pts, height=pdf_height_pts)
        pdf_canvas.setFont("Helvetica-Bold", 7)  # Nome da fonte e tamanho
        
        largura = pdfmetrics.stringWidth(self.texto, "Helvetica-Bold", 7) # Largura do texto
        dx = 14 # Para ajuste de posicionamento
        
        # Escreve texto na posição definida
        pdf_canvas.drawString( 72/self.DPI * (self.nova_img.width/2 + dx) - largura/2, 48, self.texto) 

    
        pdf_canvas.setFont("Helvetica", 9)  # Nova fonte para o patrimônio
        pdf_canvas.drawString( 18, 15, self.patrimonio) # Posiciona o texto manualmente

        # Salva o PDF na pasta etiquetas_geradas
        pdf_canvas.showPage()
        pdf_canvas.save()
        
        os.remove(f"{self.png_name}.png")                    # Remove o arquivo png


def ler_txt(arquivo):
    """
    Lê um arquivo de texto e retorna uma lista de números inteiros.
    Cada linha do arquivo deve conter um número inteiro.
    """
    with open(arquivo, 'r', encoding='utf-8-sig') as f:
        linhas = f.readlines()
    patrimonios = [linha.strip() for linha in linhas] # Remove espaços em branco e quebras de linha
    print(patrimonios)
    return patrimonios



if __name__ == '__main__':
    arquivo_origem_txt = 'SETEC_p1.txt' # Nome do arquivo txt com os patrimônios'
    patrimonios = ler_txt(f'txt_etiquetas/{arquivo_origem_txt}') # Lê o arquivo txt com os patrimônios
    #patrimonios = [2025009535, 2025009536, 2025009537]
    for patrimonio in patrimonios:
        patrimonio = str(patrimonio)
        print(f"Gerando código de barras para o patrimônio {patrimonio}")
        barcode = BarcodePF(patrimonio)
        print(f"Código de barras gerado com sucesso!")
        #concatenar_etiquetas_individuais()