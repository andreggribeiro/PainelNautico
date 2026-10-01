import sys
import math

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QRadialGradient, QConicalGradient
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton


# ============================================================
# 1. INSTRUMENTO CIRCULAR - RPM
# ============================================================

class GaugeRPM(QWidget):

    def __init__(self, titulo="RPM", valor=2500, tamanho=360):
        super().__init__()
        self.titulo = titulo
        self.valor = valor
        self.minimo = 0
        self.maximo = 8000
        self.modo_noturno = False
        self.setFixedSize(tamanho, tamanho)

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 8

        # Cores com base no modo
        if self.modo_noturno:
            cor_mostrador_inicio = QColor("#222222")
            cor_mostrador_fim = QColor("#111111")
            cor_texto = QColor("#FF4444")
            cor_ponteiro = QColor("#FF0000")
            cor_escala = QColor("#FF4444")
        else:
            cor_mostrador_inicio = QColor("#FFFFFF")
            cor_mostrador_fim = QColor("#B8B8B8")
            cor_texto = QColor("#000000")
            cor_ponteiro = QColor("#E00000")
            cor_escala = QColor("#000000")

        # Sombra e Aro
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 5), int(cy - raio + 7), int(raio * 2), int(raio * 2))

        gradiente_aro = QRadialGradient(cx - 20, cy - 25, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        # Mostrador
        raio_interno = raio - 12
        gradiente_mostrador = QRadialGradient(cx - 35, cy - 40, raio_interno)
        gradiente_mostrador.setColorAt(0.0, cor_mostrador_inicio)
        gradiente_mostrador.setColorAt(1.0, cor_mostrador_fim)

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        # Faixas Coloridas
        raio_faixa = raio_interno - 12
        rect_faixa = QRectF(cx - raio_faixa, cy - raio_faixa, raio_faixa * 2, raio_faixa * 2)

        def rpm_para_angulo_qt(rpm):
            prop = rpm / 8000.0
            angulo_graus = 225 - (270 * prop)
            return int(angulo_graus * 16)

        pen_faixa = QPen()
        pen_faixa.setWidth(8)

        pen_faixa.setColor(QColor("#2e7d32"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(1000), int(-(270 * (2000 / 8000.0)) * 16))

        pen_faixa.setColor(QColor("#f57f17"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(3000), int(-(270 * (2000 / 8000.0)) * 16))

        pen_faixa.setColor(QColor("#c62828"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(5000), int(-(270 * (3000 / 8000.0)) * 16))

        # Escala e Números
        fonte_numeros = QFont("Arial", 12, QFont.Bold)
        for i in range(9):
            angulo_graus = 135 + (270 / 8.0) * i
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 8)
            y1 = cy + math.sin(angulo) * (raio_interno - 8)
            x2 = cx + math.cos(angulo) * (raio_interno - 20)
            y2 = cy + math.sin(angulo) * (raio_interno - 20)

            painter.setPen(QPen(cor_escala, 2))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 32)
            ty = cy + math.sin(angulo) * (raio_interno - 32)

            painter.setFont(fonte_numeros)
            painter.setPen(QPen(cor_texto))
            painter.drawText(int(tx - 15), int(ty - 12), 30, 24, Qt.AlignCenter, str(i))

        # Ponteiro
        proporcao = max(0.0, min(1.0, (self.valor - self.minimo) / (self.maximo - self.minimo)))
        angulo_graus = 135 + 270 * proporcao
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 42

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 6))
        painter.drawLine(QPointF(cx + 2, cy + 3), QPointF(px + 2, py + 3))

        painter.setPen(QPen(cor_ponteiro, 4))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        # Eixo
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 8), int(cy - 8), 16, 16)
        painter.setBrush(QBrush(cor_ponteiro))
        painter.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)

        # Leitura Digital
        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy + 45), 100, 30, Qt.AlignCenter, str(int(self.valor)))

        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 60), int(cy - 50), 120, 25, Qt.AlignCenter, self.titulo)

        painter.end()


# ============================================================
# 2. INSTRUMENTO CIRCULAR PADRÃO (BATERIA)
# ============================================================

import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QPointF

