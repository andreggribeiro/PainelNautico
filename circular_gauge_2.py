import sys
import math

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget, QLabel


# ============================================================
# INSTRUMENTO CIRCULAR - RPM (COM FAIXAS E ESCALA 0-8)
# ============================================================

class GaugeRPM(QWidget):

    def __init__(self, titulo="RPM", valor=2500, tamanho=430):
        super().__init__()

        self.titulo = titulo
        self.valor = valor
        self.minimo = 0
        self.maximo = 8000

        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 8

        # 1. SOMBRA EXTERNA
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawEllipse(
            int(cx - raio + 5),
            int(cy - raio + 7),
            int(raio * 2),
            int(raio * 2)
        )

        # 2. ARO EXTERNO
        gradiente_aro = QRadialGradient(cx - 20, cy - 25, raio)
        gradiente_aro.setColorAt(0.0, QColor("#707070"))
        gradiente_aro.setColorAt(0.55, QColor("#404040"))
        gradiente_aro.setColorAt(0.78, QColor("#909090"))
        gradiente_aro.setColorAt(0.90, QColor("#353535"))
        gradiente_aro.setColorAt(1.0, QColor("#111111"))

        painter.setBrush(QBrush(gradiente_aro))
        painter.setPen(QPen(QColor("#AAAAAA"), 2))
        painter.drawEllipse(
            int(cx - raio),
            int(cy - raio),
            int(raio * 2),
            int(raio * 2)
        )

        # 3. MOSTRADOR INTERNO
        raio_interno = raio - 12
        gradiente_mostrador = QRadialGradient(cx - 35, cy - 40, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(
            int(cx - raio_interno),
            int(cy - raio_interno),
            int(raio_interno * 2),
            int(raio_interno * 2)
        )

        # 4. FAIXAS COLORIDAS (VERDE, AMARELA, VERMELHA)
        raio_faixa = raio_interno - 12
        rect_faixa = QRectF(cx - raio_faixa, cy - raio_faixa, raio_faixa * 2, raio_faixa * 2)

        def rpm_para_angulo_qt(rpm):
            prop = rpm / 8000.0
            angulo_graus = 225 - (270 * prop)
            return int(angulo_graus * 16)

        pen_faixa = QPen()
        pen_faixa.setWidth(10)

        # Verde (1 a 3 -> 1000 a 3000 RPM)
        pen_faixa.setColor(QColor("#2e7d32"))
        painter.setPen(pen_faixa)
        start_angle = rpm_para_angulo_qt(1000)
        span_angle = int(-(270 * (2000 / 8000.0)) * 16)
        painter.drawArc(rect_faixa, start_angle, span_angle)

        # Amarela (3 a 5 -> 3000 a 5000 RPM)
        pen_faixa.setColor(QColor("#f57f17"))
        painter.setPen(pen_faixa)
        start_angle = rpm_para_angulo_qt(3000)
        span_angle = int(-(270 * (2000 / 8000.0)) * 16)
        painter.drawArc(rect_faixa, start_angle, span_angle)

        # Vermelha (5 a 8 -> 5000 a 8000 RPM)
        pen_faixa.setColor(QColor("#c62828"))
        painter.setPen(pen_faixa)
        start_angle = rpm_para_angulo_qt(5000)
        span_angle = int(-(270 * (3000 / 8000.0)) * 16)
        painter.drawArc(rect_faixa, start_angle, span_angle)

        # 5. ESCALA E NÚMEROS (0 A 8)
        fonte_numeros = QFont("Arial", 16, QFont.Bold)

        for i in range(9):
            angulo_graus = 135 + (270 / 8.0) * i
            angulo = math.radians(angulo_graus)

            raio_externo = raio_interno - 8
            raio_interno_tick = raio_interno - 22

            x1 = cx + math.cos(angulo) * raio_externo
            y1 = cy + math.sin(angulo) * raio_externo
            x2 = cx + math.cos(angulo) * raio_interno_tick
            y2 = cy + math.sin(angulo) * raio_interno_tick

            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            raio_texto = raio_interno - 38
            tx = cx + math.cos(angulo) * raio_texto
            ty = cy + math.sin(angulo) * raio_texto

            painter.setFont(fonte_numeros)
            painter.setPen(QPen(Qt.black))
            painter.drawText(int(tx - 20), int(ty - 15), 40, 30, Qt.AlignCenter, str(i))

        # Marcação x1000 RPM
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(int(cx - 50), int(cy - 110), 100, 20, Qt.AlignCenter, "x1000 RPM")

        # 6. PONTEIRO
        proporcao = (self.valor - self.minimo) / (self.maximo - self.minimo)
        proporcao = max(0.0, min(1.0, proporcao))

        angulo_graus = 135 + 270 * proporcao
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 50

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 8))
        painter.drawLine(QPointF(cx + 3, cy + 4), QPointF(px + 3, py + 4))

        painter.setPen(QPen(QColor("#E00000"), 5))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        # 7. EIXO DO PONTEIRO
        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 10), int(cy - 10), 20, 20)

        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 5), int(cy - 5), 10, 10)

        # 8. VALOR DIGITAL E TÍTULO
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        texto_valor = str(int(self.valor))
        painter.drawText(int(cx - 60), int(cy + 60), 120, 40, Qt.AlignCenter, texto_valor)

        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(int(cx - 70), int(cy - 65), 140, 30, Qt.AlignCenter, self.titulo)

        painter.end()


