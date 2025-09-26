import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QTextEdit, QLabel, QFileSystemModel, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QModelIndex


class FileManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom File Manager")
        self.setFixedSize(800, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: Dark Slate Gray;
                color: Misty Rose;
                font-family: Consolas;
            }
            QTreeView {
                background-color: #1E1E1E;
                border: 1px solid #555;
                color: white
            }
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #555;
                padding: 8px;
                font-size: 14pt;
            }
            QLabel#pathLabel {
                padding: 5px;
                font-weight: bold;
            }
        """)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.model.setNameFilters(["*.txt", "*.py", "*.md", "*.log"])
        self.model.setNameFilterDisables(False) 

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('')) 
        self.tree.setColumnWidth(0, 250)
        self.tree.clicked.connect(self.on_tree_clicked)
        self.tree.setHeaderHidden(True)

        self.tree.setMinimumWidth(300)
        self.tree.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)


        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.path_label = QLabel("Выберите файл для просмотра")
        self.path_label.setObjectName("pathLabel")

        top_layout.addWidget(self.tree)
        top_layout.addWidget(self.text_edit)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.path_label)

        self.setLayout(main_layout)

    def on_tree_clicked(self, index: QModelIndex):
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        if self.model.isDir(index):
            self.text_edit.clear()
            self.path_label.setText(f"Папка: {file_path}")
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.path_label.setText(f"Файл: {file_path}")
            except Exception as e:
                self.text_edit.setPlainText(f"Не удалось прочитать файл:\n{e}")
                self.path_label.setText(f"Файл: {file_path} (ошибка чтения)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec_())
