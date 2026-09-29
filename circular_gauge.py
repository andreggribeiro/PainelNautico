import sys
import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget, QLabel


# ============================================================
# INSTRUMENTO CIRCULAR
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

        cx = self.width() / 2
        cy = self.height() / 2

        raio = min(self.width(), self.height()) / 2 - 8

        # =====================================================
        # 1. SOMBRA EXTERNA
        # =====================================================

        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(Qt.black))

        painter.drawEllipse(
            int(cx - raio + 5),
            int(cy - raio + 7),
            int(raio * 2),
            int(raio * 2)
        )

        # =====================================================
        # 2. ARO EXTERNO
        # =====================================================

        gradiente_aro = QRadialGradient(
        cx - 20,
        cy - 25,
        raio
    )

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

        # =====================================================
        # 3. MOSTRADOR INTERNO
        # =====================================================

        raio_interno = raio - 12

        gradiente_mostrador = QRadialGradient(
        cx - 35,
        cy - 40,
        raio_interno
    )

        gradiente_mostrador.setColorAt(0.0, QColor("#4A4A4A"))
        gradiente_mostrador.setColorAt(0.35, QColor("#303030"))
        gradiente_mostrador.setColorAt(0.70, QColor("#1C1C1C"))
        gradiente_mostrador.setColorAt(1.0, QColor("#0C0C0C"))

        painter.setBrush(QBrush(gradiente_mostrador))
        painter.setPen(QPen(QColor("#080808"), 3))

        painter.drawEllipse(
            int(cx - raio_interno),
            int(cy - raio_interno),
            int(raio_interno * 2),
            int(raio_interno * 2)
        )

        # =====================================================
        # 4. ESCALA
        # =====================================================

        painter.setPen(QPen(Qt.white, 3))

        for i in range(11):

            valor = self.minimo + (
                (self.maximo - self.minimo) / 10
            ) * i

            angulo_graus = 135 + (270 / 10) * i
            angulo = math.radians(angulo_graus)

            raio_externo = raio_interno - 8
            raio_interno_tick = raio_interno - 22

            x1 = cx + math.cos(angulo) * raio_externo
            y1 = cy + math.sin(angulo) * raio_externo

            x2 = cx + math.cos(angulo) * raio_interno_tick
            y2 = cy + math.sin(angulo) * raio_interno_tick

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

        # =====================================================
        # 5. PONTEIRO
        # =====================================================

        proporcao = (
            self.valor - self.minimo
        ) / (
            self.maximo - self.minimo
        )

        proporcao = max(0.0, min(1.0, proporcao))

        angulo_graus = 135 + 270 * proporcao
        angulo = math.radians(angulo_graus)

        comprimento = raio_interno - 38

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        # Sombra do ponteiro
        painter.setPen(
            QPen(QColor("#000000"), 8)
        )

        painter.drawLine(
            QPointF(cx + 3, cy + 4),
            QPointF(px + 3, py + 4)
        )

        # Ponteiro
        painter.setPen(
            QPen(QColor("#E00000"), 5)
        )

        painter.drawLine(
            QPointF(cx, cy),
            QPointF(px, py)
        )

        # =====================================================
        # 6. EIXO DO PONTEIRO
        # =====================================================

        painter.setBrush(
            QBrush(QColor("#AAAAAA"))
        )

        painter.setPen(
            QPen(QColor("#333333"), 2)
        )

        painter.drawEllipse(
            int(cx - 9),
            int(cy - 9),
            18,
            18
        )

        painter.setBrush(
            QBrush(QColor("#DD0000"))
        )

        painter.drawEllipse(
            int(cx - 4),
            int(cy - 4),
            8,
            8
        )

        # =====================================================
        # 7. VALOR
        # =====================================================

        painter.setPen(QPen(Qt.white))
        painter.setFont(
            QFont("Arial", 24, QFont.Bold)
        )

        texto_valor = str(int(self.valor))

        painter.drawText(
            int(cx - 60),
            int(cy + 55),
            120,
            40,
            Qt.AlignCenter,
            texto_valor
        )

        # =====================================================
        # 8. UNIDADE
        # =====================================================

        painter.setFont(
            QFont("Arial", 11)
        )

        painter.drawText(
            int(cx - 50),
            int(cy + 82),
            100,
            25,
            Qt.AlignCenter,
            self.unidade
        )

        # =====================================================
        # 9. TÍTULO
        # =====================================================

        painter.setFont(
            QFont("Arial", 16, QFont.Bold)
        )

        painter.drawText(
            int(cx - 70),
            int(cy - 70),
            140,
            30,
            Qt.AlignCenter,
            self.titulo
        )

        painter.end()

# ============================================================
# TRIM
# ============================================================

