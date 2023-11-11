from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QVBoxLayout, QScrollArea, QTableWidget, QPushButton, \
    QTableWidgetItem, QToolBar, QAction, QMessageBox
from cliente import Cliente

class Ventana3(QMainWindow):
    def __init__(self, anterior):
        super(Ventana3, self).__init__(anterior)

        self.ventanaAnterior = anterior

        self.setWindowTitle("formulario de registro")

        self.setWindowIcon(QtGui.QIcon("Imagenes/icono.jpg"))

        self.ancho = 1000
        self.alto = 600

        self.resize(self.ancho, self.alto)

        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)

        self.fondo = QLabel(self)
        self.imagenFondo = QPixmap('Imagenes/fondo3.jpg')
        self.fondo.setPixmap(self.imagenFondo)
        self.fondo.setScaledContents(True)
        self.resize(self.imagenFondo.width(), self.imagenFondo.height())
        self.setCentralWidget(self.fondo)

        self.file = open("datos/cliente.txt", 'rb')

        usuarios = []

        while self.file:
            linea = self.file.readline().decode('UTF-8')
            lista = linea.split(";")
            if linea == '':
                break
            u = Cliente(
                lista[0],
                lista[1],
                lista[2],
                lista[3],
                lista[4],
                lista[5],
                lista[6],
                lista[7],
                lista[8],
                lista[9],
                lista[10],
            )
            usuarios.append(u)
        self.file.close()

        self.numeroUsuarios = len(usuarios)
        self.contador = 0

        self.vertical = QVBoxLayout()

        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.setIconSize(QSize(35, 35))
        self.addToolBar(self.toolbar)

        self.delete = QAction(QIcon("Imagenes/delete.png"), '&Delete', self)
        self.delete.triggered.connect(self.accion_delete)
        self.toolbar.addAction(self.delete)

        self.add = QAction(QIcon("Imagenes/agregar.png"), '&Add', self)
        self.add.triggered.connect(self.accion_add)
        self.toolbar.addAction(self.add)

        self.insert = QAction(QIcon("Imagenes/editar.png"), '&Insert', self)
        self.insert.triggered.connect(self.accion_insert)
        self.toolbar.addAction(self.insert)

        self.letrero1 = QLabel()
        self.letrero1.setText("Usuarios Registrados")
        self.letrero1.setFont(QFont("Arial", 12))
        self.letrero1.setStyleSheet("color: white;")

        self.vertical.addWidget(self.letrero1)
        self.vertical.addStretch()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)

        self.tabla.setColumnWidth(0, 150)
        self.tabla.setColumnWidth(1, 150)
        self.tabla.setColumnWidth(2, 150)
        self.tabla.setColumnWidth(3, 150)
        self.tabla.setColumnWidth(4, 150)
        self.tabla.setColumnWidth(5, 150)
        self.tabla.setColumnWidth(6, 150)
        self.tabla.setColumnWidth(7, 150)
        self.tabla.setColumnWidth(8, 150)
        self.tabla.setColumnWidth(9, 150)
        self.tabla.setColumnWidth(10, 150)

        self.tabla.setHorizontalHeaderLabels(["Nombre",
                                             "Usuario",
                                             "Password",
                                             "Documento",
                                             "Correo",
                                             "Pregunta1",
                                             "Respuesta1",
                                             "Pregunta2",
                                             "Respuesta2",
                                             "Pregunta3",
                                             "Respuesta3"])
        self.tabla.setRowCount(self.numeroUsuarios)

        for u in usuarios:
            self.tabla.setItem(self.contador, 0, QTableWidgetItem(u.nombreCompleto))
            self.tabla.item(self.contador, 0).setFlags(Qt.ItemIsEnabled)
            self.tabla.setItem(self.contador, 1, QTableWidgetItem(u.usuario))
            self.tabla.setItem(self.contador, 2, QTableWidgetItem(u.password))
            self.tabla.setItem(self.contador, 3, QTableWidgetItem(u.documento))
            self.tabla.item(self.contador, 3).setFlags(Qt.ItemIsEnabled)
            self.tabla.setItem(self.contador, 4, QTableWidgetItem(u.correo))
            self.tabla.setItem(self.contador, 5, QTableWidgetItem(u.pregunta1))
            self.tabla.setItem(self.contador, 6, QTableWidgetItem(u.respuesta1))
            self.tabla.setItem(self.contador, 7, QTableWidgetItem(u.pregunta2))
            self.tabla.setItem(self.contador, 8, QTableWidgetItem(u.respuesta2))
            self.tabla.setItem(self.contador, 9, QTableWidgetItem(u.pregunta3))
            self.tabla.setItem(self.contador, 10, QTableWidgetItem(u.respuesta3))
            self.contador += 1

        self.scrollArea.setWidget(self.tabla)

        self.vertical.addWidget(self.scrollArea)
        self.vertical.addStretch()

        self.botonVolver = QPushButton("Volver")
        self.botonVolver.setFixedWidth(90)
        self.botonVolver.setStyleSheet("background-color: red;"
                                       "color: white;"
                                       "padding: 10px;"
                                       "margin-top: 10px;")
        self.botonVolver.clicked.connect(self.metodo_botonVolver)

        self.vertical.addWidget(self.botonVolver)

        self.fondo.setLayout(self.vertical)

    def metodo_botonVolver(self):
        self.hide()
        self.ventanaAnterior.show()

    def accion_delete(self):
        filaActual = self.tabla.currentRow()
        if filaActual < 0:
            return QMessageBox.warning(self,'Warning','Para borrar, debe seleccionar un registro')

        boton = QMessageBox.question(
            self,
            'Confirmation',
            '¿Está segur@ de que quieres borrar este registro?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if boton == QMessageBox.StandardButton.Yes:
            if(
                self.tabla.item(filaActual, 0).text() != '' and
                self.tabla.item(filaActual, 1).text() != '' and
                self.tabla.item(filaActual, 2).text() != '' and
                self.tabla.item(filaActual, 3).text() != '' and
                self.tabla.item(filaActual, 4).text() != '' and
                self.tabla.item(filaActual, 5).text() != '' and
                self.tabla.item(filaActual, 6).text() != '' and
                self.tabla.item(filaActual, 7).text() != '' and
                self.tabla.item(filaActual, 8).text() != '' and
                self.tabla.item(filaActual, 9).text() != '' and
                self.tabla.item(filaActual, 10).text() != ''
            ):
                self.file = open('datos/cliente.txt', 'rb')

                usuarios = []

                while self.file:
                    linea = self.file.readline().decode('UTF-8')
                    lista = linea.split(";")
                    if linea == '':
                        break
                    u = Cliente(
                        lista[0],
                        lista[1],
                        lista[2],
                        lista[3],
                        lista[4],
                        lista[5],
                        lista[6],
                        lista[7],
                        lista[8],
                        lista[9],
                        lista[10],
                    )
                    usuarios.append(u)
                self.file.close()

                for u in usuarios:
                    if (
                        u.documento == self.tabla.item(filaActual, 3).text()
                    ):
                        existeRegistro = True
                        usuarios.remove(u)
                        break

                self.file = open('datos/cliente.txt', 'wb')

                for u in usuarios:
                    self.file.write(bytes(u.nombreCompleto + ";"
                                          + u.usuario + ";"
                                          + u.password + ";"
                                          + u.documento + ";"
                                          + u.correo + ";"
                                          + u.pregunta1 + ";"
                                          + u.respuesta1 + ";"
                                          + u.pregunta2 + ";"
                                          + u.respuesta2 + ";"
                                          + u.pregunta3 + ";"
                                          + u.respuesta3, encoding='UTF-8'))
                self.file.close()
                self.tabla.removeRow(filaActual)

                return QMessageBox.question(
                    self,
                    'Confirmation',
                    'El registro ha sido eliminado exitosamente.',
                    QMessageBox.StandardButton.Yes
                )
            else:
                self.tabla.removeRow(filaActual)

    def accion_add(self):
        ultimaFila = self.tabla.rowCount()
        self.tabla.insertRow(ultimaFila)

        self.tabla.setItem(ultimaFila, 0, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 1, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 2, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 3, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 4, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 5, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 6, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 7, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 8, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 9, QTableWidgetItem(""))
        self.tabla.setItem(ultimaFila, 10, QTableWidgetItem(""))

    def accion_insert(self):
        filaActual = self.tabla.currentRow()

        if filaActual < 0:
            return QMessageBox.warning(self, 'Warning', 'Para ingresar, debe seleccionar un registro')

        boton = QMessageBox.question(
            self,
            'Confirmation',
            '¿Estas segur@ de que quieres ingresar a este nuevo registro?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        datosVacios = True

        if boton == QMessageBox.StandardButton.Yes:
            if(
            self.tabla.item(filaActual, 0).text() != '' and
            self.tabla.item(filaActual, 1).text() != '' and
            self.tabla.item(filaActual, 2).text() != '' and
            self.tabla.item(filaActual, 3).text() != '' and
            self.tabla.item(filaActual, 4).text() != '' and
            self.tabla.item(filaActual, 5).text() != '' and
            self.tabla.item(filaActual, 6).text() != '' and
            self.tabla.item(filaActual, 7).text() != '' and
            self.tabla.item(filaActual, 8).text() != '' and
            self.tabla.item(filaActual, 9).text() != '' and
            self.tabla.item(filaActual, 10).text() != ''
            ):
                datosVacios = False

                self.file = open('datos/cliente.txt', 'rb')

                usuarios = []

                while self.file:
                    linea = self.file.readline().decode('UTF-8')
                    lista = linea.split(";")
                    if linea == '':
                        break
                    u = Cliente(
                        lista[0],
                        lista[1],
                        lista[2],
                        lista[3],
                        lista[4],
                        lista[5],
                        lista[6],
                        lista[7],
                        lista[8],
                        lista[9],
                        lista[10],
                    )
                    usuarios.append(u)
                self.file.close()

                existeRegistro = False
                existeDocumento = False

                for u in usuarios:
                    if (
                        u.nombreCompleto == self.tabla.item(filaActual, 0).text() and
                        u.usuario == self.tabla.item(filaActual, 1).text() and
                        u.password == self.tabla.item(filaActual, 2).text() and
                        u.documento == self.tabla.item(filaActual, 3).text() and
                        u.correo == self.tabla.item(filaActual, 4).text() and
                        u.pregunta1 == self.tabla.item(filaActual, 5).text() and
                        u.respuesta1 == self.tabla.item(filaActual, 6).text() and
                        u.pregunta2 == self.tabla.item(filaActual, 7).text() and
                        u.respuesta2 == self.tabla.item(filaActual, 8).text() and
                        u.pregunta3 == self.tabla.item(filaActual, 9).text() and
                        u.respuesta3 == self.tabla.item(filaActual, 10).text()
                    ):
                        existeRegistro = True

                        return QMessageBox.warning(self, 'Warning', 'Registro duplicado, no se puede registrar')
                        break

                if not existeRegistro:
                    for u in usuarios:
                        if (
                                u.documento == self.tabla.item(filaActual, 3). text()
                        ):
                            existeDocumento = True

                            u.nombreCompleto = self.tabla.item(filaActual, 0).text()
                            u.usuario = self.tabla.item(filaActual, 1).text()
                            u.password = self.tabla.item(filaActual, 2).text()
                            u.documento = self.tabla.item(filaActual, 3).text()
                            u.correo = self.tabla.item(filaActual, 4).text()
                            u.pregunta1 = self.tabla.item(filaActual, 5).text()
                            u.respuesta1 = self.tabla.item(filaActual, 6).text()
                            u.pregunta2 = self.tabla.item(filaActual, 7).text()
                            u.respuesta2 = self.tabla.item(filaActual, 8).text()
                            u.pregunta3 = self.tabla.item(filaActual, 9).text()
                            u.respuesta3 = self.tabla.item(filaActual, 10).text()

                            self.file = open('datos/cliente.txt', 'wb')
                            for u in usuarios:
                                self.file.write(bytes(u.nombreCompleto + ";"
                                                      + u.usuario + ";"
                                                      + u.password + ";"
                                                      + u.documento + ";"
                                                      + u.correo + ";"
                                                      + u.pregunta1 + ";"
                                                      + u.respuesta1 + ";"
                                                      + u.pregunta2 + ";"
                                                      + u.respuesta2 + ";"
                                                      + u.pregunta3 + ";"
                                                      + u.respuesta3, encoding='UTF-8'))
                            self.file.close()

                            return QMessageBox.question(
                                self,
                                'Confirmation',
                                'Los datos del registro se han editado exitosamente.',
                                QMessageBox.StandardButton.Ok
                            )

                            break

                    if not existeDocumento:
                        self.file = open('datos/cliente.txt', 'ab')

                        self.file.write(bytes(self.tabla.item(filaActual, 0).text() + ";"
                                              + self.tabla.item(filaActual, 1).text() + ";"
                                              + self.tabla.item(filaActual, 2).text() + ";"
                                              + self.tabla.item(filaActual, 3).text() + ";"
                                              + self.tabla.item(filaActual, 4).text() + ";"
                                              + self.tabla.item(filaActual, 5).text() + ";"
                                              + self.tabla.item(filaActual, 6).text() + ";"
                                              + self.tabla.item(filaActual, 7).text() + ";"
                                              + self.tabla.item(filaActual, 8).text() + ";"
                                              + self.tabla.item(filaActual, 9).text() + ";"
                                              + self.tabla.item(filaActual, 10).text() + "\n", encoding='UTF-8'))

                        self.file.seek(0, 2)
                        self.file.close()

                    return QMessageBox.question(
                        self,
                        'Confirmation',
                        'Los datos del registro se han ingresado exitosamente',
                        QMessageBox.StandardButton.Ok
                    )
            if datosVacios:
                return QMessageBox.warning(self, 'Warning', 'Debe ingresar todos los datos en el registro')

