import numpy as np
import plotly.graph_objects as go
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import tempfile
import os
import base64

class GraficoPlotly(QWidget):
    def __init__(self, tipo='altura', potencia='Kw', altura='m', v='vazao', perdas=0.003, 
                 vazao_nominal=4, altura_nominal=4, parent=None):
        super().__init__(parent)

        self.tipo = tipo.lower()
        self.potencia = potencia
        self.altura = altura
        self.vazao = v
        self.Q_nominal = vazao_nominal
        self.H_nominal = altura_nominal
        self.H_geometrico = altura_nominal
        self.perda_carga = perdas

        self.H_0 = self.H_nominal * 1.2
        self.A = (self.H_0 - self.H_nominal) / (self.Q_nominal ** 2) if self.Q_nominal > 0 else 0

        # Configurar o widget web para exibir o gráfico Plotly
        self.web_view = QWebEngineView()
        
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.web_view)
        self.setLayout(layout_principal)

        # Carregar Plotly.js localmente
        self.plotly_js = self.carregar_plotly_js()
        
        # Manter referência ao arquivo temporário
        self.temp_file = None
        
        self.gerar_dados()
        self.plotar()

    def carregar_plotly_js(self):
        """Carrega o Plotly.js localmente para evitar dependência de CDN"""
        try:
            # Tenta carregar de um arquivo local primeiro
            plotly_path = os.path.join(os.path.dirname(__file__), 'plotly-2.24.1.min.js')
            if os.path.exists(plotly_path):
                with open(plotly_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        
        # Fallback: código mínimo do Plotly (versão reduzida)
        return """
        // Código mínimo do Plotly (versão extremamente reduzida)
        window.Plotly = {
            newPlot: function(divId, data, layout) {
                const div = document.getElementById(divId);
                if (!div) return;
                
                // Implementação básica de gráfico de linha
                const canvas = document.createElement('canvas');
                canvas.width = div.clientWidth;
                canvas.height = div.clientHeight;
                div.appendChild(canvas);
                
                const ctx = canvas.getContext('2d');
                
                // Desenhar eixos
                ctx.strokeStyle = '#000';
                ctx.beginPath();
                ctx.moveTo(50, 30);
                ctx.lineTo(50, canvas.height - 30);
                ctx.lineTo(canvas.width - 30, canvas.height - 30);
                ctx.stroke();
                
                // Desenhar dados (implementação simplificada)
                if (data && data.length > 0) {
                    for (let i = 0; i < data.length; i++) {
                        const trace = data[i];
                        if (trace.type === 'scatter' && trace.mode === 'lines') {
                            ctx.beginPath();
                            ctx.strokeStyle = trace.line?.color || '#000';
                            ctx.lineWidth = trace.line?.width || 2;
                            
                            const xValues = trace.x;
                            const yValues = trace.y;
                            
                            if (xValues && yValues && xValues.length === yValues.length) {
                                const xRange = Math.max(...xValues) - Math.min(...xValues);
                                const yRange = Math.max(...yValues) - Math.min(...yValues);
                                
                                const xScale = (canvas.width - 80) / (xRange || 1);
                                const yScale = (canvas.height - 60) / (yRange || 1);
                                
                                for (let j = 0; j < xValues.length; j++) {
                                    const x = 50 + (xValues[j] - Math.min(...xValues)) * xScale;
                                    const y = canvas.height - 30 - (yValues[j] - Math.min(...yValues)) * yScale;
                                    
                                    if (j === 0) {
                                        ctx.moveTo(x, y);
                                    } else {
                                        ctx.lineTo(x, y);
                                    }
                                }
                                
                                ctx.stroke();
                            }
                        } else if (trace.type === 'scatter' && trace.mode === 'markers+text') {
                            // Desenhar marcadores
                            const x = 50 + (trace.x[0] - Math.min(...data[0].x)) * ((canvas.width - 80) / (Math.max(...data[0].x) - Math.min(...data[0].x) || 1));
                            const y = canvas.height - 30 - (trace.y[0] - Math.min(...data[0].y)) * ((canvas.height - 60) / (Math.max(...data[0].y) - Math.min(...data[0].y) || 1));
                            
                            ctx.beginPath();
                            ctx.fillStyle = trace.marker?.color || '#000';
                            ctx.arc(x, y, trace.marker?.size / 2 || 5, 0, 2 * Math.PI);
                            ctx.fill();
                            
                            // Adicionar texto
                            if (trace.text && trace.text[0]) {
                                ctx.fillStyle = '#000';
                                ctx.font = '12px Arial';
                                ctx.fillText(trace.text[0], x + 10, y - 10);
                            }
                        }
                    }
                }
            }
        };
        """

    def gerar_dados(self):
        q_max = self.Q_nominal * 1.5
        self.Q_plot = np.linspace(0.1, q_max, 200)

        self.H_plot = self.H_0 - self.A * self.Q_plot ** 2
        self.H_plot[self.H_plot < 0] = 0

        self.C_plot = self.H_geometrico + self.perda_carga * self.Q_plot ** 2

        self.eta_plot = self.calcular_rendimento()
        self.P_plot = self.calcular_potencia()

        self.Q_op, self.H_op = self.encontrar_ponto_operacao()

    def calcular_rendimento(self):
        eta_max = 0.75
        k = 0.01
        return eta_max - k * (self.Q_plot - self.Q_nominal) ** 2

    def calcular_potencia(self, g=9.81):
        rho = 1000
        Q_m3s = self.Q_plot / 3600
        eta_seguro = np.where(self.eta_plot > 0, self.eta_plot, np.nan)
        P = (rho * g * Q_m3s * self.H_plot) / eta_seguro
        return P / 1000

    def encontrar_ponto_operacao(self):
        diferenca = np.abs(self.H_plot - self.C_plot)
        indice_otimo = np.argmin(diferenca)
        return self.Q_plot[indice_otimo], self.H_plot[indice_otimo]

    def plotar_ponto_operacao(self, fig, y_valor, ylabel):
        # Adicionar ponto de operação
        fig.add_trace(go.Scatter(
            x=[self.Q_op], 
            y=[y_valor],
            mode='markers+text',
            marker=dict(size=10, color='black'),
            name="Ponto de Operação",
            text=[f"Q = {self.Q_op:.2f}<br>Y = {y_valor:.2f}"],
            textposition="top right",
            hoverinfo='text'
        ))

    def plotar(self):
        fig = go.Figure()

        if self.tipo == "altura":
            # Curva da Bomba
            fig.add_trace(go.Scatter(
                x=self.Q_plot, 
                y=self.H_plot, 
                mode='lines',
                name="Curva da Bomba",
                line=dict(color='#1f77b4', width=2.5)
            ))
            
            # Curva do Sistema
            fig.add_trace(go.Scatter(
                x=self.Q_plot, 
                y=self.C_plot, 
                mode='lines',
                name="Curva do Sistema",
                line=dict(color='#ff7f0e', width=2.5)
            ))
            
            self.plotar_ponto_operacao(fig, self.H_op, f"Altura {self.potencia}")
            
            fig.update_layout(
                title="Curva da Bomba - Altura vs Vazão",
                xaxis_title=f"Vazão {self.vazao}",
                yaxis_title=f"Altura {self.altura}"
            )

        elif self.tipo == "potencia":
            y_val = np.interp(self.Q_op, self.Q_plot, self.P_plot)
            
            fig.add_trace(go.Scatter(
                x=self.Q_plot, 
                y=self.P_plot, 
                mode='lines',
                name="Potência",
                line=dict(color='#2ca02c', width=2.5)
            ))
            
            self.plotar_ponto_operacao(fig, y_val, f"Potência {self.potencia}")
            
            fig.update_layout(
                title="Potência vs Vazão",
                xaxis_title=f"Vazão {self.vazao}",
                yaxis_title=f"Potência {self.potencia}"
            )

        elif self.tipo == "rendimento":
            y_val = np.interp(self.Q_op, self.Q_plot, self.eta_plot * 100)
            
            fig.add_trace(go.Scatter(
                x=self.Q_plot, 
                y=self.eta_plot * 100, 
                mode='lines',
                name="Rendimento",
                line=dict(color='#d62728', width=2.5)
            ))
            
            self.plotar_ponto_operacao(fig, y_val, "Rendimento (%)")
            
            fig.update_layout(
                title="Rendimento vs Vazão",
                xaxis_title=f"Vazão {self.vazao}",
                yaxis_title="Rendimento (%)"
            )

        else:
            fig.add_annotation(
                x=0.5, 
                y=0.5, 
                text="Tipo de gráfico inválido",
                showarrow=False,
                font=dict(size=16)
            )

        # Configurações comuns
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            hovermode='closest',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgray',
            zeroline=False
        )
        
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgray',
            zeroline=False
        )

        # Limpar arquivo temporário anterior se existir
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.unlink(self.temp_file)
            except:
                pass  # Ignorar erros ao excluir arquivos temporários
        
        # Criar novo arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            # Gerar HTML com Plotly.js incorporado
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Plotly Graph</title>
                <script>
                {self.plotly_js}
                </script>
            </head>
            <body>
                <div id="plotly-div" style="width:100%; height:100%;"></div>
                <script>
                    var figure = {fig.to_json()};
                    Plotly.newPlot('plotly-div', figure.data, figure.layout);
                </script>
            </body>
            </html>
            """
            f.write(html_content)
            self.temp_file = f.name
        
    # Carregar o arquivo
        self.web_view.load(QUrl.fromLocalFile(self.temp_file))

    def actualizar_dados(self, altura, perda):
        """ Atualiza os dados da bomba e recalcula os gráficos. """
        self.H_geometrico = altura
        self.perda_carga = perda
        self.gerar_dados()
        self.plotar()
        
    def __del__(self):
        """Limpar arquivo temporário quando o objeto for destruído"""
        if hasattr(self, 'temp_file') and self.temp_file and os.path.exists(self.temp_file):
            try:
                os.unlink(self.temp_file)
            except:
                pass  # Ignorar erros ao excluir arquivos temporários