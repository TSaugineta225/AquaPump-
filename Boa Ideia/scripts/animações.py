from PySide6.QtCore import QPropertyAnimation, QEasingCurve

class Animações():
    def __init__(self):
        self.animacoes_ativas = []

    def largura(self, frame, botao=None, largura_alvo=280, duracao=300):
        """
        Anima a largura de um frame, ocultando ou mostrando um botão opcional.

        Parâmetros:
        - frame: QWidget (o container cuja largura será animada)
        - botao: QPushButton ou outro widget (opcional) a ocultar/mostrar junto
        - largura_alvo: int (largura ao expandir)
        - duracao: int (tempo da animação em milissegundos)
        """
        largura_atual = frame.width()

        # Determina se está aberto ou fechado
        if largura_atual == 0:
            nova_largura = largura_alvo
            if botao:
                botao.setHidden(True)
        else:
            nova_largura = 0
            if botao:
                botao.setHidden(False)

        animacao = QPropertyAnimation(frame, b"maximumWidth")
        animacao.setDuration(duracao)
        animacao.setStartValue(largura_atual)
        animacao.setEndValue(nova_largura)
        animacao.setEasingCurve(QEasingCurve.OutCubic)

        # Armazena a referência para evitar garbage collection
        self.animacoes_ativas.append(animacao)

        # Remove do histórico quando terminar
        animacao.finished.connect(lambda: self.animacoes_ativas.remove(animacao))

        animacao.start()


    def altura(self, frame, altura=140, duracao=300):
        height = frame.height()
        
        if height == 0:
            newHeight = altura

        else:
            newHeight = 0
        
        self.animacao_2 = QPropertyAnimation(frame, b"maximumHeight")
        self.animacao_2.setDuration(duracao) 
        self.animacao_2.setStartValue(height)
        self.animacao_2.setEndValue(newHeight)
        self.animacao_2.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao_2.start()

