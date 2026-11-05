#include "QueuePanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QPushButton>
#include <QMessageBox>
#include <QInputDialog>

namespace SmartClinic {
    QueuePanel::QueuePanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database) {
        setupUI();
        refreshTable();
    }

    void QueuePanel::setupUI() {
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* topBar = new QHBoxLayout();
        QPushButton* enqBtn = new QPushButton("Add Patient to Queue", this);
        QPushButton* callBtn = new QPushButton("Call Next Patient", this);
        QPushButton* clearBtn = new QPushButton("Clear Queue", this);

        topBar->addWidget(enqBtn);
        topBar->addWidget(callBtn);
        topBar->addWidget(clearBtn);
        layout->addLayout(topBar);

        tableWidget = new QTableWidget(this);
        tableWidget->setColumnCount(5);
        tableWidget->setHorizontalHeaderLabels({"Queue Position", "Patient ID", "Full Name", "Category", "Special Instructions"});
        tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        layout->addWidget(tableWidget);

        connect(enqBtn, &QPushButton::clicked, this, &QueuePanel::onEnqueueClicked);
        connect(callBtn, &QPushButton::clicked, this, &QueuePanel::onCallNextClicked);
        connect(clearBtn, &QPushButton::clicked, this, &QueuePanel::onClearQueueClicked);
    }

    void QueuePanel::refreshTable() {
        tableWidget->setRowCount(0);
        auto qCopy = db.getWaitingQueueCopy();
        int pos = 1;
        while (!qCopy.empty()) {
            auto p = qCopy.front();
            qCopy.pop();

            int row = tableWidget->rowCount();
            tableWidget->insertRow(row);
            tableWidget->setItem(row, 0, new QTableWidgetItem(QString::number(pos++)));
            tableWidget->setItem(row, 1, new QTableWidgetItem(QString::fromStdString(p->getPatientId())));
            tableWidget->setItem(row, 2, new QTableWidgetItem(QString::fromStdString(p->getFullName())));
            tableWidget->setItem(row, 3, new QTableWidgetItem(QString::fromStdString(p->getCategoryString())));
            tableWidget->setItem(row, 4, new QTableWidgetItem(QString::fromStdString(p->getSpecialInstructions())));

            if (p->getCategory() == PatientCategory::Emergency) {
                for (int col = 0; col < 5; ++col) {
                    tableWidget->item(row, col)->setBackground(QColor(255, 220, 220));
                }
            }
        }
    }

    void QueuePanel::onEnqueueClicked() {
        bool ok;
        QString patId = QInputDialog::getText(this, "Add to Queue", "Enter Patient ID:", QLineEdit::Normal, "", &ok);
        if (!ok || patId.trimmed().isEmpty()) return;

        auto pat = db.findPatient(patId.toStdString());
        if (!pat) {
            QMessageBox::warning(this, "Not Found", "Patient ID not found in records.");
            return;
        }

        if (db.isPatientInQueue(patId.toStdString())) {
            QMessageBox::warning(this, "Duplicate", "Patient is already in the active waiting queue.");
            return;
        }

        db.enqueuePatient(pat);
        refreshTable();
        QMessageBox::information(this, "Enqueued", QString::fromStdString(pat->getFullName() + " added to waiting queue."));
    }

    void QueuePanel::onCallNextClicked() {
        auto pat = db.dequeuePatient();
        if (!pat) {
            QMessageBox::information(this, "Queue Empty", "No patients currently waiting in queue.");
            return;
        }
        refreshTable();
        QMessageBox::information(this, "Calling Patient", QString::fromStdString("Calling next patient for consultation:\n\nName: " + pat->getFullName() + "\nInstructions: " + pat->getSpecialInstructions()));
    }

    void QueuePanel::onClearQueueClicked() {
        if (QMessageBox::question(this, "Confirm", "Clear the entire waiting queue?") == QMessageBox::Yes) {
            db.clearQueue();
            refreshTable();
        }
    }
}