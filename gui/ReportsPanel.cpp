#include "ReportsPanel.h"
#include <QVBoxLayout>
#include <QPushButton>
#include <QTextStream>
#include <algorithm>

namespace SmartClinic {
    ReportsPanel::ReportsPanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database) {
        setupUI();
        generateReports();
    }

    void ReportsPanel::setupUI() {
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* topBar = new QHBoxLayout();
        QPushButton* refreshBtn = new QPushButton("Refresh Reports", this);
        topBar->addWidget(refreshBtn);
        layout->addLayout(topBar);

        reportTextEdit = new QTextEdit(this);
        reportTextEdit->setReadOnly(true);
        reportTextEdit->setStyleSheet("font-family: Consolas, monospace; font-size: 13px; background-color: #000000;");
        layout->addWidget(reportTextEdit);

        connect(refreshBtn, &QPushButton::clicked, this, &ReportsPanel::generateReports);
    }

    void ReportsPanel::generateReports() {
        QString report;
        QTextStream out(&report);

        out << "===================================================\n";
        out << "          UNIVERSITY CLINIC MANAGEMENT SYSTEM      \n";
        out << "                   OFFICIAL REPORTS                \n";
        out << "===================================================\n\n";

        out << "1. MOST FREQUENTLY ATTENDED PATIENTS (Ranked)\n";
        out << "---------------------------------------------------\n";
        auto patList = db.getPatients();
        std::sort(patList.begin(), patList.end(), [](const auto& a, const auto& b) {
            return a->getAppointmentCount() > b->getAppointmentCount();
        });
        int rank = 1;
        for (const auto& p : patList) {
            out << rank++ << ". " << QString::fromStdString(p->getFullName()) 
                << " (ID: " << QString::fromStdString(p->getPatientId()) << ") - " 
                << p->getAppointmentCount() << " appointments\n";
        }
        out << "\n";

        out << "2. PATIENTS WITH PENDING / SCHEDULED APPOINTMENTS\n";
        out << "---------------------------------------------------\n";
        for (const auto& a : db.getAppointments()) {
            if (a.getStatus() == AppointmentStatus::Scheduled || a.getStatus() == AppointmentStatus::Pending) {
                out << "- Appt ID: " << QString::fromStdString(a.getAppointmentId()) 
                    << " | Patient: " << QString::fromStdString(a.getPatientName()) 
                    << " | Date: " << QString::fromStdString(a.getDate()) 
                    << " @ " << QString::fromStdString(a.getTime()) << "\n";
            }
        }
        out << "\n";

        out << "3. PATIENT CATEGORY DISTRIBUTION\n";
        out << "---------------------------------------------------\n";
        int genCount = 0, emgCount = 0, folCount = 0;
        for (const auto& p : patList) {
            if (p->getCategory() == PatientCategory::General) genCount++;
            else if (p->getCategory() == PatientCategory::Emergency) emgCount++;
            else if (p->getCategory() == PatientCategory::FollowUp) folCount++;
        }
        out << "- General Patients:   " << genCount << "\n";
        out << "- Emergency Patients: " << emgCount << "\n";
        out << "- Follow-Up Patients: " << folCount << "\n";
        out << "- Total Registered:   " << patList.size() << "\n\n";

        out << "4. DAILY APPOINTMENT SUMMARY\n";
        out << "---------------------------------------------------\n";
        int totalAppts = db.getAppointments().size();
        int completed = 0, pending = 0, scheduled = 0, cancelled = 0;
        for (const auto& a : db.getAppointments()) {
            if (a.getStatus() == AppointmentStatus::Completed) completed++;
            else if (a.getStatus() == AppointmentStatus::Pending) pending++;
            else if (a.getStatus() == AppointmentStatus::Scheduled) scheduled++;
            else if (a.getStatus() == AppointmentStatus::Cancelled) cancelled++;
        }
        out << "- Total Appointments: " << totalAppts << "\n";
        out << "- Scheduled:          " << scheduled << "\n";
        out << "- Pending:            " << pending << "\n";
        out << "- Completed:          " << completed << "\n";
        out << "- Cancelled:          " << cancelled << "\n";
        out << "===================================================\n";

        reportTextEdit->setPlainText(report);
    }
}