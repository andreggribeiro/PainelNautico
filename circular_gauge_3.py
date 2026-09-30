import sys
import math

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget, QLabel


# ============================================================
# 1. INSTRUMENTO CIRCULAR - RPM (0 a 8 x1000)
# ============================================================

class GaugeRPM(QWidget):

    def __init__(self, titulo="RPM", valor=2500, tamanho=360):
        super().__init__()
        self.titulo = titulo
        self.valor = valor
        self.minimo = 0
        self.maximo = 8000
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 8

        # Sombra Externa
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 5), int(cy - raio + 7), int(raio * 2), int(raio * 2))

        # Aro Metálico
        gradiente_aro = QRadialGradient(cx - 20, cy - 25, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        # Mostrador Interno
        raio_interno = raio - 12
        gradiente_mostrador = QRadialGradient(cx - 35, cy - 40, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

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

        # Verde (1000 a 3000)
        pen_faixa.setColor(QColor("#2e7d32"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(1000), int(-(270 * (2000 / 8000.0)) * 16))

        # Amarela (3000 a 5000)
        pen_faixa.setColor(QColor("#f57f17"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(3000), int(-(270 * (2000 / 8000.0)) * 16))

        # Vermelha (5000 a 8000)
        pen_faixa.setColor(QColor("#c62828"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, rpm_para_angulo_qt(5000), int(-(270 * (3000 / 8000.0)) * 16))

        # Escala e Números (0 a 8)
        fonte_numeros = QFont("Arial", 12, QFont.Bold)
        for i in range(9):
            angulo_graus = 135 + (270 / 8.0) * i
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 8)
            y1 = cy + math.sin(angulo) * (raio_interno - 8)
            x2 = cx + math.cos(angulo) * (raio_interno - 20)
            y2 = cy + math.sin(angulo) * (raio_interno - 20)

            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 32)
            ty = cy + math.sin(angulo) * (raio_interno - 32)

            painter.setFont(fonte_numeros)
            painter.setPen(QPen(Qt.black))
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

        painter.setPen(QPen(QColor("#E00000"), 4))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        # Eixo Central
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 8), int(cy - 8), 16, 16)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)

        # Textos e Leitura Digital
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy + 45), 100, 30, Qt.AlignCenter, str(int(self.valor)))

        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 60), int(cy - 50), 120, 25, Qt.AlignCenter, self.titulo)

        painter.end()


# ============================================================
# 2. INSTRUMENTO CIRCULAR PADRÃO (USADO PARA BATERIA)
# ============================================================

class Gauge(QWidget):

    def __init__(self, titulo, valor, unidade, minimo, maximo, tamanho=230):
        super().__init__()
        self.titulo = titulo
        self.valor = valor
        self.unidade = unidade
        self.minimo = minimo
        self.maximo = maximo
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        # Sombra
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(int(cx - raio + 4), int(cy - raio + 5), int(raio * 2), int(raio * 2))

        # Aro
        gradiente_aro = QRadialGradient(cx - 15, cy - 20, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(int(cx - raio), int(cy - raio), int(raio * 2), int(raio * 2))

        # Mostrador
        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        # Escala
        painter.setPen(QPen(Qt.black, 2))
        for i in range(11):
            angulo_graus = 135 + (270 / 10) * i
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Ponteiro
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

        # Eixo
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        # Textos
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        texto_valor = f"{self.valor:.1f}" if isinstance(self.valor, float) else str(int(self.valor))
        painter.drawText(int(cx - 40), int(cy + 28), 80, 25, Qt.AlignCenter, texto_valor)

        painter.setFont(QFont("Arial", 9))
        painter.drawText(int(cx - 35), int(cy + 52), 70, 20, Qt.AlignCenter, self.unidade)

        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 42), 100, 25, Qt.AlignCenter, self.titulo)

        painter.end()


# ============================================================
# 3. NOVO: PRESSÃO DA ÁGUA (0 a 60 PSI)
# ============================================================