class Gauge(QWidget):

    def __init__(self, titulo, valor, unidade, minimo, maximo, tamanho=230):
        super().__init__()
        self.titulo = titulo
        self.unidade = unidade
        self.minimo = float(minimo)
        self.maximo = float(maximo)
        
        # Força a conversão do valor para float no início
        try:
            self._valor = float(valor)
        except (ValueError, TypeError):
            self._valor = float(minimo)

        self.modo_noturno = False
        self.setFixedSize(tamanho, tamanho)

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        try:
            self._valor = float(novo_valor)
        except (ValueError, TypeError):
            self._valor = self.minimo
        self.update()

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        # Cores padrão do projeto
        cor_inicio = QColor("#222222") if self.modo_noturno else QColor("#FFFFFF")
        cor_fim = QColor("#111111") if self.modo_noturno else QColor("#B8B8B8")
        cor_texto = QColor("#FF4444") if self.modo_noturno else QColor("#000000")

        # ---------------------------------------------------------
        # 1. SOMBRA PROJETADA DO RELÓGIO
        # ---------------------------------------------------------
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 4), int(cy - raio + 5), int(raio * 2), int(raio * 2))

        # ---------------------------------------------------------
        # 2. ARO METÁLICO 3D
        # ---------------------------------------------------------
        gradiente_aro = QRadialGradient(cx - 15, cy - 20, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        # ---------------------------------------------------------
        # 3. MOSTRADOR INTERNO
        # ---------------------------------------------------------
        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, cor_inicio)
        gradiente_mostrador.setColorAt(1.0, cor_fim)

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        # ---------------------------------------------------------
        # 4. ESCALA DA VOLTAGEM (10V A 16V)
        # ---------------------------------------------------------
        painter.setPen(QPen(cor_texto, 2))
        divisoes = 6  # 10, 11, 12, 13, 14, 15, 16

        for i in range(divisoes + 1):
            val_escala = self.minimo + (i * (self.maximo - self.minimo) / divisoes)
            
            # Mapeamento: 0 (10V) -> 135°, 6 (16V) -> 405°
            ang_graus = 135.0 + (270.0 / divisoes) * i
            rad = math.radians(ang_graus)

            # Traços
            x1 = cx + math.cos(rad) * (raio_interno - 6)
            y1 = cy + math.sin(rad) * (raio_interno - 6)
            x2 = cx + math.cos(rad) * (raio_interno - 16)
            y2 = cy + math.sin(rad) * (raio_interno - 16)

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            # Números impressos na escala
            tx = cx + math.cos(rad) * (raio_interno - 28)
            ty = cy + math.sin(rad) * (raio_interno - 28)

            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(int(tx - 15), int(ty - 10), 30, 20, Qt.AlignCenter, str(int(val_escala)))

        # ---------------------------------------------------------
        # 5. PONTEIRO (AJUSTADO E CALIBRADO)
        # ---------------------------------------------------------
        intervalo = self.maximo - self.minimo
        if intervalo <= 0:
            intervalo = 1.0

        # Força o cálculo em float do valor atual
        val_atual = float(self._valor)
        val_limpo = max(self.minimo, min(self.maximo, val_atual))
        proporcao = (val_limpo - self.minimo) / intervalo

        # Mapeamento do ângulo: Para 14.2V a proporção é 0.70 (324 graus - Quadrante Superior Direito)
        ang_ponteiro_graus = 135.0 + (270.0 * proporcao)
        rad_ponteiro = math.radians(ang_ponteiro_graus)
        comprimento = raio_interno - 30

        px = cx + math.cos(rad_ponteiro) * comprimento
        py = cy + math.sin(rad_ponteiro) * comprimento

        # Sombra do Ponteiro
        painter.setPen(QPen(QColor(0, 0, 0, 100), 5))
        painter.drawLine(QPointF(cx + 2.0, cy + 3.0), QPointF(px + 2.0, py + 3.0))

        # Corpo do Ponteiro
        cor_ponteiro = QColor("#FF4444") if self.modo_noturno else QColor("#E00000")
        painter.setPen(QPen(cor_ponteiro, 4))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        # Eixo Central
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        # ---------------------------------------------------------
        # 6. LEITURA DIGITAL E TÍTULO
        # ---------------------------------------------------------
        painter.setPen(QPen(cor_texto))
        
        # Título Superior ("BATERIA")
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 40), 100, 25, Qt.AlignCenter, self.titulo)

        # Leitura Digital Inferior
        painter.setFont(QFont("Arial", 13, QFont.Bold))
        texto_valor = f"{self._valor:.1f} {self.unidade}"
        painter.drawText(int(cx - 50), int(cy + 28), 100, 25, Qt.AlignCenter, texto_valor)

        painter.end()