# ============================================================
# INSTRUMENTO CIRCULAR PADRÃO (BATERIA)
# ============================================================

class Gauge(QWidget):

    def __init__(self, titulo, valor, unidade, minimo, maximo, tamanho=300):
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

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 8

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

        raio_interno = raio - 12
        gradiente_mostrador = QRadialGradient(cx - 35, cy - 40, raio_interno)
        gradiente_mostrador.setColorAt(0.0, QColor("#FFFFFF"))
        gradiente_mostrador.setColorAt(0.65, QColor("#F2F2F2"))
        gradiente_mostrador.setColorAt(0.88, QColor("#D8D8D8"))
        gradiente_mostrador.setColorAt(1.0, QColor("#B8B8B8"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#707070"), 2))
        painter.drawEllipse(int(cx - raio_interno), int(cy - raio_interno), int(raio_interno * 2), int(raio_interno * 2))

        painter.setPen(QPen(Qt.black, 3))
        for i in range(11):
            angulo_graus = 135 + (270 / 10) * i
            angulo = math.radians(angulo_graus)

            raio_externo = raio_interno - 8
            raio_interno_tick = raio_interno - 22

            x1 = cx + math.cos(angulo) * raio_externo
            y1 = cy + math.sin(angulo) * raio_externo
            x2 = cx + math.cos(angulo) * raio_interno_tick
            y2 = cy + math.sin(angulo) * raio_interno_tick

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        proporcao = (self.valor - self.minimo) / (self.maximo - self.minimo)
        proporcao = max(0.0, min(1.0, proporcao))

        angulo_graus = 135 + 270 * proporcao
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 38

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 8))
        painter.drawLine(QPointF(cx + 3, cy + 4), QPointF(px + 3, py + 4))

        painter.setPen(QPen(QColor("#E00000"), 5))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 9), int(cy - 9), 18, 18)

        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)

        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 22, QFont.Bold))
        texto_valor = f"{self.valor:.1f}" if isinstance(self.valor, float) else str(int(self.valor))
        painter.drawText(int(cx - 60), int(cy + 40), 120, 40, Qt.AlignCenter, texto_valor)

        painter.setFont(QFont("Arial", 11))
        painter.drawText(int(cx - 50), int(cy + 75), 100, 25, Qt.AlignCenter, self.unidade)

        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(int(cx - 70), int(cy - 65), 140, 30, Qt.AlignCenter, self.titulo)

        painter.end()


# ============================================================
# TRIM (VISUAL PADRONIZADO IGUAL AOS DEMAIS GAUGES)
# ============================================================

