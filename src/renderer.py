from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QLineEdit
from PySide6.QtCore import Qt, QSize
from .components import UIComponent

class UIRenderer:
    """
    Renders a tree of UIComponent objects into a live widget preview.
    """

    def __init__(self, device_preset):
        self.device_preset = device_preset
        self.device_frame = None

    def render(self, parent_widget: QWidget, component_tree: UIComponent):
        """
        Renders the entire component tree into the parent widget.
        """
        # Clear previous widgets
        while parent_widget.layout().count():
            child = parent_widget.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not component_tree:
            # Show a placeholder if parsing fails or input is empty
            placeholder = QLabel("Start typing your UI code...")
            placeholder.setAlignment(Qt.AlignCenter)
            parent_widget.layout().addWidget(placeholder)
            return

        # Create the device frame
        self.device_frame = QFrame(parent_widget)
        self.device_frame.setFixedSize(self.device_preset.width, self.device_preset.height)
        self.device_frame.setObjectName("DeviceFrame")
        self.device_frame.setStyleSheet("#DeviceFrame { border: 10px solid black; border-radius: 20px; background-color: white; }")

        # The main layout for the content inside the device frame
        device_content_layout = QVBoxLayout(self.device_frame)
        device_content_layout.setContentsMargins(5, 15, 5, 15) # Margins to simulate phone bezels

        # Recursively create and add the root widget
        root_widget = self._create_widget(component_tree)
        if root_widget:
            device_content_layout.addWidget(root_widget)

        parent_widget.layout().addWidget(self.device_frame)

    def _create_widget(self, component: UIComponent) -> QWidget:
        """
        Recursively creates a widget from a UIComponent.
        """
        widget_type = component.type.lower()

        if widget_type == 'container':
            return self._create_container(component)
        elif widget_type == 'button':
            return self._create_button(component)
        elif widget_type == 'text':
            return self._create_text(component)
        elif widget_type == 'textfield':
            return self._create_textfield(component)

        # Return a placeholder for unknown components
        return QLabel(f"Unknown component: {component.type}")

    def _create_container(self, component: UIComponent) -> QWidget:
        """Creates a container widget with a layout to hold children."""
        container = QWidget()
        # For now, all containers use a vertical layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Apply layout parameters
        alignment = component.layout_params.get('alignment', 'top')
        if alignment == 'center':
            layout.setAlignment(Qt.AlignCenter)
        elif alignment == 'bottom':
            layout.setAlignment(Qt.AlignBottom)
        else:
            layout.setAlignment(Qt.AlignTop)

        # Recursively create and add children
        for child_component in component.children:
            child_widget = self._create_widget(child_component)
            if child_widget:
                layout.addWidget(child_widget)

        return container

    def _create_button(self, component: UIComponent) -> QPushButton:
        """Creates a styled QPushButton."""
        text = component.properties.get('text', 'Button')
        button = QPushButton(text)
        button.setMinimumHeight(44) # Good practice for touch targets

        # Basic Material Design styling
        bg_color = component.properties.get('color', 'rgb(98, 0, 238)') # Material Purple
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:pressed {{
                background-color: rgb(49, 0, 119);
            }}
        """)
        return button

    def _create_text(self, component: UIComponent) -> QLabel:
        """Creates a QLabel for displaying text."""
        text = component.properties.get('value', 'Text')
        label = QLabel(text)
        label.setWordWrap(True)

        # Basic Material Design styling
        font_size = component.properties.get('size', 16)
        label.setStyleSheet(f"font-size: {font_size}px; color: #333;")

        # Apply layout parameters
        alignment = component.layout_params.get('alignment', 'left')
        if alignment == 'center':
            label.setAlignment(Qt.AlignCenter)
        elif alignment == 'right':
            label.setAlignment(Qt.AlignRight)
        else:
            label.setAlignment(Qt.AlignLeft)

        return label