# ============================================================
# 3. PRESSÃO DA ÁGUA
# ============================================================

class WaterPressureGauge(QWidget):

    def __init__(self, valor=25, tamanho=230):
        super().__init__()
        self.valor = valor
        self.minimo = 0
        self.maximo = 60
        self.modo_noturno = False
        self.setFixedSize(tamanho, tamanho)

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        cor_inicio = QColor("#222222") if self.modo_noturno else QColor("#FFFFFF")
        cor_fim = QColor("#111111") if self.modo_noturno else QColor("#B8B8B8")
        cor_texto = QColor("#FF4444") if self.modo_noturno else QColor("#000000")

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 4), int(cy - raio + 5), int(raio * 2), int(raio * 2))

        gradiente_aro = QRadialGradient(cx - 15, cy - 20, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, cor_inicio)
        gradiente_mostrador.setColorAt(1.0, cor_fim)

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        raio_faixa = raio_interno - 10
        rect_faixa = QRectF(cx - raio_faixa, cy - raio_faixa, raio_faixa * 2, raio_faixa * 2)

        def psi_para_angulo_qt(psi):
            prop = psi / 60.0
            angulo_graus = 225 - (270 * prop)
            return int(angulo_graus * 16)

        pen_faixa = QPen()
        pen_faixa.setWidth(6)

        pen_faixa.setColor(QColor("#c62828"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(0), int(-(270 * (10 / 60.0)) * 16))

        pen_faixa.setColor(QColor("#2e7d32"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(10), int(-(270 * (30 / 60.0)) * 16))

        pen_faixa.setColor(QColor("#f57f17"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(40), int(-(270 * (20 / 60.0)) * 16))

        painter.setFont(QFont("Arial", 8, QFont.Bold))
        for i in range(7):
            val = i * 10
            angulo_graus = 135 + (270 / 6.0) * i
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.setPen(QPen(cor_texto, 2))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 26)
            ty = cy + math.sin(angulo) * (raio_interno - 26)

            painter.setPen(QPen(cor_texto))
            painter.drawText(int(tx - 15), int(ty - 10), 30, 20, Qt.AlignCenter, str(val))

        proporcao = max(0.0, min(1.0, (self.valor - self.minimo) / (self.maximo - self.minimo)))
        angulo_graus = 135 + 270 * proporcao
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 30

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 5))
        painter.drawLine(QPointF(cx + 2, cy + 3), QPointF(px + 2, py + 3))

        painter.setPen(QPen(QColor("#E00000"), 4))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 40), int(cy + 28), 80, 25, Qt.AlignCenter, f"{self.valor:.1f}")

        painter.setFont(QFont("Arial", 9))
        painter.drawText(int(cx - 35), int(cy + 52), 70, 20, Qt.AlignCenter, "PSI")

        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(int(cx - 60), int(cy - 42), 120, 25, Qt.AlignCenter, "PRESSÃO ÁGUA")

        painter.end()


# ============================================================
# 4. BÚSSOLA NÁUTICA
# ============================================================

