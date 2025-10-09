import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QToolBar,
    QComboBox,
    QLabel,
)
from PySide6.QtCore import Qt, QTimer

from .components import DevicePreset
from .parser import parse_dsl
from .renderer import UIRenderer

# Device presets
DEVICE_PRESETS = [
    DevicePreset(name="iPhone X", width=375, height=812),
    DevicePreset(name="Samsung S21", width=360, height=800),
    DevicePreset(name="iPad Pro", width=1024, height=1366),
    DevicePreset(name="Desktop", width=1920, height=1080),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live UI Renderer")
        self.setGeometry(100, 100, 1200, 800)

        self.current_device = DEVICE_PRESETS[0]
        self.renderer = UIRenderer(self.current_device)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)


        # Toolbar for device selection
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        self.device_selector = QComboBox()
        self.device_selector.addItems([d.name for d in DEVICE_PRESETS])
        self.device_selector.currentIndexChanged.connect(self.device_changed)
        toolbar.addWidget(QLabel("Device: "))
        toolbar.addWidget(self.device_selector)

        # Splitter for editor and preview
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Code Editor
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("Enter UI description here...")
        self.code_editor.textChanged.connect(self.schedule_update)
        splitter.addWidget(self.code_editor)

        # Device Preview Panel
        self.preview_panel = QWidget()
        preview_layout = QVBoxLayout(self.preview_panel)
        preview_layout.setAlignment(Qt.AlignCenter)
        splitter.addWidget(self.preview_panel)

        # Debounce timer for live updates
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_preview)

        # Set initial sizes for the splitter
        splitter.setSizes([400, 800])

        # Initial render
        self.update_preview()

    def schedule_update(self):
        """Schedules a UI update after a short delay."""
        self.update_timer.start(300) # 300ms delay

    def update_preview(self):
        """Parses the code and re-renders the preview."""
        code = self.code_editor.toPlainText()
        if not code.strip():
             # Clear the panel if there is no code
            while self.preview_panel.layout().count():
                child = self.preview_panel.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            placeholder = QLabel("Start typing your UI code...")
            placeholder.setAlignment(Qt.AlignCenter)
            self.preview_panel.layout().addWidget(placeholder)
            return

        component_tree = parse_dsl(code)
        self.renderer.render(self.preview_panel, component_tree)

    def device_changed(self, index):
        """Handles device selection change."""
        self.current_device = DEVICE_PRESETS[index]
        self.renderer.device_preset = self.current_device
        self.update_preview()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())