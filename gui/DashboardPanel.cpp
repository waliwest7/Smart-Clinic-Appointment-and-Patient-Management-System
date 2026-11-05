#include "DashboardPanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QFrame>

namespace SmartClinic {
    DashboardPanel::DashboardPanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database) {
        setupUI();
        refreshDashboard();
    }

    QFrame* createCard(const QString& title, QLabel*& valLabel, const QString& colorHex) {
        QFrame* card = new QFrame();
        card->setStyleSheet(QString("QFrame { background-color: white; border-radius: 8px; border-left: 5px solid %1; padding: 15px; }").arg(colorHex));
        QVBoxLayout* layout = new QVBoxLayout(card);
        
        QLabel* titleLbl = new QLabel(title);
        titleLbl->setStyleSheet("color: #7f8c8d; font-size: 13px; font-weight: bold;");
        
        valLabel = new QLabel("0");
        valLabel->setStyleSheet("color: #2c3e50; font-size: 26px; font-weight: bold;");
        
        layout->addWidget(titleLbl);
        layout->addWidget(valLabel);
        return card;
    }

    void DashboardPanel::setupUI() {
        QVBoxLayout* mainLayout = new QVBoxLayout(this);
        mainLayout->setContentsMargins(20, 20, 20, 20);
        mainLayout->setSpacing(20);

        QLabel* header = new QLabel("Clinic Management Dashboard");
        header->setStyleSheet("font-size: 22px; font-weight: bold; color: #dfe7f0;");
        mainLayout->addWidget(header);

        QGridLayout* grid = new QGridLayout();
        grid->setSpacing(15);

        grid->addWidget(createCard("Total Registered Patients", totalPatientsVal, "#3498db"), 0, 0);
        grid->addWidget(createCard("Scheduled Appointments", todayApptsVal, "#2ecc71"), 0, 1);
        grid->addWidget(createCard("Pending Appointments", pendingApptsVal, "#f39c12"), 0, 2);
        grid->addWidget(createCard("Patients Waiting in Queue", waitingQueueVal, "#e74c3c"), 1, 0);
        grid->addWidget(createCard("Active Emergency Cases", emergencyCountVal, "#c0392b"), 1, 1);

        mainLayout->addLayout(grid);
        mainLayout->addStretch();
    }

    void DashboardPanel::refreshDashboard() {
        totalPatientsVal->setText(QString::number(db.getPatients().size()));

        int scheduled = 0;
        int pending = 0;
        for (const auto& a : db.getAppointments()) {
            if (a.getStatus() == AppointmentStatus::Scheduled) scheduled++;
            else if (a.getStatus() == AppointmentStatus::Pending) pending++;
        }
        todayApptsVal->setText(QString::number(scheduled));
        pendingApptsVal->setText(QString::number(pending));

        waitingQueueVal->setText(QString::number(db.getWaitingQueueCopy().size()));

        int emergencies = 0;
        for (const auto& p : db.getPatients()) {
            if (p->getCategory() == PatientCategory::Emergency) emergencies++;
        }
        emergencyCountVal->setText(QString::number(emergencies));
    }
}