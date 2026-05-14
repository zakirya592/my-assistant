import sys
import json
import os
import asyncio
import edge_tts
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen, QFont, QRadialGradient
from datetime import datetime
import psutil
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QSlider,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
    QComboBox,
    QScrollArea,          # <-- added for right panel scrolling
)

# ==========================================
# WAVE ANIMATION
# ==========================================

class WaveWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

        self.setMinimumHeight(200)

    def animate(self):
        self.offset += 5
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(90, 0, 255))
        pen.setWidth(3)
        painter.setPen(pen)

        w = self.width()
        h = self.height()

        points = []

        for x in range(w):
            y = h / 2 + 30 * __import__("math").sin((x + self.offset) * 0.03)
            points.append((x, y))

        for i in range(len(points) - 1):
            painter.drawLine(
                int(points[i][0]),
                int(points[i][1]),
                int(points[i + 1][0]),
                int(points[i + 1][1]),
            )


# ==========================================
# GLOW CIRCLE MIC
# ==========================================

class GlowCircle(QWidget):
    def __init__(self):
        super().__init__()

        self.radius = 60
        self.grow = True

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

        self.setMinimumSize(250, 250)

    def animate(self):
        if self.grow:
            self.radius += 1
            if self.radius >= 70:
                self.grow = False
        else:
            self.radius -= 1
            if self.radius <= 60:
                self.grow = True

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2

        # Gradient glow rings - blue to purple
        for i in range(20):
            # Calculate color gradient from blue to purple
            progress = i / 20.0
            r = int(0 + (120 - 0) * progress)
            g = int(180 - (180 * progress))
            b = int(255)
            alpha = max(0, int(40 - i * 2))
            
            color = QColor(r, g, b, alpha)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(center_x - self.radius - i * 2.5),
                int(center_y - self.radius - i * 2.5),
                int((self.radius + i * 2.5) * 2),
                int((self.radius + i * 2.5) * 2),
            )

        # Main circle with gradient from blue to purple
        gradient = QRadialGradient(
            int(center_x), int(center_y), self.radius
        )
        gradient.setColorAt(0, QColor(100, 50, 255))  # Purple center
        gradient.setColorAt(1, QColor(0, 150, 255))   # Blue edge
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(center_x - self.radius),
            int(center_y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2),
        )

        # Mic icon - draw a proper microphone shape matching the first image
        painter.setPen(QPen(QColor("white"), 3))
        painter.setBrush(QColor("white"))
        
        # Microphone capsule - larger oval head
        painter.drawEllipse(
            int(center_x - 14),
            int(center_y - 28),
            28,
            32,
        )
        
        # Microphone stem
        painter.setPen(QPen(QColor("white"), 3))
        painter.drawLine(
            int(center_x),
            int(center_y + 4),
            int(center_x),
            int(center_y + 18),
        )
        
        # Bottom speaker part
        painter.drawEllipse(
            int(center_x - 6),
            int(center_y + 16),
            12,
            8,
        )


# ==========================================
# MAIN WINDOW
# ==========================================

