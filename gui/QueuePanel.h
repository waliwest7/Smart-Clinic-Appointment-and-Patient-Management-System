#ifndef QUEUE_PANEL_H
#define QUEUE_PANEL_H

#include <QWidget>
#include <QTableWidget>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class QueuePanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QTableWidget* tableWidget;

        void setupUI();

    public:
        explicit QueuePanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshTable();

    private slots:
        void onEnqueueClicked();
        void onCallNextClicked();
        void onClearQueueClicked();
    };
}

#endif // QUEUE_PANEL_H