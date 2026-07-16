from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QGraphicsObject

class PointItem(QGraphicsObject):

    CROSS_SIZE = 7

    def __init__(self, point):
        super().__init__()

        self.point = point

        self.font = QFont()
        self.font.setPointSize(10)

        self.padding = 3

        fm = QFontMetrics(self.font)

        self.label_rect = QRectF(
            self.CROSS_SIZE + 4,
            -fm.height()/2 - self.padding,
            fm.horizontalAdvance(point.label) + 2*self.padding,
            fm.height() + 2*self.padding,
        )

        self.setPos(
            point.image_x,
            point.image_y,
        )

        from PySide6.QtWidgets import QGraphicsItem

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations,
            True,
        )

    def boundingRect(self):

        s = self.CROSS_SIZE

        return QRectF(
            -s,
            -s,
            self.label_rect.right() + 2,
            2*s,
        )
    
    def paint(self, painter, option, widget):

        if self.point.kind == "calibration":
            color = QColor(0,0,255)
        else:
            color = QColor(255,0,0)

        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(color,2)
        painter.setPen(pen)

        s = self.CROSS_SIZE

        painter.drawLine(-s,-s,s,s)
        painter.drawLine(-s,s,s,-s)

        painter.setBrush(QColor(255,255,255,180))
        painter.setPen(Qt.NoPen)

        painter.drawRoundedRect(
            self.label_rect,
            3,
            3,
        )

        painter.setPen(Qt.black)
        painter.setFont(self.font)

        painter.drawText(
            self.label_rect.adjusted(
                self.padding,
                self.padding,
                -self.padding,
                -self.padding,
            ),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.point.label,
        )