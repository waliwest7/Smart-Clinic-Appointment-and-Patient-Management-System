#ifndef DASHBOARD_PANEL_H
#define DASHBOARD_PANEL_H

#include <QWidget>
#include <QLabel>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class DashboardPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QLabel* totalPatientsVal;
        QLabel* todayApptsVal;
        QLabel* pendingApptsVal;
        QLabel* waitingQueueVal;
        QLabel* emergencyCountVal;

        void setupUI();

    public:
        explicit DashboardPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshDashboard();
    };
}

#endif // DASHBOARD_PANEL_H