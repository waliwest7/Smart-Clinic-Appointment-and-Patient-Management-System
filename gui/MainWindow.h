#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QListWidget>
#include <QLabel>
#include "../controller/ClinicDatabase.h"
#include "DashboardPanel.h"
#include "PatientPanel.h"
#include "AppointmentPanel.h"
#include "QueuePanel.h"
#include "SearchPanel.h"
#include "ReportsPanel.h"

namespace SmartClinic {
    class MainWindow : public QMainWindow {
        Q_OBJECT

    private:
        ClinicDatabase clinicDb;
        QStackedWidget* stackedWidget;
        QListWidget* navListWidget;
        QLabel* statusLabel;

        DashboardPanel* dashboardPanel;
        PatientPanel* patientPanel;
        AppointmentPanel* appointmentPanel;
        QueuePanel* queuePanel;
        SearchPanel* searchPanel;
        ReportsPanel* reportsPanel;

        void setupUI();
        void createMenus();

    public:
        MainWindow(QWidget* parent = nullptr);
        ~MainWindow() = default;

    private slots:
        void handleNavigation(int row);
        void onSaveTriggered();
        void onLoadTriggered();
        void onUndoTriggered();
    };
}

#endif // MAINWINDOW_H