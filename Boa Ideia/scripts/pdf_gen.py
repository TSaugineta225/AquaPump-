import os
import webbrowser
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PySide6.QtWidgets import QMessageBox

class PDF():
    def __init__(self):
        self.doc = SimpleDocTemplate('doc.pdf', pagesize=A4)
        self.configuracao_dos_sytles()
        self.Relatorio = []
        pdfmetrics.registerFont(TTFont('GastrolinaSignature', r'scripts\GastrolineSignature_PERSONAL_USE_ONLY.ttf'))

    def configuracao_dos_sytles(self):
        self.titulo = ParagraphStyle(
            name='Titulos',
            fontName='Courier-Bold',
            fontSize=12,
            leading=30,
            textColor='black',
            alignment=TA_JUSTIFY
        )
        self.subtitulo = ParagraphStyle(
            name='Subtitulos',
            fontName='Courier-Bold',
            fontSize=11,
            leading=20,
            textColor='black',
            alignment=TA_JUSTIFY
        )
        self.corpo = ParagraphStyle(
            name='Corpo',
            fontName='Courier',
            fontSize=10,
            leading=12,
            textColor='black',
            alignment=TA_JUSTIFY
        )

    def adicionar_titulos(self):
        self.Relatorio.append(Paragraph("Bombas Centrifugas", self.titulo))
        self.Relatorio.append(Spacer(1, 12))
        self.Relatorio.append(Paragraph("Dados do Projeto", self.subtitulo))
        self.Relatorio.append(Spacer(1, 12))

    def adicionar_conteudo(self, vazao, tempo, D):
        self.Relatorio.append(Spacer(1, 12))
        
        tabela = Table([
        ['Parametros', 'Resultados', 'Unidades'],
        ['Vazão total da bomba', vazao, 'm³/h'],
        ['Tempo de Funcionamento da Bomba', tempo, 'h'],
        ['Diâmetro de Sucção', D, 'mm'],
        ['Material da Tubulação', "None", 'None'],
        ['Perdas de Cargas Distribuidas na Linha de Sucção ', 'None', 'm'],
        ['Perdas de Cargas Distribuidas na Linha de Recalque', 'None', 'm'],
        ['Potência  da Bomba  ', "None", 'CV'],
        ['Rendimento da Bomba ', 'None', '%'],
    ]
)
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.ghostwhite),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME',  (0, 1), (-1, -1), 'Courier'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabela.setStyle(estilo_tabela)
        self.Relatorio.append(tabela)

    def adicionar_imagem(self, caminho_imagem):
        if os.path.exists(caminho_imagem):
            img = Image(caminho_imagem, width=350, height=300)
            self.Relatorio.append(Spacer(1, 5))
            self.Relatorio.append(Paragraph("Grafico da Associação  de Bombas", self.subtitulo))
            self.Relatorio.append(img)
  
    def rodape(self, canvas, doc):
        largura, altura = A4
        canvas.drawImage(r"img\TS.jpg", 30, 5, width=60, height=50)
        canvas.setFont('GastrolinaSignature', 12)
        canvas.drawRightString(largura - 50, 30, 'Obrigado por usar nosso programa ')
        canvas.line(35, 45, largura - 45, 45)

    def gravar_pdf(self):
        try:
            self.doc.build(self.Relatorio, onLaterPages=self.rodape, onFirstPage=self.rodape)
            caminho_absoluto = os.path.abspath('doc.pdf')
            webbrowser.open_new(f"file://{caminho_absoluto}")
        except Exception as e:
            QMessageBox.warning(None, "Aviso", f"Erro ao gerar PDF: {str(e)}")
