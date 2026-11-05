#include "AppointmentPanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QPushButton>
#include <QMessageBox>
#include <QDialog>
#include <QFormLayout>
#include <QLineEdit>
#include <QComboBox>
#include <QDialogButtonBox>
#include <QDateEdit>
#include <QTimeEdit>
#include "../utils/IDGenerator.h"

namespace SmartClinic {
    class ScheduleAppointmentDialog : public QDialog {
    public:
        QString patientId;
        QString date;
        QString time;
        QString service;
        QString clinician;
        QString reason;

        QLineEdit* patIdEdit;
        QDateEdit* dateEdit;
        QTimeEdit* timeEdit;
        QComboBox* serviceCombo;
        QLineEdit* clinicianEdit;
        QLineEdit* reasonEdit;

        ScheduleAppointmentDialog(QWidget* parent = nullptr) : QDialog(parent) {
            setWindowTitle("Schedule Appointment");
            QFormLayout* form = new QFormLayout(this);

            patIdEdit = new QLineEdit(this);
            patIdEdit->setPlaceholderText("e.g. PAT-12345");
            form->addRow("Patient ID:", patIdEdit);

            dateEdit = new QDateEdit(QDate::currentDate(), this);
            dateEdit->setCalendarPopup(true);
            form->addRow("Date:", dateEdit);

            timeEdit = new QTimeEdit(QTime::currentTime(), this);
            form->addRow("Time:", timeEdit);

            serviceCombo = new QComboBox(this);
            serviceCombo->addItem("General Consultation");
            serviceCombo->addItem("Emergency Triage");
            serviceCombo->addItem("Follow-Up Review");
            form->addRow("Medical Service:", serviceCombo);

            clinicianEdit = new QLineEdit(this);
            form->addRow("Assigned Clinician:", clinicianEdit);

            reasonEdit = new QLineEdit(this);
            form->addRow("Reason for Visit:", reasonEdit);

            QDialogButtonBox* buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
            form->addRow(buttons);
            connect(buttons, &QDialogButtonBox::accepted, this, &QDialog::accept);
            connect(buttons, &QDialogButtonBox::rejected, this, &QDialog::reject);
        }

        void accept() override {
            if (patIdEdit->text().trimmed().isEmpty() || clinicianEdit->text().trimmed().isEmpty()) {
                QMessageBox::warning(this, "Error", "Patient ID and Clinician are required.");
                return;
            }
            patientId = patIdEdit->text().trimmed();
            date = dateEdit->date().toString("yyyy-MM-dd");
            time = timeEdit->time().toString("HH:mm");
            service = serviceCombo->currentText();
            clinician = clinicianEdit->text().trimmed();
            reason = reasonEdit->text().trimmed();
            QDialog::accept();
        }
    };

    AppointmentPanel::AppointmentPanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database), appointmentController(db) {
        setupUI();
        refreshTable();
    }

    void AppointmentPanel::setupUI() {
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* topBar = new QHBoxLayout();
        QPushButton* schedBtn = new QPushButton("Schedule Appointment", this);
        QPushButton* cancelBtn = new QPushButton("Cancel Appointment", this);
        QPushButton* compBtn = new QPushButton("Mark Completed", this);

        topBar->addWidget(schedBtn);
        topBar->addWidget(cancelBtn);
        topBar->addWidget(compBtn);
        layout->addLayout(topBar);

        tableWidget = new QTableWidget(this);
        tableWidget->setColumnCount(9);
        tableWidget->setHorizontalHeaderLabels({"Appt ID", "Patient ID", "Patient Name", "Date", "Time", "Service", "Clinician", "Reason", "Status"});
        tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        layout->addWidget(tableWidget);

        connect(schedBtn, &QPushButton::clicked, this, &AppointmentPanel::onScheduleClicked);
        connect(cancelBtn, &QPushButton::clicked, this, &AppointmentPanel::onCancelClicked);
        connect(compBtn, &QPushButton::clicked, this, &AppointmentPanel::onCompleteClicked);
    }

    void AppointmentPanel::refreshTable() {
        tableWidget->setRowCount(0);
        const auto& appts = db.getAppointments();
        for (const auto& a : appts) {
            int row = tableWidget->rowCount();
            tableWidget->insertRow(row);
            tableWidget->setItem(row, 0, new QTableWidgetItem(QString::fromStdString(a.getAppointmentId())));
            tableWidget->setItem(row, 1, new QTableWidgetItem(QString::fromStdString(a.getPatientId())));
            tableWidget->setItem(row, 2, new QTableWidgetItem(QString::fromStdString(a.getPatientName())));
            tableWidget->setItem(row, 3, new QTableWidgetItem(QString::fromStdString(a.getDate())));
            tableWidget->setItem(row, 4, new QTableWidgetItem(QString::fromStdString(a.getTime())));
            tableWidget->setItem(row, 5, new QTableWidgetItem(QString::fromStdString(a.getService())));
            tableWidget->setItem(row, 6, new QTableWidgetItem(QString::fromStdString(a.getClinician())));
            tableWidget->setItem(row, 7, new QTableWidgetItem(QString::fromStdString(a.getReason())));
            tableWidget->setItem(row, 8, new QTableWidgetItem(QString::fromStdString(a.getStatusString())));
        }
    }

    void AppointmentPanel::onScheduleClicked() {
        ScheduleAppointmentDialog dlg(this);
        if (dlg.exec() == QDialog::Accepted) {
            try {
                std::string appId = IDGenerator::generateAppointmentId();
                appointmentController.bookAppointment(
                    appId,
                    dlg.patientId.toStdString(),
                    dlg.date.toStdString(),
                    dlg.time.toStdString(),
                    dlg.service.toStdString(),
                    dlg.clinician.toStdString(),
                    dlg.reason.toStdString()
                );
                refreshTable();
                QMessageBox::information(this, "Success", "Appointment scheduled successfully.");
            } catch (const std::exception& e) {
                QMessageBox::critical(this, "Booking Error", e.what());
            }
        }
    }

    void AppointmentPanel::onCancelClicked() {
        int row = tableWidget->currentRow();
        if (row < 0) {
            QMessageBox::warning(this, "Selection", "Please select an appointment row.");
            return;
        }
        QString appId = tableWidget->item(row, 0)->text();
        if (QMessageBox::question(this, "Confirm", "Cancel appointment " + appId + "?") == QMessageBox::Yes) {
            try {
                db.cancelAppointment(appId.toStdString());
                refreshTable();
            } catch (const std::exception& e) {
                QMessageBox::warning(this, "Error", e.what());
            }
        }
    }

    void AppointmentPanel::onCompleteClicked() {
        int row = tableWidget->currentRow();
        if (row < 0) {
            QMessageBox::warning(this, "Selection", "Please select an appointment row.");
            return;
        }
        QString appId = tableWidget->item(row, 0)->text();
        try {
            db.completeAppointment(appId.toStdString());
            refreshTable();
            QMessageBox::information(this, "Updated", "Appointment marked as completed.");
        } catch (const std::exception& e) {
            QMessageBox::warning(this, "Error", e.what());
        }
    }
}