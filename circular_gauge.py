import sys
import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel


# ============================================================
# INSTRUMENTO CIRCULAR
# ============================================================

class Gauge(QWidget):

    def __init__(
        self,
        titulo,
        valor,
        unidade,
        minimo,
        maximo,
        tamanho
    ):
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

        w = self.width()
        h = self.height()

        cx = w / 2
        cy = h / 2

        raio = min(w, h) * 0.45

        # ----------------------------------------------------
        # FUNDO DO INSTRUMENTO
        # ----------------------------------------------------

        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            QPointF(cx, cy),
            raio,
            raio
        )

        # ----------------------------------------------------
        # BORDA EXTERNA
        # ----------------------------------------------------

        pen = QPen(Qt.white)
        pen.setWidth(3)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(
            QPointF(cx, cy),
            raio,
            raio
        )

        # ----------------------------------------------------
        # ESCALA
        # ----------------------------------------------------

        painter.setPen(QPen(Qt.white, 2))

        quantidade = 10

        for i in range(quantidade + 1):

            proporcao = i / quantidade

            angulo_graus = 135 + proporcao * 270
            angulo = math.radians(angulo_graus)

            raio_externo = raio * 0.91
            raio_interno = raio * 0.82

            x1 = cx + math.cos(angulo) * raio_interno
            y1 = cy + math.sin(angulo) * raio_interno

            x2 = cx + math.cos(angulo) * raio_externo
            y2 = cy + math.sin(angulo) * raio_externo

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

        # ----------------------------------------------------
        # PONTEIRO
        # ----------------------------------------------------

        proporcao = (
            self.valor - self.minimo
        ) / (
            self.maximo - self.minimo
        )

        angulo_graus = 135 + proporcao * 270
        angulo = math.radians(angulo_graus)

        raio_ponteiro = raio * 0.67

        px = cx + math.cos(angulo) * raio_ponteiro
        py = cy + math.sin(angulo) * raio_ponteiro

        pen = QPen(Qt.red)
        pen.setWidth(5)

        painter.setPen(pen)

        painter.drawLine(
            QPointF(cx, cy),
            QPointF(px, py)
        )

        # ----------------------------------------------------
        # CENTRO DO PONTEIRO
        # ----------------------------------------------------

        painter.setBrush(QBrush(Qt.white))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            QPointF(cx, cy),
            7,
            7
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        fonte = QFont("Arial", 17)
        fonte.setBold(True)

        painter.setFont(fonte)
        painter.setPen(QPen(Qt.white))

        painter.drawText(
            0,
            int(cy - raio * 0.55),
            w,
            30,
            Qt.AlignCenter,
            self.titulo
        )

        # ----------------------------------------------------
        # VALOR
        # ----------------------------------------------------

        fonte = QFont("Arial", 25)
        fonte.setBold(True)

        painter.setFont(fonte)

        if self.titulo == "VOLTAGEM":

            texto = f"{self.valor:.1f}"

        else:

            texto = f"{self.valor:.0f}"

        painter.drawText(
            0,
            int(cy + raio * 0.30),
            w,
            40,
            Qt.AlignCenter,
            texto
        )

        # ----------------------------------------------------
        # UNIDADE
        # ----------------------------------------------------

        fonte = QFont("Arial", 11)

        painter.setFont(fonte)

        painter.drawText(
            0,
            int(cy + raio * 0.58),
            w,
            25,
            Qt.AlignCenter,
            self.unidade
        )


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
            "PAINEL NÁUTICO",
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