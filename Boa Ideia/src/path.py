import os

class Path:
    def caminho_dados(self, caminho_relactivo):
        """Garante que os arquivos sejam carregados tantos nos testes de python como .exe"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, caminho_relactivo)
        return os.path.join(os.path.abspath("."), caminho_relactivo)