class TrimGauge(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 300)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Centro e raio do instrumento
        cx = 150
        cy = 150
        raio = 140

        # =====================================================
        # FUNDO DO RELÓGIO
        # =====================================================

        painter.setBrush(QBrush(Qt.black))
        painter.setPen(QPen(Qt.white, 3))

        painter.drawEllipse(
            cx - raio,
            cy - raio,
            raio * 2,
            raio * 2
        )

        # =====================================================
        # ESCALA DO TRIM
        #
        # 0°   = horizontal para a direita
        # +15° = para cima
        # -15° = para baixo
        # =====================================================

        painter.setPen(QPen(Qt.white, 3))

        for valor in range(-15, 16, 5):

            # No sistema de coordenadas da tela,
            # Y aumenta para baixo.
            angulo_graus = -valor*2
            angulo = math.radians(angulo_graus)

            x1 = cx + math.cos(angulo) * 105
            y1 = cy + math.sin(angulo) * 105

            x2 = cx + math.cos(angulo) * 135
            y2 = cy + math.sin(angulo) * 135

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

        # =====================================================
        # VALORES DA ESCALA
        # =====================================================

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 11))

        painter.drawText(
            195,
            82,
            "+15°"
        )

        painter.drawText(
            218,
            155,
            "0°"
        )

        painter.drawText(
            195,
            235,
            "-15°"
        )

        # =====================================================
        # PONTEIRO
        #
        # Por enquanto permanece em 0°.
        # =====================================================

        valor_trim = 0

        angulo_graus = -valor_trim
        angulo = math.radians(angulo_graus)

        comprimento = 100

        px = cx + math.cos(angulo) * comprimento
        py = cy + math.sin(angulo) * comprimento

        painter.setPen(QPen(Qt.red, 5))

        painter.drawLine(
            QPointF(cx, cy),
            QPointF(px, py)
        )

        # =====================================================
        # CENTRO DO PONTEIRO
        # =====================================================

        painter.setBrush(QBrush(Qt.red))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            cx - 7,
            cy - 7,
            14,
            14
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 16, QFont.Bold))

        painter.drawText(
            115,
            275,
            "TRIM"
        )

        painter.end()

# ============================================================
# COMBUSTÍVEL
# ============================================================

class FuelIndicator(QWidget):

    def __init__(self):

        super().__init__()

        self.setFixedSize(150, 300)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()

        # =====================================================
        # MOLDURA
        # =====================================================

        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)

        painter.drawRoundedRect(
            2,
            2,
            146,
            296,
            10,
            10
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        fonte = QFont("Arial", 15)
        fonte.setBold(True)

        painter.setFont(fonte)
        painter.setPen(QPen(Qt.white))

        painter.drawText(
            0,
            5,
            w,
            25,
            Qt.AlignCenter,
            "COMBUSTÍVEL"
        )

        # ----------------------------------------------------
        # SEGMENTOS
        # ----------------------------------------------------

        largura = 45
        altura = 18
        espacamento = 7

        x = (w - largura) / 2

        y_inicial = 45

        # Apenas representação gráfica de 70%.

        preenchidos = 7

        for i in range(10):

            y = (
                y_inicial
                +
                (9 - i) *
                (altura + espacamento)
            )

            if i < preenchidos:

                painter.setBrush(
                    QBrush(Qt.green)
                )

            else:

                painter.setBrush(
                    Qt.NoBrush
                )

            painter.setPen(
                QPen(Qt.white, 2)
            )

            painter.drawRoundedRect(
                int(x),
                int(y),
                largura,
                altura,
                3,
                3
            )

        # ----------------------------------------------------
        # MARCAÇÕES
        # ----------------------------------------------------

        fonte = QFont("Arial", 10)
        painter.setFont(fonte)

        painter.drawText(
            0,
            y_inicial + 10,
            30,
            20,
            Qt.AlignCenter,
            "E"
        )

        painter.drawText(
            0,
            y_inicial + 5 * (altura + espacamento) + 10,
            30,
            20,
            Qt.AlignCenter,
            "½"
        )

        painter.drawText(
            0,
            y_inicial + 9 * (altura + espacamento) + 10,
            30,
            20,
            Qt.AlignCenter,
            "F"
        )


# ============================================================
# PAINEL
# ============================================================

class Painel(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Painel Náutico"
        )

        self.setFixedSize(
            1280,
            720
        )

        self.setStyleSheet(
            """
            QWidget {
                background-color: #0b1117;
            }
            """
        )

        # ----------------------------------------------------
        # RPM
        # ----------------------------------------------------

        self.rpm = Gauge(
            "RPM",
            1200,
            "RPM",
            0,
            6000,
            430
        )

        self.rpm.setParent(self)

        self.rpm.move(
            10,
            170
            #55,
            #125
        )

        # ----------------------------------------------------
        # TRIM
        # ----------------------------------------------------

        self.trim = TrimGauge()

        self.trim.setParent(self)

        self.trim.move(
            400,
            100
            #570,
            #70
        )

        # ----------------------------------------------------
        # VOLTAGEM
        # ----------------------------------------------------

        self.voltagem = Gauge(
            "BATERIA",
            12.6,
            "V",
            10,
            16,
            300
        )

        self.voltagem.setParent(self)

        self.voltagem.move(
            400,
            380
            #570,
            #385
        )

        # ----------------------------------------------------
        # COMBUSTÍVEL
        # ----------------------------------------------------

        self.combustivel = FuelIndicator()

        self.combustivel.setParent(self)

        self.combustivel.move(
            700,
            370
            #1060,
            #205
        )

        # ----------------------------------------------------
        # TÍTULO DO PAINEL
        # ----------------------------------------------------

        titulo = QLabel(
            "Embarcação: BUSCAPÉ I",
            self
        )

        titulo.setGeometry(
            0,
            20,
            1280,
            40
        )

        fonte = QFont("Arial", 22)
        fonte.setBold(True)

        titulo.setFont(fonte)
        titulo.setStyleSheet(
            "color: white;"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    painel = Painel()

    painel.show()

    sys.exit(
        app.exec()
    )