class WaterPressureGauge(QWidget):

    def __init__(self, valor=25, tamanho=230):
        super().__init__()
        self.valor = valor
        self.minimo = 0
        self.maximo = 60
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        # Sombra e Aro Metálico
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

        # Mostrador Interno
        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        # Faixas Coloridas
        raio_faixa = raio_interno - 10
        rect_faixa = QRectF(cx - raio_faixa, cy - raio_faixa, raio_faixa * 2, raio_faixa * 2)

        def psi_para_angulo_qt(psi):
            prop = psi / 60.0
            angulo_graus = 225 - (270 * prop)
            return int(angulo_graus * 16)

        pen_faixa = QPen()
        pen_faixa.setWidth(6)

        # Vermelho Alerta Baixa Pressão (0 a 10 PSI)
        pen_faixa.setColor(QColor("#c62828"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(0), int(-(270 * (10 / 60.0)) * 16))

        # Verde Operação Normal (10 a 40 PSI)
        pen_faixa.setColor(QColor("#2e7d32"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(10), int(-(270 * (30 / 60.0)) * 16))

        # Amarelo Alta Pressão (40 a 60 PSI)
        pen_faixa.setColor(QColor("#f57f17"))
        painter.setPen(pen_faixa)
        painter.drawArc(rect_faixa, psi_para_angulo_qt(40), int(-(270 * (20 / 60.0)) * 16))

        # Escala (0, 10, 20, 30, 40, 50, 60)
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        for i in range(7):
            val = i * 10
            angulo_graus = 135 + (270 / 6.0) * i
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 26)
            ty = cy + math.sin(angulo) * (raio_interno - 26)

            painter.setPen(QPen(Qt.black))
            painter.drawText(int(tx - 15), int(ty - 10), 30, 20, Qt.AlignCenter, str(val))

        # Ponteiro
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

        # Eixo
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)
        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        # Textos
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 40), int(cy + 28), 80, 25, Qt.AlignCenter, f"{self.valor:.1f}")

        painter.setFont(QFont("Arial", 9))
        painter.drawText(int(cx - 35), int(cy + 52), 70, 20, Qt.AlignCenter, "PSI")

        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(int(cx - 60), int(cy - 42), 120, 25, Qt.AlignCenter, "PRESSÃO ÁGUA")

        painter.end()


# ============================================================
# 4. NOVO: BÚSSOLA NÁUTICA (HEADING / RUMO)
# ============================================================

class CompassGauge(QWidget):

    def __init__(self, rumo=45, tamanho=230):
        super().__init__()
        self.rumo = rumo  # Rumo em graus (0 - 359)
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

        # Sombra e Aro Metálico
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

        # Mostrador Interno
        raio_interno = raio - 10
        gradiente_mostrador = QRadialGradient(cx - 25, cy - 30, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        # MARCAÇÕES DA BÚSSOLA (Giram conforme o rumo)
        pontos_cardeais = {0: "N", 90: "E", 180: "S", 270: "W"}
        fonte_cardeal = QFont("Arial", 11, QFont.Bold)

        for ang_base in range(0, 360, 30):
            # O rumo atual rotaciona a rosa dos ventos
            ang_visivel = ang_base - self.rumo - 90
            angulo = math.radians(ang_visivel)

            x1 = cx + math.cos(angulo) * (raio_interno - 6)
            y1 = cy + math.sin(angulo) * (raio_interno - 6)
            x2 = cx + math.cos(angulo) * (raio_interno - 16)
            y2 = cy + math.sin(angulo) * (raio_interno - 16)

            painter.setPen(QPen(Qt.black, 2 if ang_base % 90 == 0 else 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            tx = cx + math.cos(angulo) * (raio_interno - 28)
            ty = cy + math.sin(angulo) * (raio_interno - 28)

            if ang_base in pontos_cardeais:
                label = pontos_cardeais[ang_base]
                painter.setFont(fonte_cardeal)
                if label == "N":
                    painter.setPen(QPen(QColor("#DD0000")))  # Norte em Destaque Vermelho
                else:
                    painter.setPen(QPen(Qt.black))
                painter.drawText(int(tx - 12), int(ty - 12), 24, 24, Qt.AlignCenter, label)

        # PONTEIRO DE PROA (LUBBER LINE - Fixo apontando para o topo)
        painter.setPen(QPen(QColor("#E00000"), 3))
        painter.drawLine(QPointF(cx, cy - raio_interno + 2), QPointF(cx, cy - raio_interno + 22))

        # TRIÂNGULO DA PROA
        painter.setBrush(QBrush(QColor("#E00000")))
        painter.setPen(Qt.NoPen)
        p1 = QPointF(cx, cy - raio_interno + 22)
        p2 = QPointF(cx - 6, cy - raio_interno + 32)
        p3 = QPointF(cx + 6, cy - raio_interno + 32)
        painter.drawPolygon([p1, p2, p3])

        # CENTRO
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 7), int(cy - 7), 14, 14)

        # Leitura Digital do Rumo
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(int(cx - 40), int(cy + 25), 80, 25, Qt.AlignCenter, f"{int(self.rumo):03d}°")

        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 42), 100, 25, Qt.AlignCenter, "BÚSSOLA")

        painter.end()


