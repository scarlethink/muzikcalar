from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QAction, QListWidget
from PyQt5.QtGui import QIcon, QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
import sys

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TURKFY")
        self.setWindowIcon(QIcon("muzikcalar.png"))
        self.setStyleSheet("background-color: lightblue;")  # Ana pencerenin arka plan rengi
        self.setGeometry(100, 100, 800, 600)

        self.sarkilar = []  # Şarkı yollarını tutacak liste

        # Menü çubuğu oluşturuluyor
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: pink;
                color: black;
            }
            QMenuBar::item {
                background-color: pink;
                color: black;
            }
            QMenuBar::item:selected {
                background-color: gray;
                color: white;
            }
            QMenu {
                background-color: black;
                color: white;
            }
            QMenu::item:selected {
                background-color: gray;
                color: white;
            }
        """)

        # Dosya menüsü oluşturuluyor
        dosya_menu = menubar.addMenu('Dosya')

        # Menü öğeleri oluşturuluyor
        ac_menu_item_oynatici = QAction('Oynatıcıyı aç', self)
        ac_menu_item_oynatici.triggered.connect(self.yeni_pencere_ac)
        dosya_menu.addAction(ac_menu_item_oynatici)

        ac_menu_item_sarki_ekle = QAction('Şarkı ekle', self)
        ac_menu_item_sarki_ekle.triggered.connect(self.sarki_ekle)
        dosya_menu.addAction(ac_menu_item_sarki_ekle)

        # Şarkı listesi widget'ı oluşturuluyor
        self.sarki_listesi = QListWidget()
        self.sarki_listesi.setStyleSheet("background-color: white; color: black;")  # Liste arka plan rengi beyaz, yazı rengi siyah

        # Ana layout oluşturuluyor ve widget'lar ekleniyor
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.sarki_listesi)

        # Widget oluşturuluyor ve layout'a set ediliyor
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))  # Metin rengini siyah olarak ayarla
        painter.setFont(QFont("Arial", 50))  # Metin fontu ve boyutunu ayarla
        painter.drawText(self.rect(), Qt.AlignCenter, "TURKFY")  # Metni ortala ve çiz

    def sarki_ekle(self):
        self.sarki_ekle_pencere = SarkiEkle(self)
        self.sarki_ekle_pencere.show()

    def yeni_pencere_ac(self):
        self.yeni_pencere = YeniPencere(self.sarkilar)
        self.yeni_pencere.show()

    def sarkilari_guncelle(self):
        # Şarkı listesi widget'ını günceller
        self.sarki_listesi.clear()
        self.sarki_listesi.addItems([sarki for sarki in self.sarkilar])

class SarkiEkle(QWidget):
    def __init__(self, ana_pencere):
        super().__init__()
        self.ana_pencere = ana_pencere  # Ana pencereyi referans olarak alıyoruz
        self.setWindowTitle("Şarkı Ekle")
        self.setGeometry(200, 200, 400, 300)

        # Layout ve içerik ekleniyor
        layout = QVBoxLayout()

        # Dosya seçme butonu
        self.dosya_sec_buton = QPushButton("MP3 Dosyası Seç", self)
        self.dosya_sec_buton.clicked.connect(self.dosya_sec)
        self.dosya_sec_buton.setStyleSheet("background-color: white; color: black;")  # Buton arka plan rengi beyaz, yazı rengi siyah

        # Seçilen dosya yolunu göstermek için etiket
        self.dosya_yolu_etiket = QLabel("Henüz dosya seçilmedi.", self)
        self.dosya_yolu_etiket.setStyleSheet("color: black;")  # Etiket rengi siyah

        # Layout'a buton ve etiket ekleniyor
        layout.addWidget(self.dosya_sec_buton)
        layout.addWidget(self.dosya_yolu_etiket)
        
        self.setLayout(layout)

    def dosya_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "MP3 Dosyaları (*.mp3)")
        if dosya_yolu:
            self.dosya_yolu_etiket.setText(f"Seçilen dosya: {dosya_yolu}")
            self.ana_pencere.sarkilar.append(dosya_yolu)  # Şarkı yolunu ana pencereye ekliyoruz
            self.ana_pencere.sarkilari_guncelle()  # Şarkı listesini güncelle

class YeniPencere(QWidget):
    def __init__(self, sarkilar):
        super().__init__()
        self.sarkilar = sarkilar  # Şarkı yollarını alıyoruz
        self.setWindowTitle("Oynatıcı")
        self.setWindowIcon(QIcon("muzikcalar.png"))

        # Medya player ve liste oluşturuluyor
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # Ana layout oluşturuluyor
        main_layout = QVBoxLayout()

        # Oynat butonu oluşturuluyor
        self.buton = QPushButton("OYNAT", self)
        self.buton.clicked.connect(self.oynat)
        main_layout.addWidget(self.buton)

        # Yan yana düğmeler için layout oluşturuluyor
        h_layout = QHBoxLayout()
        
        # Butonlar oluşturuluyor
        self.prev_button = QPushButton("Önceki Parça", self)
        self.prev_button.clicked.connect(self.prev_parca)
        self.stop_button = QPushButton("Durdur", self)
        self.stop_button.clicked.connect(self.durdur)
        self.next_button = QPushButton("Sonraki Parça", self)
        self.next_button.clicked.connect(self.next_parca)
        self.repeat_button = QPushButton("Tekrarla", self)
        self.repeat_button.clicked.connect(self.toggle_repeat)

        # Butonlar h_layout'a ekleniyor
        h_layout.addWidget(self.prev_button)
        h_layout.addWidget(self.stop_button)
        h_layout.addWidget(self.next_button)
        h_layout.addWidget(self.repeat_button)

        # H_layout ana layout'a ekleniyor
        main_layout.addLayout(h_layout)

        # Layout pencereye set ediliyor
        self.setLayout(main_layout)

    def oynat(self):
        if self.sarkilar:
            self.playlist.clear()
            for sarki in self.sarkilar:
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(sarki)))
            self.playlist.setCurrentIndex(0)
            self.player.play()

    def prev_parca(self):
        self.playlist.previous()

    def durdur(self):
        self.player.stop()

    def next_parca(self):
        self.playlist.next()

    def toggle_repeat(self):
        current_mode = self.playlist.playbackMode()
        if current_mode == QMediaPlaylist.Loop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

# Uygulama çalıştırılıyor
uygulama = QApplication(sys.argv)
ana_pencere = AnaPencere()
ana_pencere.show()
sys.exit(uygulama.exec_())