class CompassGauge(QWidget):

    def __init__(self, rumo=45, tamanho=230):
        super().__init__()
        self.rumo = rumo
        self.modo_noturno = False
        self.setFixedSize(tamanho, tamanho)

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        cor_inicio = QColor("#222222") if self.modo_noturno else QColor("#FFFFFF")
        cor_fim = QColor("#111111") if self.modo_noturno else QColor("#B8B8B8")
        cor_texto = QColor("#FF4444") if self.modo_noturno else QColor("#000000")

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 4), int(cy - raio + 5), int(raio * 2), int(raio * 2))

        gradiente_aro = QRadialGradient(cx - 15, cy - 20, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, cor_inicio)
        gradiente_mostrador.setColorAt(1.0, cor_fim)

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        pontos_cardeais = {0: "N", 90: "E", 180: "S", 270: "W"}
        fonte_cardeal = QFont("Arial", 11, QFont.Bold)

        for ang_base in range(0, 360, 30):
            ang_visivel = ang_base - self.rumo - 90
            angulo = math.radians(ang_visivel)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.setPen(QPen(cor_texto, 2 if ang_base % 90 == 0 else 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 28)
            ty = cy + math.sin(angulo) * (raio_interno - 28)

            if ang_base in pontos_cardeais:
                label = pontos_cardeais[ang_base]
                painter.setFont(fonte_cardeal)
                if label == "N":
                    painter.setPen(QPen(QColor("#DD0000")))
                else:
                    painter.setPen(QPen(cor_texto))
                painter.drawText(int(tx - 12), int(ty - 12), 24, 24, Qt.AlignCenter, label)

        painter.setPen(QPen(QColor("#E00000"), 3))
        painter.drawLine(QPointF(cx, cy - raio_interno + 2), QPointF(cx, cy - raio_interno + 22))

        painter.setBrush(QBrush(QColor("#E00000")))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon([QPointF(cx, cy - raio_interno + 22), QPointF(cx - 6, cy - raio_interno + 32), QPointF(cx + 6, cy - raio_interno + 32)])

        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)

        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 40), int(cy + 25), 80, 25, Qt.AlignCenter, f"{int(self.rumo):03d}°")

        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 42), 100, 25, Qt.AlignCenter, "BÚSSOLA")

        painter.end()


# ============================================================
# 5. TRIM
# ============================================================

class TrimGauge(QWidget):

    def __init__(self, valor=0, tamanho=230):
        super().__init__()
        self.valor = valor
        self.minimo = -15
        self.maximo = 15
        self.modo_noturno = False
        self.setFixedSize(tamanho, tamanho)

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        cor_inicio = QColor("#222222") if self.modo_noturno else QColor("#FFFFFF")
        cor_fim = QColor("#111111") if self.modo_noturno else QColor("#B8B8B8")
        cor_texto = QColor("#FF4444") if self.modo_noturno else QColor("#000000")

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 4), int(cy - raio + 5), int(raio * 2), int(raio * 2))

        gradiente_aro = QRadialGradient(cx - 15, cy - 20, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, cor_inicio)
        gradiente_mostrador.setColorAt(1.0, cor_fim)

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        painter.setPen(QPen(cor_texto, 2))
        valores_escala = [-15, -10, -5, 0, 5, 10, 15]

        for val in valores_escala:
            angulo_graus = -val * 2.0
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            if val in [-15, 0, 15]:
                tx = cx + math.cos(angulo) * (raio_interno - 28)
                ty = cy + math.sin(angulo) * (raio_interno - 28)
                texto = f"+{val}°" if val > 0 else f"{val}°"
                painter.setFont(QFont("Arial", 9, QFont.Bold))
                painter.drawText(int(tx - 15), int(ty - 10), 30, 20, Qt.AlignCenter, texto)

        angulo_graus = -self.valor * 2.0
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 30

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 5))
        painter.drawLine(QPointF(cx + 2, cy + 3), QPointF(px + 2, py + 3))

        painter.setPen(QPen(QColor("#E00000"), 4))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        texto_valor = f"{self.valor:+.1f}°" if isinstance(self.valor, float) else f"{self.valor:+d}°"
        painter.drawText(int(cx - 40), int(cy + 28), 80, 25, Qt.AlignCenter, texto_valor)

        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 42), 100, 25, Qt.AlignCenter, "TRIM")

        painter.end()


# ============================================================
# 6. INDICADOR DE COMBUSTÍVEL
# ============================================================

