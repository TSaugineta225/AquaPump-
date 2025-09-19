from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup

class Animações():
    def __init__(self):
        self.animacoes_ativas = []

    def largura(self, frame, botao=None, largura_alvo=280, duracao=300):

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

        animacao = QPropertyAnimation(frame, b"minimumWidth")
        animacao.setDuration(duracao)
        animacao.setStartValue(largura_atual)
        animacao.setEndValue(nova_largura)
        animacao.setEasingCurve(QEasingCurve.OutCubic)

        self.animacoes_ativas.append(animacao)
        animacao.finished.connect(lambda: self.animacoes_ativas.remove(animacao))

        animacao.start()


    def altura(self, frame, altura=400, duracao=300):
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

    def largura_altura(self, frame, frame_2, botao=None, largura_alvo=300, altura=400, duracao=300):
        largura_atual = frame.width()
        altura_atual = frame_2.height()

        if largura_atual == 0:  
            nova_largura = largura_alvo
            nova_altura = altura
            if botao:
                botao.setHidden(True)
        else:  
            nova_largura = 0
            nova_altura = 0
            if botao: 
                botao.setHidden(False)

        # Animação de largura
        animacao_largura = QPropertyAnimation(frame, b"minimumWidth")
        animacao_largura.setDuration(duracao)
        animacao_largura.setStartValue(largura_atual)
        animacao_largura.setEndValue(nova_largura)
        animacao_largura.setEasingCurve(QEasingCurve.OutCubic)

        # Animação de altura (com a mesma duração para sincronia)
        animacao_altura = QPropertyAnimation(frame_2, b"maximumHeight")
        animacao_altura.setDuration(duracao) 
        animacao_altura.setStartValue(altura_atual)
        animacao_altura.setEndValue(nova_altura)
        animacao_altura.setEasingCurve(QEasingCurve.OutCubic)

        # Grupo de animação
        if hasattr(self, 'animacao_grupo') and self.animacao_grupo.state() == QSequentialAnimationGroup.Running:
            self.animacao_grupo.stop()

        self.animacao_grupo = QSequentialAnimationGroup()
        self.animacao_grupo.addAnimation(animacao_largura)
        self.animacao_grupo.addAnimation(animacao_altura)

        self.animacao_grupo.start()