# ============================================================
# 5. TRIM (-15° a +15°)
# ============================================================

class TrimGauge(QWidget):

    def __init__(self, valor=0, tamanho=230):
        super().__init__()
        self.valor = valor
        self.minimo = -15
        self.maximo = 15
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 6

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
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        painter.setPen(QPen(Qt.black, 2))
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

        painter.setPen(QPen(Qt.black))
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
        self.setFixedSize(130, 250)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()

        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(2, 2, w - 4, 246, 10, 10)

        fonte = QFont("Arial", 11, QFont.Bold)
        painter.setFont(fonte)
        painter.setPen(QPen(Qt.white))
        painter.drawText(0, 10, w, 20, Qt.AlignCenter, "COMBUSTÍVEL")

        largura, altura, espacamento = 38, 15, 5
        x = (w - largura) / 2
        y_inicial = 38
        preenchidos = 7

        for i in range(10):
            y = y_inicial + (9 - i) * (altura + espacamento)

            if i < preenchidos:
                painter.setBrush(QBrush(Qt.green))
            else:
                painter.setBrush(Qt.NoBrush)

            painter.setPen(QPen(Qt.black, 1))
            painter.drawRoundedRect(int(x), int(y), largura, altura, 6, 6)

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(3, int(y_inicial + 9 * (altura + espacamento)), 25, 18, Qt.AlignCenter, "E")
        painter.drawText(3, int(y_inicial + 4.5 * (altura + espacamento)), 25, 18, Qt.AlignCenter, "½")
        painter.drawText(3, int(y_inicial), 25, 18, Qt.AlignCenter, "F")

        painter.end()


# ============================================================
# PAINEL PRINCIPAL (1024 x 600)
# ============================================================

class Painel(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Painel Náutico")
        self.setFixedSize(1024, 600)
        self.setStyleSheet("QWidget { background-color: #0b1117; }")

        # 1. RPM (Grande)
        self.rpm = GaugeRPM("RPM", 2500, tamanho=360)
        self.rpm.setParent(self)
        self.rpm.move(30, 50)

        # 2. TRIM (Tamanho 230)
        self.trim = TrimGauge(valor=0, tamanho=230)
        self.trim.setParent(self)
        self.trim.move(380, 10)

        # 3. BATERIA (Tamanho 230)
        self.voltagem = Gauge("BATERIA", 12.6, "V", 10, 16, tamanho=230)
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

        # 7. TÍTULO DO PAINEL
        #titulo = QLabel("Embarcação: BUSCAPÉ I", self)
        #titulo.setGeometry(0, 10, 1024, 40)
        #fonte = QFont("Arial", 20, QFont.Bold)
        #titulo.setFont(fonte)
        #titulo.setStyleSheet("color: white;")
        #titulo.setAlignment(Qt.AlignCenter)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    painel = Painel()
    painel.show()
    sys.exit(app.exec())