class FuelIndicator(QWidget):

    def __init__(self):
        super().__init__()
        self.modo_noturno = False
        self.setFixedSize(130, 250)

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        cor_borda = QColor("#FF4444") if getattr(self, 'modo_noturno', False) else QColor("#FFFFFF")

        # 1. Moldura externa
        painter.setPen(QPen(cor_borda, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(2, 2, w - 4, 246, 10, 10)

        # 2. Título
        fonte = QFont("Arial", 11, QFont.Bold)
        painter.setFont(fonte)
        painter.setPen(QPen(cor_borda))
        painter.drawText(0, 10, w, 20, Qt.AlignCenter, "COMBUSTÍVEL")

        # 3. Configuração dos Segmentos
        largura, altura, espacamento = 38, 15, 5
        x = (w - largura) / 2
        y_inicial = 38
        
        # Consideramos o percentual atual do indicador (ex: self.percentual ou um valor padrão)
        percentual_atual = getattr(self, 'percentual', 20)  # Caso não tenha a propriedade, usa 70% como teste
        segmentos_ativos = int(round((percentual_atual / 100.0) * 10))

        # =========================================================
        # REGRA DE CORES CONFORME A AUTONOMIA DO TANQUE
        # =========================================================
        if percentual_atual <= 20:
            cor_combustivel = QColor("#FF2222")  # Vermelho (Reserva <= 20%)
        elif percentual_atual <= 50:
            cor_combustivel = QColor("#FFCC00")  # Amarelo (Atenção <= 50%)
        else:
            cor_combustivel = QColor("#00E676")  # Verde (Normal > 50%)

        # 4. Desenhar os 10 segmentos
        for i in range(10):
            y = y_inicial + (9 - i) * (altura + espacamento)

            if i < segmentos_ativos:
                # Segmentos ACESOS (Verde, Amarelo ou Vermelho)
                painter.setBrush(QBrush(cor_combustivel))
                painter.setPen(QPen(Qt.black, 1))
            else:
                # Segmentos DESABILITADOS/APAGADOS (Ajustados para ficarem mais visíveis)
                if getattr(self, 'modo_noturno', False):
                    # Modo Noturno: Cinza escuro sutil
                    painter.setBrush(QBrush(QColor("#262626")))
                    painter.setPen(QPen(QColor("#404040"), 1))
                else:
                    # Modo Dia: Tom chumbo mais claro para destacar bem no fundo escuro
                    painter.setBrush(QBrush(QColor("#2e3d49")))  # <-- Tom mais claro que o fundo
                    painter.setPen(QPen(QColor("#526575"), 1))   # <-- Borda visível do bloco vago

            painter.drawRoundedRect(int(x), int(y), largura, altura, 6, 6)

        # 5. Marcadores (E, ½, F)
        painter.setPen(QPen(cor_borda))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(3, int(y_inicial + 9 * (altura + espacamento)), 25, 18, Qt.AlignCenter, "E")
        painter.drawText(3, int(y_inicial + 4.5 * (altura + espacamento)), 25, 18, Qt.AlignCenter, "½")
        painter.drawText(3, int(y_inicial), 25, 18, Qt.AlignCenter, "F")

        painter.end()

class DepthIndicator(QWidget):

    def __init__(self, valor=5.4, largura=220, altura=110):
        super().__init__()
        self._profundidade = valor
        self.modo_noturno = False
        self.setFixedSize(largura, altura)

    @property
    def profundidade(self):
        return self._profundidade

    @profundidade.setter
    def profundidade(self, valor):
        """Atualiza o valor e repinta o widget."""
        self._profundidade = max(0.0, float(valor))
        self.update()

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Definição de cores (Modo Dia vs Modo Noturno)
        if self.modo_noturno:
            cor_linha = QColor("#FF4444")
            cor_texto = QColor("#FF4444")
            cor_alerta = QColor("#FF0000")
        else:
            cor_linha = Qt.white
            cor_texto = Qt.white
            cor_alerta = QColor("#FF3333")  # Alerta vermelho em água rasa

        # 1. Contorno Retangular (Borda Branca)
        painter.setPen(QPen(cor_linha, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(1, 1, w - 2, h - 2)

        # 2. Título / Cabeçalho
        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(10, 8, w - 20, 20, Qt.AlignLeft | Qt.AlignVCenter, "PROFUNDIDADE")

        # 3. Alerta de Água Rasa (Ex: se profundidade < 2.0 metros)
        if self._profundidade <= 2.0:
            painter.setPen(QPen(cor_alerta))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(10, 8, w - 20, 20, Qt.AlignRight | Qt.AlignVCenter, "⚠️ RASA")

        # 4. Valor Numérico Grande (Destaque para leitura rápida)
        # Se for menor que 2m, destaca o valor em vermelho de alerta
        cor_numero = cor_alerta if (self._profundidade <= 2.0 and not self.modo_noturno) else cor_texto
        painter.setPen(QPen(cor_numero))
        painter.setFont(QFont("Arial", 36, QFont.Bold))
        
        texto_prof = f"{self._profundidade:.1f}"
        # Desenha o número centralizado ligeiramente deslocado para a esquerda para caber o "m"
        painter.drawText(10, 28, w - 50, 65, Qt.AlignCenter, texto_prof)

        # 5. Unidade de Medida ("m" de Metros)
        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(w - 45, 60, 35, 30, Qt.AlignLeft | Qt.AlignBottom, "m")

        painter.end()

class GPSIndicator(QWidget):

    def __init__(self, lat="-00.000000", lon="-00.000000", largura=220, altura=110):
        super().__init__()
        self._lat = lat
        self._lon = lon
        self.modo_noturno = False
        self.setFixedSize(largura, altura)

    def atualizar_coordenadas(self, lat, lon):
        """Atualiza a latitude e longitude e repinta o widget."""
        self._lat = str(lat)
        self._lon = str(lon)
        self.update()

    def set_modo_noturno(self, ativado):
        self.modo_noturno = ativado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Definição de cores (Modo Dia vs Modo Noturno)
        if self.modo_noturno:
            cor_linha = QColor("#FF4444")
            cor_texto = QColor("#FF4444")
            cor_rotulo = QColor("#FF8888")
        else:
            cor_linha = Qt.white
            cor_texto = Qt.white
            cor_rotulo = QColor("#94a3b8")  # Cinza claro para os rótulos LAT/LON

        # 1. Contorno Retangular (Mesmo padrão do indicador de profundidade)
        painter.setPen(QPen(cor_linha, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(1, 1, w - 2, h - 2)

        # 2. Título / Cabeçalho
        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(10, 8, w - 20, 20, Qt.AlignLeft | Qt.AlignVCenter, "POSIÇÃO GPS")

        # 3. Exibição da Latitude
        painter.setPen(QPen(cor_rotulo))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(12, 36, 40, 20, Qt.AlignLeft | Qt.AlignVCenter, "LAT:")

        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 13, QFont.Bold))
        painter.drawText(50, 36, w - 60, 20, Qt.AlignLeft | Qt.AlignVCenter, self._lat)

        # 4. Exibição da Longitude
        painter.setPen(QPen(cor_rotulo))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(12, 68, 40, 20, Qt.AlignLeft | Qt.AlignVCenter, "LON:")

        painter.setPen(QPen(cor_texto))
        painter.setFont(QFont("Arial", 13, QFont.Bold))
        painter.drawText(50, 68, w - 60, 20, Qt.AlignLeft | Qt.AlignVCenter, self._lon)

        painter.end()


# ============================================================
# PAINEL PRINCIPAL
# ============================================================

class Painel(QWidget):

    def __init__(self):
        super().__init__()
        #self.voltagem = Gauge("BATERIA", 14.2, "V", 10, 16, tamanho=230)

        # =====================================================
        # INDICADOR DE PROFUNDIDADE (Canto Inferior Esquerdo)
        # =====================================================
        self.profundidade = DepthIndicator(valor=5.4, largura=220, altura=110)
        self.profundidade.setParent(self)
        
        # Posição X=15, Y = 600 - 110 - 15 = 475px
        self.profundidade.move(15, 475)

        # ======================================================
        # INDICADOR GPS (canto Inferior Direito)
        # ======================================================

        self.gps = GPSIndicator(lat="-23.550520", lon="-46.633308", largura=220, altura=110)
        self.gps.setParent(self)
        
        # Cálculo de Posição:
        # X = 1024 (Largura da tela) - 220 (Largura do widget) - 15 (Margem) = 789px
        # Y = 600 (Altura da tela) - 110 (Altura do widget) - 15 (Margem) = 475px
        self.gps.move(789, 475)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.modo_noturno_ativo = False

        self.setWindowTitle("Painel Náutico")
        self.setFixedSize(1024, 600)
        self.setStyleSheet("QWidget { background-color: #0b1117; }")

        # Instrumentos

        # 1. RPM (Grande)
        self.rpm = GaugeRPM("RPM", 2500, tamanho=360)
        self.rpm.setParent(self)
        self.rpm.move(30, 50)

        # 2. TRIM (Tamanho 230)
        self.trim = TrimGauge(valor=0, tamanho=230)
        self.trim.setParent(self)
        self.trim.move(380, 10)

        # 3. BATERIA (Tamanho 230)
        self.voltagem = Gauge("BATERIA", 14.8, "V", 10, 16, tamanho=230)
        self.voltagem.setParent(self)
        self.voltagem.move(610, 10)

        # 4. PRESSÃO DA ÁGUA (Tamanho 230 - NOVO)
        self.pressao_agua = WaterPressureGauge(valor=28.5, tamanho=230)
        self.pressao_agua.setParent(self)
        self.pressao_agua.move(380, 240)

        # 5. BÚSSOLA (Tamanho 230 - NOVO)
        self.bussola = CompassGauge(rumo=45, tamanho=230)
        self.bussola.setParent(self)
        self.bussola.move(610, 240)

        # 6. COMBUSTÍVEL
        self.combustivel = FuelIndicator()
        self.combustivel.setParent(self)
        self.combustivel.move(860, 10)

        # Título do Painel
        #self.titulo = QLabel("Embarcação: BUSCAPÉ I", self)
        #self.titulo.setGeometry(0, 10, 800, 40)
        #fonte = QFont("Arial", 20, QFont.Bold)
        #self.titulo.setFont(fonte)
        #self.titulo.setStyleSheet("color: white;")
        #self.titulo.setAlignment(Qt.AlignCenter)

        # Botão Touch do Modo Noturno
        self.btn_noturno = QPushButton("MODO NOTURNO", self)
        self.btn_noturno.setGeometry(432, 530, 160, 40)
        self.btn_noturno.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: white;
                border: 2px solid #3b82f6;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:pressed {
                background-color: #3b82f6;
            }
        """)
        self.btn_noturno.clicked.connect(self.alternar_modo_noturno)

    def paintEvent(self, event):
        # 1. Mantém a renderização do fundo (preto/azul) definida no QSS
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 2. Configura a caneta: Linha Branca, Espessura de 2px
        # Se estiver em modo noturno, podemos mudar a linha para vermelho sutil (opcional)
        cor_linha = QColor("#FF4444") if getattr(self, 'modo_noturno_ativo', False) else Qt.white
        painter.setPen(QPen(cor_linha, 2))
        painter.setBrush(Qt.NoBrush)  # Transparente por dentro

        # 3. Dimensões do Retângulo (Ajuste a largura e altura como preferir)
        largura_rect = 220
        altura_rect = 110
        margem = 15  # Afastamento da borda da tela

        # 4. Cálculo da Posição (Canto Inferior Esquerdo)
        x = margem
        y = self.height() - altura_rect - margem  # 600 - 110 - 15 = Y: 475px

        # 5. Desenha o retângulo (use drawRoundedRect se quiser cantos arredondados)
        painter.drawRect(int(x), int(y), largura_rect, altura_rect)

        painter.end()    

      
    def alternar_modo_noturno(self):
        self.modo_noturno_ativo = not self.modo_noturno_ativo

        # 1. Altera a cor de fundo do painel e do título
        if self.modo_noturno_ativo:
            self.setStyleSheet("QWidget { background-color: #000000; }")
            #self.titulo.setStyleSheet("color: #FF4444;")
            self.btn_noturno.setText("MODO DIA")
            self.btn_noturno.setStyleSheet("""
                QPushButton {
                    background-color: #7f1d1d;
                    color: #fca5a5;
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)
        else:
            self.setStyleSheet("QWidget { background-color: #0b1117; }")
            #self.titulo.setStyleSheet("color: white;")
            self.btn_noturno.setText("MODO NOTURNO")
            self.btn_noturno.setStyleSheet("""
                QPushButton {
                    background-color: #1e293b;
                    color: white;
                    border: 2px solid #3b82f6;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)

        # 2. Notifica TODOS os instrumentos ativos no seu painel
        self.rpm.set_modo_noturno(self.modo_noturno_ativo)
        self.trim.set_modo_noturno(self.modo_noturno_ativo)
        self.voltagem.set_modo_noturno(self.modo_noturno_ativo)
        self.pressao_agua.set_modo_noturno(self.modo_noturno_ativo)
        self.bussola.set_modo_noturno(self.modo_noturno_ativo)
        self.combustivel.set_modo_noturno(self.modo_noturno_ativo)
        self.profundidade.set_modo_noturno(self.modo_noturno_ativo)  # <-- NOVO
        self.gps.set_modo_noturno(self.modo_noturno_ativo)
        
# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    painel = Painel()
    painel.show()
    sys.exit(app.exec())