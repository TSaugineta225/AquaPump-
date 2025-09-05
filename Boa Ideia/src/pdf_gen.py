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

import tempfile
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PySide6.QtWidgets import QMessageBox, QFileDialog
import matplotlib.pyplot as plt

class PDF():
    def __init__(self):
        self.doc = SimpleDocTemplate('doc.pdf', pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.configuracao_dos_styles()
        self.Relatorio = []
        try:
            pdfmetrics.registerFont(TTFont('GastrolinaSignature', r'src\GastrolineSignature_PERSONAL_USE_ONLY.ttf'))
        except:
            pass  # Usar fonte padrão se a personalizada não estiver disponível

    def configuracao_dos_styles(self):

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

        self.rodape_style = ParagraphStyle(
            name='Rodape',
            fontName='Helvetica-Oblique',
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=2  # Direita
        )

    def adicionar_titulos(self, titulo_principal="Relatório do Sistema de Bombeamento"):
        self.Relatorio.append(Paragraph(titulo_principal, self.titulo))
        self.Relatorio.append(Spacer(1, 12))

    def adicionar_secao(self, titulo):
        self.Relatorio.append(Paragraph(titulo, self.subtitulo))

    def adicionar_conteudo(self, dados):
        tabela_dados = []
        cabecalho = ['Parâmetro', 'Valor', 'Unidade']
        tabela_dados.append(cabecalho)
        
        for param, (valor, unidade) in dados.items():
            tabela_dados.append([param, str(valor), unidade])
        
        tabela = Table(tabela_dados, colWidths=[3*inch, 2*inch, 1.5*inch])
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
        
        # Adicionar zebra pattern
        for i in range(1, len(tabela_dados)):
            if i % 2 == 0:
                estilo_tabela.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#d6dbdf'))
        
        tabela.setStyle(estilo_tabela)
        self.Relatorio.append(tabela)
        self.Relatorio.append(Spacer(1, 15))

    def adicionar_grafico(self, figura_matplotlib, largura=6*inch, altura=4*inch):
        """Adiciona um gráfico matplotlib ao PDF"""
        try:
            # Salvar figura temporariamente
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                figura_matplotlib.savefig(tmp.name, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
                tmp_path = tmp.name
            
            # Adicionar ao PDF
            img = Image(tmp_path, width=largura, height=altura)
            self.Relatorio.append(img)
            self.Relatorio.append(Spacer(1, 12))
            
            # Limpar arquivo temporário
            os.unlink(tmp_path)
        except Exception as e:
            print(f"Erro ao adicionar gráfico: {e}")

    def rodape(self, canvas, doc):
        canvas.saveState()
        largura, altura = A4
        
        # Adicionar logo se disponível
        try:
            canvas.drawImage(r"img\TS.jpg", 30, 5, width=60, height=50)
        except:
            pass
        
        # Adicionar texto do rodapé
        canvas.setFont('GastrolinaSignature', 10)
        canvas.setFillColor(colors.HexColor('#7f8c8d'))
        canvas.drawRightString(largura - 50, 30, 'Relatório gerado pelo AquaPump')
        
        # Adicionar linha decorativa
        canvas.setStrokeColor(colors.HexColor('#3498db'))
        canvas.setLineWidth(0.5)
        canvas.line(35, 45, largura - 35, 45)
        
        # Adicionar número da página
        canvas.setFont('Helvetica', 9)
        pagina = f"Página {doc.page}"
        canvas.drawCentredString(largura / 2, 20, pagina)
        
        canvas.restoreState()

    def gravar_pdf(self, caminho=None):
        try:
            if caminho is None:
                caminho, _ = QFileDialog.getSaveFileName(
                    None, "Salvar como PDF", "Relatório.pdf", "Arquivos PDF (*.pdf)"
                )
                if not caminho:
                    return False
            
            if not caminho.endswith('.pdf'):
                caminho += '.pdf'

            # Cria o documento com o caminho especificado
            doc = SimpleDocTemplate(caminho, pagesize=A4)

            doc.build(
                self.Relatorio,
                onFirstPage=self.rodape,
                onLaterPages=self.rodape
            )

            # Abre o PDF após gerar
            caminho_absoluto = os.path.abspath(caminho)
            webbrowser.open_new(f"file://{caminho_absoluto}")
            
            return True
        except Exception as e:
            QMessageBox.warning(None, "Aviso", f"Erro ao gerar PDF: {str(e)}")
            return False