from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QObject, Signal

class VerificadorConexaoInternet(QObject):
    conexao_finalizada = Signal(bool)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self._resposta)

    def verificar(self):
        url = QUrl("https://clients3.google.com/generate_204") 
        requisicao = QNetworkRequest(url)
        self.manager.get(requisicao)

    def _resposta(self, reply):
        conectado = not reply.error()
        self.conexao_finalizada.emit(conectado)
        reply.deleteLater()