class ZakirAI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZAKIR AI")
        self.setGeometry(100, 50, 1500, 900)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #060b1b;
            }

            QLabel {
                color: white;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #111d3a;
                border: 1px solid #243b73;
                border-radius: 12px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #1b2c57;
            }

            QFrame {
                background-color: #0c1329;
                border-radius: 18px;
            }

            QListWidget {
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #0f1830;
                border: 1px solid #243b73;
                border-radius: 15px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            
            QComboBox {
                background-color: #0f1830;
                border: 1px solid #243b73;
                border-radius: 12px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox QAbstractItemView {
                background-color: #0f1830;
                color: white;
                selection-background-color: #1b2c57;
            }
            
            /* Scroll area style */
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollBar:vertical {
                background: #0f1830;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # ==========================================
        # CENTRAL WIDGET
        # ==========================================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # ==========================================
        # LEFT PANEL (no scroll)
        # ==========================================

        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        # Logo
        logo = QLabel("⚡ ZAKIR AI")
        logo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        logo.setStyleSheet("padding: 10px;")
        sidebar_layout.addWidget(logo)

        # ==========================================
        # RECENT COMMANDS
        # ==========================================

        recent_card = QFrame()
        recent_card.setStyleSheet("""
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(0,200,255,0.15);
            border-radius: 20px;
        """)
        recent_layout = QVBoxLayout()
        recent_card.setLayout(recent_layout)
        recent_title = QLabel("🕘 Recent Commands")
        recent_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        recent_layout.addWidget(recent_title)
        recent_list = QListWidget()
        recent_list.setStyleSheet("""
            QListWidget{
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
            }
            QListWidget::item{
                padding: 5px;
            }
        """)
        recent_list.addItem("🎵 Open Spotify")
        recent_list.addItem("🌐 Search AI News")
        recent_layout.addWidget(recent_list)
        sidebar_layout.addWidget(recent_card)

        # ==========================================
        # SYSTEM STATUS
        # ==========================================

        system_card = QFrame()
        system_card.setStyleSheet("""
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(0,200,255,0.15);
            border-radius: 20px;
        """)
        system_layout = QVBoxLayout()
        system_card.setLayout(system_layout)
        sys_title = QLabel("💻 System Status")
        sys_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        system_layout.addWidget(sys_title)
        self.cpu_label = QLabel("⚙ CPU Usage       0%")
        self.ram_label = QLabel("🧠 Memory Usage   0%")
        self.disk_label = QLabel("💾 Disk Usage     0%")
        self.network_label = QLabel("🌐 Network        Checking...")
        for label in [self.cpu_label, self.ram_label, self.disk_label, self.network_label]:
            label.setStyleSheet("color: #8aa0d6; padding: 8px; font-size: 14px;")
            system_layout.addWidget(label)
        sidebar_layout.addWidget(system_card)
        
        # Update system status every 2 seconds
        system_timer = QTimer()
        system_timer.timeout.connect(self.update_system_status)
        system_timer.start(2000)
        self.update_system_status()  # Initial update

        # ==========================================
        # PROFILE CARD
        # ==========================================

        profile = QFrame()
        profile.setFixedHeight(95)
        profile.setStyleSheet("""
            QFrame{
                background-color: #0f172a;
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 22px;
            }
        """)
        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(18, 14, 18, 14)
        profile.setLayout(profile_layout)

        avatar = QLabel("Z")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(52, 52)
        avatar.setStyleSheet("""
            background:qlineargradient(
                x1:0,y1:0,
                x2:1,y2:1,
                stop:0 #2563eb,
                stop:1 #7c3aed
            );
            border-radius:26px;
            color:white;
            font-size:24px;
            font-weight:bold;
        """)
        profile_layout.addWidget(avatar)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setAlignment(Qt.AlignVCenter)
        name = QLabel("Zakirya")
        name.setStyleSheet("""
            QLabel{
                color:white;
                font-size:18px;
                font-weight:700;
                border:none;
                background:transparent;
            }
        """)
        online = QLabel("● Online")
        online.setStyleSheet("""
            QLabel{
                color:#22c55e;
                font-size:10px;
                font-weight:600;
                border:none;
                background:transparent;
            }
        """)
        info_layout.addWidget(name)
        info_layout.addWidget(online)
        profile_layout.addLayout(info_layout)
        sidebar_layout.addWidget(profile)

        # ==========================================
        # DATE & TIME SECTION
        # ==========================================

        datetime_card = QFrame()
        datetime_card.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                padding: 0px;
            }
        """)
        datetime_layout = QHBoxLayout()
        datetime_layout.setSpacing(10)
        datetime_layout.setContentsMargins(10, 5, 10, 5)
        datetime_card.setLayout(datetime_layout)

        icon_label = QLabel("🕐")
        icon_label.setFont(QFont("Segoe UI", 28))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(50, 50)

        time_date_layout = QVBoxLayout()
        time_date_layout.setSpacing(2)
        time_date_layout.setContentsMargins(0, 0, 0, 0)
        time_date_layout.setAlignment(Qt.AlignVCenter)

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.time_label.setStyleSheet("color: #00d4ff; background: transparent;")
        self.time_label.setAlignment(Qt.AlignLeft)

        self.date_label = QLabel()
        self.date_label.setFont(QFont("Segoe UI", 9))
        self.date_label.setStyleSheet("color: #38bdf8; background: transparent;")
        self.date_label.setAlignment(Qt.AlignLeft)

        time_date_layout.addWidget(self.time_label)
        time_date_layout.addWidget(self.date_label)

        datetime_layout.addWidget(icon_label)
        datetime_layout.addLayout(time_date_layout)

        self.update_datetime()
        datetime_timer = QTimer()
        datetime_timer.timeout.connect(self.update_datetime)
        datetime_timer.start(1000)

        sidebar_layout.addWidget(datetime_card)
        sidebar_layout.addStretch()

        # ==========================================
        # CENTER SECTION (no scroll)
        # ==========================================
        center_frame = QFrame()
        center_frame.setStyleSheet("background:#060b1b;")

        center_layout = QVBoxLayout()
        center_frame.setLayout(center_layout)

        # ==========================================
        # HEADER CARD (COMBINED)
        # ==========================================

        header_card = QFrame()
        header_card.setFixedHeight(100)
        header_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(0,200,255,0.15);
                border-radius: 20px;
                padding: 1px;
            }
        """)

        header_layout = QVBoxLayout()
        header_card.setLayout(header_layout)

        title = QLabel("Good Evening, Zakirya! 👋")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("background: transparent; border: none;")

        subtitle = QLabel("How can I help you today?")
        subtitle.setStyleSheet("""
            color: #8aa0d6;
            font-size: 15px;
            background: transparent;
            border: none;
        """)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        center_layout.addWidget(header_card)

        # ==========================================
        # MAIN LISTEN PANEL (AS ONE CARD)
        # ==========================================

        listen_card = QFrame()
        # listen_card.setFixedHeight(300)
        listen_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(0,200,255,0.15);
                border-radius: 20px;
                padding: 15px;
            }
        """)

        listen_layout = QVBoxLayout()
        listen_card.setLayout(listen_layout)

        # ==========================================
        # MIC (CENTERED)
        # ==========================================

        mic = GlowCircle()

        mic_container = QHBoxLayout()
        mic_container.addStretch()
        mic_container.addWidget(mic)
        mic_container.addStretch()

        listen_layout.addLayout(mic_container)

        # ==========================================
        # STATUS TEXT
        # ==========================================

        status = QLabel("I'm listening")
        status.setAlignment(Qt.AlignCenter)
        status.setFont(QFont("Segoe UI", 18, QFont.Bold))
        status.setStyleSheet("color:white; background:transparent; border:none;")

        sub_status = QLabel("Speak now...")
        sub_status.setAlignment(Qt.AlignCenter)
        sub_status.setStyleSheet("color:#8aa0d6; background:transparent; border:none;")

        listen_layout.addWidget(status)
        listen_layout.addWidget(sub_status)

        # ==========================================
        # STOP BUTTON
        # ==========================================

        stop_btn = QPushButton("⏹ Stop Listening")
        stop_btn.setFixedWidth(180)
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #111d3a;
                border: 1px solid #243b73;
                border-radius: 12px;
                padding: 8px;
                color: white;
            }
            QPushButton:hover {
                background-color: #1b2c57;
            }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(stop_btn)
        btn_layout.addStretch()

        listen_layout.addLayout(btn_layout)

        # ==========================================
        # ADD TO CENTER LAYOUT
        # ==========================================

        center_layout.addWidget(listen_card)

        # ==========================================
        # INPUT BAR
        # ==========================================

        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command or ask anything...")
        send_btn = QPushButton("➤")
        send_btn.setFixedWidth(60)
        input_layout.addWidget(self.input)
        input_layout.addWidget(send_btn)
        center_layout.addLayout(input_layout)

        # ==========================================
        # RIGHT PANEL (with QScrollArea)
        # ==========================================

        # Outer frame that holds the scroll area
        right_panel = QFrame()
        right_panel.setFixedWidth(354)
        right_panel.setStyleSheet("background: transparent; border: none;")

        # Create scroll area
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        right_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Container widget that will hold all right-side content
        right_container = QWidget()
        right_container.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_container)
        right_layout.setAlignment(Qt.AlignTop)

        # ------------------- CHAT CARD -------------------
        chat_card = QFrame()
        # chat_card.setFixedWidth(250)
        chat_card.setStyleSheet("""
            QFrame{
                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:1,
                    stop:0 #071122,
                    stop:1 #0b1730
                );
                border:1px solid rgba(255,255,255,0.05);
                border-radius:24px;
            }
        """)
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 5, 0, 0)
        chat_card.setLayout(chat_layout)

        chat_title = QLabel("🤖 AI Chat Mode")
        chat_title.setStyleSheet("""
            QLabel{
                color:white;
                font-size:22px;
                font-weight:800;
                background:transparent;
                border:none;
            }
        """)
        chat_layout.addWidget(chat_title)

        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 3)
        dot = QLabel()
        dot.setFixedSize(12, 12)
        dot.setStyleSheet("background:#22c55e; border-radius:6px;")
        active = QLabel("Active")
        active.setStyleSheet("""
            QLabel{
                color:white;
                font-size:15px;
                font-weight:600;
                background:transparent;
                border:none;
            }
        """)
        status_layout.addWidget(dot)
        status_layout.addSpacing(10)
        status_layout.addWidget(active)
        status_layout.addStretch()
        chat_layout.addLayout(status_layout)

        right_layout.addWidget(chat_card)

        # ------------------- BACKGROUND TASKS -------------------
        task_card = QFrame()
        task_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(0,200,255,0.15);
                border-radius: 18px;
                padding: 5px;
            }
        """)
        task_layout = QVBoxLayout(task_card)
        task_title = QLabel("📊 Background Tasks")
        task_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        task_layout.addWidget(task_title)

        def task_item(name, color, state):
            row = QFrame()
            row.setStyleSheet("border:none;")
            r = QHBoxLayout(row)
            name_label = QLabel(name)
            name_label.setStyleSheet("color:white;")
            state_label = QLabel(state)
            state_label.setStyleSheet(f"color:{color}; font-weight:bold;")
            r.addWidget(name_label)
            r.addStretch()
            r.addWidget(state_label)
            return row

        task_layout.addWidget(task_item("File Search", "#00ff99", "Running"))
        task_layout.addWidget(task_item("Web Scraping", "#ff6b6b", "Running"))
        right_layout.addWidget(task_card)

        # ------------------- MEMORY SNAPSHOT -------------------
        memory_card = QFrame()
        memory_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 10px;
            }
        """)
        memory_layout = QVBoxLayout(memory_card)
        mem_title = QLabel("🧠 Memory Snapshot")
        mem_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        memory_layout.addWidget(mem_title)

        def chip(key, value):
            row = QFrame()
            row.setStyleSheet("background: rgba(0,200,255,0.08); border-radius: 10px; padding: 6px;")
            r = QHBoxLayout(row)
            k = QLabel(key)
            k.setStyleSheet("color:#8aa0d6;")
            v = QLabel(value)
            v.setStyleSheet("color:white; font-weight:bold;")
            r.addWidget(k)
            r.addStretch()
            r.addWidget(v)
            return row

        # Load and display memory.json data
        try:
            memory_file = os.path.join(os.path.dirname(__file__), "memory.json")
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                    for key, value in memory_data.items():
                        memory_layout.addWidget(chip(key.title(), str(value)))
            else:
                memory_layout.addWidget(chip("Status", "No memory.json"))
        except Exception as e:
            memory_layout.addWidget(chip("Status", f"Error: {str(e)}"))
        
        memory_status = QLabel("🟢 Memory Sync Active")
        memory_status.setStyleSheet("color:#00ff99; font-weight:bold;")
        memory_layout.addWidget(memory_status)
        right_layout.addWidget(memory_card)

        # ==========================================
        # VOICE SETTINGS CARD (dropdown + side-by-side slider & percent)
        # ==========================================

        voice_card = QFrame()
        voice_card.setStyleSheet("""
            QFrame{
                background:qlineargradient(
                    x1:0,y1:0,
                    x2:1,y2:1,
                    stop:0 #071122,
                    stop:1 #0b1730
                );
                border:1px solid rgba(255,255,255,0.05);
                border-radius:24px;
            }
        """)
        voice_layout = QVBoxLayout()
        voice_card.setLayout(voice_layout)

        voice_title = QLabel("🎤 Voice Settings")
        voice_title.setStyleSheet("""
            QLabel{
                color:white;
                font-size:22px;
                font-weight:800;
                background:transparent;
                border:none;
            }
        """)
        voice_layout.addWidget(voice_title)

        # Voice Engine Dropdown
        engine_box = QFrame()
        engine_box.setStyleSheet("""
            QFrame{
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.04);
                border-radius:18px;
            }
        """)
        engine_layout = QVBoxLayout()
        engine_box.setLayout(engine_layout)
        
        self.voice_engine_combo = QComboBox()
        self.voice_engine_combo.addItem("Loading voices...")
        self.voice_engine_combo.setStyleSheet("""
            QComboBox {
                background-color: #0f1830;
                border: 1px solid #3b82f6;
                border-radius: 12px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        engine_layout.addWidget(self.voice_engine_combo)
        voice_layout.addWidget(engine_box)

        # Volume Section (slider and percent side by side)
        volume_frame = QFrame()
        volume_frame.setStyleSheet("""
            QFrame{
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.04);
                border-radius:18px;
            }
        """)
        volume_layout = QVBoxLayout()
        volume_frame.setLayout(volume_layout)
        
        slider_percent_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setValue(80)
        slider.setStyleSheet("""
            QSlider::groove:horizontal{
                background:#0f172a;
                height:8px;
                border-radius:4px;
            }
            QSlider::handle:horizontal{
                background:#3b82f6;
                width:18px;
                margin:-6px 0;
                border-radius:9px;
            }
            QSlider::sub-page:horizontal{
                background:#3b82f6;
                border-radius:4px;
            }
        """)
        volume_percent = QLabel("80%")
        volume_percent.setStyleSheet("color:#22c55e; font-size:14px; font-weight:700; background:transparent; border:none;")
        volume_percent.setFixedWidth(45)
        
        slider_percent_layout.addWidget(slider)
        slider_percent_layout.addWidget(volume_percent)
        
        volume_layout.addLayout(slider_percent_layout)
        
        def update_volume(value):
            volume_percent.setText(f"{value}%")
        slider.valueChanged.connect(update_volume)
        
        voice_layout.addWidget(volume_frame)
        
        right_layout.addWidget(voice_card)
        right_layout.addStretch()

        # Assign the container to the scroll area
        right_scroll.setWidget(right_container)

        # Put the scroll area inside the right panel frame
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.addWidget(right_scroll)

        # ==========================================
        # ADD ALL TO MAIN LAYOUT
        # ==========================================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(center_frame)
        main_layout.addWidget(right_panel)

        # Load voices from edge_tts
        self.load_voices()

    def load_voices(self):
        """
        Load all available voices from edge_tts and populate the combo box.
        Handles asyncio safely without freezing the UI.
        Format: "ShortName (Gender)"
        """
        try:
            # Try to run asyncio safely - handle case where event loop already exists
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running (e.g., in Jupyter), use a different approach
                    voices = asyncio.run_coroutine_threadsafe(
                        edge_tts.list_voices(), loop
                    ).result()
                else:
                    # Loop exists but not running, we can use it
                    voices = loop.run_until_complete(edge_tts.list_voices())
            except RuntimeError:
                # No event loop exists, create a new one
                voices = asyncio.run(edge_tts.list_voices())

            # Clear the combo box and populate with voices
            self.voice_engine_combo.clear()

            # Sort voices by locale for better organization
            sorted_voices = sorted(
                voices,
                key=lambda v: (v.get("Locale", ""), v.get("ShortName", ""))
            )

            # Add voices in the format "ShortName (Gender)"
            for voice in sorted_voices:
                short_name = voice.get("ShortName", "Unknown")
                gender = voice.get("Gender", "Unknown")
                display_name = f"{short_name} ({gender})"
                self.voice_engine_combo.addItem(display_name, short_name)

            # Set default voice
            if self.voice_engine_combo.count() > 0:
                # Try to find and select en-US-GuyNeural as default
                for i in range(self.voice_engine_combo.count()):
                    if "en-US-GuyNeural" in self.voice_engine_combo.itemText(i):
                        self.voice_engine_combo.setCurrentIndex(i)
                        break

        except Exception as e:
            print(f"Error loading voices: {e}")
            # Fallback to default voices if fetch fails
            self.voice_engine_combo.clear()
            default_voices = [
                ("en-US-GuyNeural", "Guy (Male)"),
                ("en-US-JennyNeural", "Jenny (Female)"),
                ("en-GB-RyanNeural", "Ryan (Male)"),
                ("en-IN-PrabhatNeural", "Prabhat (Male)"),
            ]
            for short_name, display_name in default_voices:
                self.voice_engine_combo.addItem(display_name, short_name)

    def update_datetime(self):
        """Update time and date display"""
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%A, %B %d, %Y")
        self.time_label.setText(time_str)
        self.date_label.setText(date_str)

    def update_system_status(self):
        """Update system status with real-time data"""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_label.setText(f"⚙ CPU Usage       {int(cpu_percent)}%")
            
            # Memory Usage
            memory = psutil.virtual_memory()
            self.ram_label.setText(f"🧠 Memory Usage   {int(memory.percent)}%")
            
            # Disk Usage
            disk = psutil.disk_usage('/')
            self.disk_label.setText(f"💾 Disk Usage     {int(disk.percent)}%")
            
            # Network Status
            try:
                net_io = psutil.net_io_counters()
                if net_io.bytes_sent > 0 or net_io.bytes_recv > 0:
                    self.network_label.setText("🌐 Network        Active")
                else:
                    self.network_label.setText("🌐 Network        Idle")
            except:
                self.network_label.setText("🌐 Network        Stable")
        except Exception as e:
            print(f"Error updating system status: {e}")


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZakirAI()
    window.show()
    sys.exit(app.exec_())