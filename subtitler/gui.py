"""Subtitler - PySide6 GUI."""

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .transcribe import load_model, transcribe_audio, translate_audio
from .romanize import create_converter, romanize_segments
from .srt import parse_srt, write_srt


class TranscribeWorker(QThread):
    """Worker thread for transcription tasks."""

    progress = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self, task_type, file_path, output_dir, model_name, with_english=False
    ):
        super().__init__()
        self.task_type = task_type
        self.file_path = file_path
        self.output_dir = output_dir
        self.model_name = model_name
        self.with_english = with_english

    def run(self):
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)

            if self.task_type == "ja":
                self._run_japanese()
            elif self.task_type == "en":
                self._run_english()
            elif self.task_type == "romaji":
                self._run_romaji()

        except Exception as e:
            self.error.emit(str(e))

    def _run_japanese(self):
        """Run Japanese transcription."""
        base_name = self.file_path.stem

        self.progress.emit(f"Loading model: {self.model_name}")
        model = load_model(self.model_name)

        self.progress.emit("Transcribing Japanese...")
        ja_segments = transcribe_audio(self.file_path, model, language="ja")
        ja_srt_path = self.output_dir / f"{base_name}_ja.srt"
        write_srt(ja_segments, ja_srt_path)
        self.progress.emit(f"-> {ja_srt_path}")

        if self.with_english:
            self.progress.emit("Translating to English...")
            en_segments = translate_audio(self.file_path, model, language="ja")
            en_srt_path = self.output_dir / f"{base_name}_en.srt"
            write_srt(en_segments, en_srt_path)
            self.progress.emit(f"-> {en_srt_path}")

        self.finished.emit("Done!")

    def _run_english(self):
        """Run English transcription."""
        base_name = self.file_path.stem

        self.progress.emit(f"Loading model: {self.model_name}")
        model = load_model(self.model_name)

        self.progress.emit("Transcribing English...")
        en_segments = transcribe_audio(self.file_path, model, language="en")
        en_srt_path = self.output_dir / f"{base_name}_en.srt"
        write_srt(en_segments, en_srt_path)
        self.progress.emit(f"-> {en_srt_path}")

        self.finished.emit("Done!")

    def _run_romaji(self):
        """Run Romaji conversion."""
        base_name = self.file_path.stem
        if base_name.endswith("_ja"):
            base_name = base_name[:-3]

        self.progress.emit("Converting to Romaji...")
        ja_segments = parse_srt(self.file_path)
        converter = create_converter()
        romaji_segments = romanize_segments(ja_segments, converter)
        romaji_srt_path = self.output_dir / f"{base_name}_romaji.srt"
        write_srt(romaji_segments, romaji_srt_path)
        self.progress.emit(f"-> {romaji_srt_path}")

        self.finished.emit("Done!")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtitler")
        self.resize(450, 300)

        self.worker = None

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)

        # Label width for alignment
        label_width = 70

        # Output directory
        output_layout = QHBoxLayout()
        output_layout.setSpacing(4)
        output_label = QLabel("Output:")
        output_label.setFixedWidth(label_width)
        output_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        output_layout.addWidget(output_label)
        self.output_edit = QLineEdit(str(Path("output").absolute()))
        output_layout.addWidget(self.output_edit)
        btn_browse = QPushButton("...")
        btn_browse.setFixedWidth(30)
        btn_browse.clicked.connect(self.browse_output)
        output_layout.addWidget(btn_browse)
        layout.addLayout(output_layout)

        # Model selector
        model_layout = QHBoxLayout()
        model_layout.setSpacing(4)
        model_label = QLabel("Model:")
        model_label.setFixedWidth(label_width)
        model_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        model_layout.addWidget(model_label)
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.model_combo.setCurrentText("base")
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        layout.addLayout(model_layout)

        # Buttons row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        convert_label = QLabel("Convert:")
        convert_label.setFixedWidth(label_width)
        convert_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        btn_layout.addWidget(convert_label)

        btn_ja = QPushButton("Japanese")
        btn_ja.clicked.connect(self.on_japanese_clicked)
        btn_layout.addWidget(btn_ja)

        btn_en = QPushButton("English")
        btn_en.clicked.connect(self.on_english_clicked)
        btn_layout.addWidget(btn_en)

        btn_romaji = QPushButton("Romaji")
        btn_romaji.clicked.connect(self.on_romaji_clicked)
        btn_layout.addWidget(btn_romaji)

        layout.addLayout(btn_layout)

        # With English checkbox (indented to align with content)
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(4)
        checkbox_spacer = QLabel("")
        checkbox_spacer.setFixedWidth(label_width)
        checkbox_layout.addWidget(checkbox_spacer)
        self.with_english_check = QCheckBox(
            "Also generate English translation (for Japanese)"
        )
        checkbox_layout.addWidget(self.with_english_check)
        checkbox_layout.addStretch()
        layout.addLayout(checkbox_layout)

        # Log output
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def browse_output(self):
        """Browse for output directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.output_edit.text()
        )
        if dir_path:
            self.output_edit.setText(dir_path)

    def get_output_dir(self):
        """Get output directory path."""
        return Path(self.output_edit.text())

    def log(self, message):
        """Add message to log."""
        self.log_text.append(message)

    def on_japanese_clicked(self):
        """Handle Japanese transcription button."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.flac);;All Files (*.*)",
        )
        if not file_path:
            return

        with_english = self.with_english_check.isChecked()
        self.run_task("ja", Path(file_path), self.get_output_dir(), with_english)

    def on_english_clicked(self):
        """Handle English transcription button."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.flac);;All Files (*.*)",
        )
        if not file_path:
            return

        self.run_task("en", Path(file_path), self.get_output_dir())

    def on_romaji_clicked(self):
        """Handle Romaji conversion button."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Japanese SRT File",
            "",
            "SRT Files (*.srt);;All Files (*.*)",
        )
        if not file_path:
            return

        self.run_task("romaji", Path(file_path), self.get_output_dir())

    def run_task(self, task_type, file_path, output_dir, with_english=False):
        """Run a transcription task in background."""
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Busy", "A task is already running.")
            return

        model_name = self.model_combo.currentText()

        self.log(f"[{task_type}] {file_path.name}")

        self.worker = TranscribeWorker(
            task_type, file_path, output_dir, model_name, with_english
        )
        self.worker.progress.connect(self.log)
        self.worker.finished.connect(self.log)
        self.worker.error.connect(self.on_task_error)
        self.worker.start()

    def on_task_error(self, message):
        """Handle task error."""
        self.log(f"Error: {message}")
        QMessageBox.critical(self, "Error", message)


def main():
    """Run the GUI application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
