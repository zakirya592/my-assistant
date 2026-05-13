# ==========================================
# ZAKIR AI - FUTURISTIC AI ASSISTANT UI
# Python + PyQt5
# ==========================================

# INSTALL:
# pip install PyQt5

import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
from datetime import datetime
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

        # Glow
        for i in range(15):
            color = QColor(0, 180, 255, 15 - i)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(center_x - self.radius - i * 3),
                int(center_y - self.radius - i * 3),
                int((self.radius + i * 3) * 2),
                int((self.radius + i * 3) * 2),
            )

        # Main circle
        painter.setBrush(QColor(120, 0, 255))
        painter.drawEllipse(
            int(center_x - self.radius),
            int(center_y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2),
        )

        # Mic icon
        painter.setPen(QPen(QColor("white"), 5))

        painter.drawLine(
            int(center_x),
            int(center_y - 20),
            int(center_x),
            int(center_y + 20),
        )

        painter.drawEllipse(
            int(center_x - 15),
            int(center_y - 40),
            30,
            50,
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
        """)

        # ==========================================
        # CENTRAL WIDGET
        # ==========================================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # ==========================================
        # LEFT PANEL
        # ==========================================

        sidebar = QFrame()

        sidebar.setFixedWidth(320)

        sidebar_layout = QVBoxLayout()

        sidebar.setLayout(sidebar_layout)

        # Logo
        logo = QLabel("⚡ ZAKIR AI")

        logo.setFont(QFont("Segoe UI", 22, QFont.Bold))

        logo.setStyleSheet("""
            padding: 10px;
        """)

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
        # recent_list.addItem("📂 Find project folder")
        # recent_list.addItem("📸 Take Screenshot")
        # recent_list.addItem("🔊 Volume Up")

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

        cpu = QLabel("⚙ CPU Usage       23%")
        ram = QLabel("🧠 Memory Usage   61%")
        disk = QLabel("💾 Disk Usage     45%")
        network = QLabel("🌐 Network        Stable")

        for label in [cpu, ram, disk, network]:

            label.setStyleSheet("""
                color: #8aa0d6;
                padding: 8px;
                font-size: 14px;
            """)

            system_layout.addWidget(label)

        sidebar_layout.addWidget(system_card)


            # ==========================================
        # EXACT IMAGE STYLE PROFILE CARD
        # LEFT SIDE BOTTOM
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

        # ==========================================
        # AVATAR
        # ==========================================

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


        # ==========================================
        # USER INFO
        # ==========================================

        info_layout = QVBoxLayout()

        info_layout.setSpacing(2)
        info_layout.setAlignment(Qt.AlignVCenter)


        # NAME

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

        # ONLINE

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

        # Icon on the left
        icon_label = QLabel("🕐")
        icon_label.setFont(QFont("Segoe UI", 28))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(50, 50)
        
        # Vertical layout for time and date (centered)
        time_date_layout = QVBoxLayout()
        time_date_layout.setSpacing(2)
        time_date_layout.setContentsMargins(0, 0, 0, 0)
        time_date_layout.setAlignment(Qt.AlignVCenter)

        # Time label (12-hour format with AM/PM)
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.time_label.setStyleSheet("color: #00d4ff; background: transparent;")
        self.time_label.setAlignment(Qt.AlignLeft)

        # Date and day label
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Segoe UI", 9))
        self.date_label.setStyleSheet("color: #38bdf8; background: transparent;")
        self.date_label.setAlignment(Qt.AlignLeft)

        time_date_layout.addWidget(self.time_label)
        time_date_layout.addWidget(self.date_label)

        datetime_layout.addWidget(icon_label)
        datetime_layout.addLayout(time_date_layout)

        # Update time and date
        self.update_datetime()

        # Timer to update every second
        datetime_timer = QTimer()
        datetime_timer.timeout.connect(self.update_datetime)
        datetime_timer.start(1000)

        sidebar_layout.addWidget(datetime_card)
        sidebar_layout.addStretch()


        # ==========================================
        # CENTER SECTION
        # ==========================================

        center_frame = QFrame()

        center_layout = QVBoxLayout()
        center_frame.setLayout(center_layout)

        title = QLabel("Good Evening, Zakirya! 👋")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))

        subtitle = QLabel("How can I help you today?")
        subtitle.setStyleSheet("color: #8aa0d6; font-size: 15px;")

        center_layout.addWidget(title)
        center_layout.addWidget(subtitle)

        # ==========================================
        # MAIN LISTEN PANEL
        # ==========================================

        listen_panel = QFrame()
        listen_layout = QVBoxLayout()
        listen_panel.setLayout(listen_layout)

        wave = WaveWidget()
        mic = GlowCircle()

        mic_container = QHBoxLayout()
        mic_container.addStretch()
        mic_container.addWidget(mic)
        mic_container.addStretch()

        listen_layout.addWidget(wave)
        listen_layout.addLayout(mic_container)

        status = QLabel("I'm listening")
        status.setAlignment(Qt.AlignCenter)
        status.setFont(QFont("Segoe UI", 22, QFont.Bold))

        sub_status = QLabel("Speak now...")
        sub_status.setAlignment(Qt.AlignCenter)
        sub_status.setStyleSheet("color:#8aa0d6;")

        stop_btn = QPushButton("⏹ Stop Listening")
        stop_btn.setFixedWidth(200)

        stop_layout = QHBoxLayout()
        stop_layout.addStretch()
        stop_layout.addWidget(stop_btn)
        stop_layout.addStretch()

        listen_layout.addWidget(status)
        listen_layout.addWidget(sub_status)
        listen_layout.addLayout(stop_layout)

        center_layout.addWidget(listen_panel)

        # ==========================================
        # QUICK ACTIONS
        # ==========================================

        actions_frame = QFrame()
        actions_layout = QHBoxLayout()
        actions_frame.setLayout(actions_layout)

        actions = [
            "Open App",
            "Search Web",
            "Screenshot",
            "Volume Up",
            "Shutdown"
        ]

        for act in actions:
            btn = QPushButton(act)
            btn.setFixedHeight(80)
            actions_layout.addWidget(btn)

        center_layout.addWidget(actions_frame)

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
        # RIGHT PANEL
        # ==========================================

        right_panel = QFrame()
        right_panel.setFixedWidth(300)

        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # AI Chat Mode
        chat_card = QFrame()
        chat_layout = QVBoxLayout()
        chat_card.setLayout(chat_layout)

        chat_title = QLabel("🤖 AI Chat Mode")
        active = QLabel("Active")
        active.setStyleSheet("color: #00ff99;")

        chat_layout.addWidget(chat_title)
        chat_layout.addWidget(active)
        

        # Background Tasks
        task_card = QFrame()
        task_layout = QVBoxLayout()
        task_card.setLayout(task_layout)
        task_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(0,200,255,0.15);
                border-radius: 18px;
                padding: 5px;
            }
        """)
        t = QVBoxLayout(task_card)

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

            # r.addWidget(dot)
            r.addWidget(name_label)
            r.addStretch()
            r.addWidget(state_label)

            return row

        
        task_layout.addWidget(task_item("File Search", "#00ff99", "Running"))
        task_layout.addWidget(task_item("Web Scraping", "#ff6b6b", "Running"))

        # Memory Snapshot
        memory_card = QFrame()
        memory_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 10px;
            }
        """)
        m = QVBoxLayout(memory_card)
        title = QLabel("🧠 Memory Snapshot")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        m.addWidget(title)

        def chip(key, value):
            row = QFrame()
            row.setStyleSheet("""
                background: rgba(0,200,255,0.08);
                border-radius: 10px;
                padding: 6px;
            """)
            r = QHBoxLayout(row)

            k = QLabel(key)
            k.setStyleSheet("color:#8aa0d6;")

            v = QLabel(value)
            v.setStyleSheet("color:white; font-weight:bold;")

            r.addWidget(k)
            r.addStretch()
            r.addWidget(v)

            return row

        m.addWidget(chip("Language", "Python"))
        m.addWidget(chip("Project", "Zakir AI"))

        status = QLabel("🟢 Memory Sync Active")
        status.setStyleSheet("color:#00ff99; font-weight:bold;")
        m.addWidget(status)



        memory_layout = QVBoxLayout()
        memory_card.setLayout(memory_layout)

        memory_layout.addWidget(QLabel("Name: Zakirya"))
        memory_layout.addWidget(QLabel("Favorite Language: Python"))
        memory_layout.addWidget(QLabel("Project: AI Assistant"))

        # Voice Settings
        voice_card = QFrame()
        voice_layout = QVBoxLayout()
        voice_card.setLayout(voice_layout)

        voice_title = QLabel("🎤 Voice Settings")
        voice_title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        slider = QSlider(Qt.Horizontal)
        slider.setValue(80)

        voice_layout.addWidget(voice_title)
        voice_layout.addWidget(QLabel("en-US-GuyNeural"))
        voice_layout.addWidget(slider)

        right_layout.addWidget(chat_card)
        right_layout.addWidget(task_card)
        right_layout.addWidget(memory_card)
        right_layout.addWidget(voice_card)

        right_layout.addStretch()

        # ==========================================
        # ADD ALL TO MAIN LAYOUT
        # ==========================================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(center_frame)
        main_layout.addWidget(right_panel)

    def update_datetime(self):
        """Update time and date display"""
        now = datetime.now()
        # Format: 11:30:45 PM
        time_str = now.strftime("%I:%M:%S %p")
        # Format: Friday, May 16, 2025
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.time_label.setText(time_str)
        self.date_label.setText(date_str)


# ==========================================
# RUN APP
# ==========================================

app = QApplication(sys.argv)

window = ZakirAI()
window.show()

sys.exit(app.exec_())