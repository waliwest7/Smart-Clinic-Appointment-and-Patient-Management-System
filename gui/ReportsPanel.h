#ifndef REPORTS_PANEL_H
#define REPORTS_PANEL_H

#include <QWidget>
#include <QTextEdit>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class ReportsPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QTextEdit* reportTextEdit;

        void setupUI();

    public:
        explicit ReportsPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void generateReports();
    };
}

#endif // REPORTS_PANEL_H