class TrimGauge(QWidget):

    def __init__(self, valor=0, tamanho=300):
        super().__init__()
        self.valor = valor
        self.minimo = -15
        self.maximo = 15
        self.setFixedSize(tamanho, tamanho)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        raio = min(self.width(), self.height()) / 2.0 - 8

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

        raio_interno = raio - 12
        gradiente_mostrador = QRadialGradient(cx - 35, cy - 40, raio_interno)
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

            raio_externo = raio_interno - 8
            raio_interno_tick = raio_interno - 22

            x1 = cx + math.cos(angulo) * raio_externo
            y1 = cy + math.sin(angulo) * raio_externo
            x2 = cx + math.cos(angulo) * raio_interno_tick
            y2 = cy + math.sin(angulo) * raio_interno_tick

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            if val in [-15, 0, 15]:
                tx = cx + math.cos(angulo) * (raio_interno - 38)
                ty = cy + math.sin(angulo) * (raio_interno - 38)

                texto = f"+{val}°" if val > 0 else f"{val}°"
                painter.setFont(QFont("Arial", 10, QFont.Bold))
                painter.drawText(int(tx - 20), int(ty - 10), 40, 20, Qt.AlignCenter, texto)

        angulo_graus = -self.valor * 2.0
        angulo = math.radians(angulo_graus)
        comprimento = raio_interno - 38

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(QColor(0, 0, 0, 100), 8))
        painter.drawLine(QPointF(cx + 3, cy + 4), QPointF(px + 3, py + 4))

        painter.setPen(QPen(QColor("#E00000"), 5))
        painter.drawLine(QPointF(cx, cy), QPointF(px, py))

        painter.setBrush(QBrush(QColor("#AAAAAA")))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawEllipse(int(cx - 9), int(cy - 9), 18, 18)

        painter.setBrush(QBrush(QColor("#DD0000")))
        painter.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)

        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        texto_valor = f"{self.valor:+.1f}°" if isinstance(self.valor, float) else f"{self.valor:+d}°"
        painter.drawText(int(cx - 60), int(cy + 40), 120, 30, Qt.AlignCenter, texto_valor)

        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(int(cx - 70), int(cy - 65), 140, 30, Qt.AlignCenter, "TRIM")

        painter.end()


# ============================================================
# COMBUSTÍVEL (COM BORDAS DOS SEGMENTOS ARREDONDADAS)
# ============================================================

class FuelIndicator(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(150, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()

        # Moldura externa
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(2, 2, 146, 296, 10, 10)

        # Título
        fonte = QFont("Arial", 13, QFont.Bold)
        painter.setFont(fonte)
        painter.setPen(QPen(Qt.white))
        painter.drawText(0, 12, w, 25, Qt.AlignCenter, "COMBUSTÍVEL")

        # Configuração das barras/segmentos
        largura, altura, espacamento = 45, 18, 7
        x = (w - largura) / 2
        y_inicial = 45
        preenchidos = 7

        for i in range(10):
            y = y_inicial + (9 - i) * (altura + espacamento)

            if i < preenchidos:
                painter.setBrush(QBrush(Qt.green))
            else:
                painter.setBrush(Qt.NoBrush)

            painter.setPen(QPen(Qt.black, 2))

            # Desenhando os segmentos com raio de canto 8px para um visual arredondado suave
            painter.drawRoundedRect(
                int(x),
                int(y),
                largura,
                altura,
                5,  # Raio X do arredondamento
                5   # Raio Y do arredondamento
            )

        # Marcações
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(5, int(y_inicial + 9 * (altura + espacamento)), 30, 20, Qt.AlignCenter, "E")
        painter.drawText(5, int(y_inicial + 4.5 * (altura + espacamento)), 30, 20, Qt.AlignCenter, "½")
        painter.drawText(5, int(y_inicial), 30, 20, Qt.AlignCenter, "F")

        painter.end()


# ============================================================
# PAINEL COMPLETO
# ============================================================

class Painel(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Painel Náutico")
        self.setFixedSize(1024, 600)
        self.setStyleSheet("QWidget { background-color: #0b1117; }")

        # 1. RPM
        self.rpm = GaugeRPM("RPM", 2500, 360)
        self.rpm.setParent(self)
        self.rpm.move(30, 10)
        #self.rpm.move(10, 70)

        # 2. TRIM
        self.trim = TrimGauge(valor=0, tamanho=230)
        self.trim.setParent(self)
        self.trim.move(380, 10)
        #self.trim.move(440, 70)

        # 3. VOLTAGEM (BATERIA)
        self.voltagem = Gauge("BATERIA", 12.6, "V", 10, 16, 230)
        self.voltagem.setParent(self)
        self.voltagem.move(610, 10)
        #self.voltagem.move(410, 380)

        # 4. COMBUSTÍVEL
        self.combustivel = FuelIndicator()
        self.combustivel.setParent(self)
        self.combustivel.move(860, 10)
        #self.combustivel.move(700, 370)

        # 5. TÍTULO DO PAINEL
        #titulo = QLabel("Embarcação: BUSCAPÉ I", self)
        #titulo.setGeometry(320, 20, 640, 40)
        #fonte = QFont("Arial", 22, QFont.Bold)
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