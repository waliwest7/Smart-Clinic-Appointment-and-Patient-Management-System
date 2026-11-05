#ifndef APPOINTMENT_PANEL_H
#define APPOINTMENT_PANEL_H

#include <QWidget>
#include <QTableWidget>
#include "../controller/ClinicDatabase.h"
#include "../controller/AppointmentController.h"

namespace SmartClinic {
    class AppointmentPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        AppointmentController appointmentController;
        QTableWidget* tableWidget;

        void setupUI();

    public:
        explicit AppointmentPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshTable();

    private slots:
        void onScheduleClicked();
        void onCancelClicked();
        void onCompleteClicked();
    };
}

#endif // APPOINTMENT_PANEL_H