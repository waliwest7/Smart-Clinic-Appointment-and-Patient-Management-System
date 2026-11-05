#include "MainWindow.h"
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QMenuBar>
#include <QStatusBar>
#include <QMessageBox>
#include <QFileDialog>
#include "../utils/FileHandler.h"

namespace SmartClinic {
    MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
        setWindowTitle("Smart Clinic Appointment & Patient Management System");
        setupUI();
        createMenus();
    }

    void MainWindow::setupUI() {
        QWidget* centralWidget = new QWidget(this);
        QHBoxLayout* mainLayout = new QHBoxLayout(centralWidget);
        mainLayout->setContentsMargins(0, 0, 0, 0);

        navListWidget = new QListWidget(this);
        navListWidget->addItem("Dashboard");
        navListWidget->addItem("Patient Records");
        navListWidget->addItem("Appointments");
        navListWidget->addItem("Waiting Queue");
        navListWidget->addItem("Search & Sort");
        navListWidget->addItem("Reports");
        navListWidget->setFixedWidth(220);
        navListWidget->setStyleSheet("QListWidget { background-color: #2c3e50; color: white; font-size: 14px; border: none; padding: 10px; }"
                                   "QListWidget::item { padding: 12px; border-radius: 6px; margin-bottom: 4px; }"
                                   "QListWidget::item:selected { background-color: #3498db; color: white; }");

        stackedWidget = new QStackedWidget(this);

        dashboardPanel = new DashboardPanel(clinicDb, this);
        patientPanel = new PatientPanel(clinicDb, this);
        appointmentPanel = new AppointmentPanel(clinicDb, this);
        queuePanel = new QueuePanel(clinicDb, this);
        searchPanel = new SearchPanel(clinicDb, this);
        reportsPanel = new ReportsPanel(clinicDb, this);

        stackedWidget->addWidget(dashboardPanel);   // Index 0
        stackedWidget->addWidget(patientPanel);     // Index 1
        stackedWidget->addWidget(appointmentPanel); // Index 2
        stackedWidget->addWidget(queuePanel);       // Index 3
        stackedWidget->addWidget(searchPanel);      // Index 4
        stackedWidget->addWidget(reportsPanel);     // Index 5

        mainLayout->addWidget(navListWidget);
        mainLayout->addWidget(stackedWidget);
        setCentralWidget(centralWidget);

        statusLabel = new QLabel("Ready", this);
        statusBar()->addPermanentWidget(statusLabel);

        connect(navListWidget, &QListWidget::currentRowChanged, this, &MainWindow::handleNavigation);
        navListWidget->setCurrentRow(0);
    }

    void MainWindow::createMenus() {
        QMenu* fileMenu = menuBar()->addMenu("&File");
        
        QAction* saveAction = fileMenu->addAction("&Save Data");
        saveAction->setShortcut(QKeySequence::Save);
        connect(saveAction, &QAction::triggered, this, &MainWindow::onSaveTriggered);

        QAction* loadAction = fileMenu->addAction("&Load Data");
        loadAction->setShortcut(QKeySequence::Open);
        connect(loadAction, &QAction::triggered, this, &MainWindow::onLoadTriggered);

        fileMenu->addSeparator();
        QAction* exitAction = fileMenu->addAction("E&xit");
        exitAction->setShortcut(QKeySequence::Quit);
        connect(exitAction, &QAction::triggered, this, &QWidget::close);

        QMenu* editMenu = menuBar()->addMenu("&Edit");
        QAction* undoAction = editMenu->addAction("&Undo Last Operation");
        undoAction->setShortcut(QKeySequence::Undo);
        connect(undoAction, &QAction::triggered, this, &MainWindow::onUndoTriggered);
    }

    void MainWindow::handleNavigation(int row) {
        stackedWidget->setCurrentIndex(row);
        if (row == 0) dashboardPanel->refreshDashboard();
        else if (row == 2) appointmentPanel->refreshTable();
        else if (row == 3) queuePanel->refreshTable();
        else if (row == 5) reportsPanel->generateReports();

        statusLabel->setText("Switched workspace section: " + navListWidget->item(row)->text());
    }

    void MainWindow::onSaveTriggered() {
        QString fileName = QFileDialog::getSaveFileName(this, "Save Clinic Data", "", "Clinic Data Files (*.dat);;All Files (*)");
        if (fileName.isEmpty()) return;

        bool success = FileHandler::saveData(fileName.toStdString(), clinicDb.getPatients(), clinicDb.getAppointments());
        if (success) {
            statusLabel->setText("Data successfully saved to " + fileName);
            QMessageBox::information(this, "Success", "Clinic records saved successfully.");
        } else {
            QMessageBox::critical(this, "Error", "Failed to save data to file.");
        }
    }

    void MainWindow::onLoadTriggered() {
        QString fileName = QFileDialog::getOpenFileName(this, "Load Clinic Data", "", "Clinic Data Files (*.dat);;All Files (*)");
        if (fileName.isEmpty()) return;

        std::vector<std::shared_ptr<PatientRecord>> loadedPatients;
        std::vector<Appointment> loadedAppointments;

        bool success = FileHandler::loadData(fileName.toStdString(), loadedPatients, loadedAppointments);
        if (success) {
            clinicDb.clearAllData();
            for (auto& p : loadedPatients) {
                clinicDb.addPatient(p, false);
            }
            for (auto& a : loadedAppointments) {
                clinicDb.addAppointment(a, false);
            }
            dashboardPanel->refreshDashboard();
            patientPanel->refreshTable();
            appointmentPanel->refreshTable();
            queuePanel->refreshTable();
            reportsPanel->generateReports();

            statusLabel->setText("Data successfully loaded from " + fileName);
            QMessageBox::information(this, "Success", "Clinic records loaded successfully.");
        } else {
            QMessageBox::critical(this, "Error", "Failed to load data or file validation failed.");
        }
    }

    void MainWindow::onUndoTriggered() {
        if (!clinicDb.getUndoManager().canUndo()) {
            QMessageBox::information(this, "Undo", "No operations available to undo.");
            return;
        }
        std::string desc = clinicDb.getUndoManager().popAndExecute();
        dashboardPanel->refreshDashboard();
        patientPanel->refreshTable();
        appointmentPanel->refreshTable();
        queuePanel->refreshTable();
        reportsPanel->generateReports();

        statusLabel->setText(QString::fromStdString("Undid operation: " + desc));
        QMessageBox::information(this, "Undo Successful", QString::fromStdString("Successfully reversed: " + desc));
    }
}