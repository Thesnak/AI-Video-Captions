from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt6.QtWidgets import QWidget

class WidgetAnimations:
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 500):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        return animation

    @staticmethod
    def slide_in(widget: QWidget, direction: str = "right", duration: int = 500):
        animation = QPropertyAnimation(widget, b"pos")
        start_pos = widget.pos()
        
        if direction == "right":
            animation.setStartValue(QPoint(start_pos.x() - 100, start_pos.y()))
        elif direction == "left":
            animation.setStartValue(QPoint(start_pos.x() + 100, start_pos.y()))
        
        animation.setEndValue(start_pos)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation

    @staticmethod
    def expand(widget: QWidget, duration: int = 500):
        animation = QPropertyAnimation(widget, b"size")
        final_size = widget.size()
        animation.setStartValue(QSize(final_size.width(), 0))
        animation.setEndValue(final_size)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation

