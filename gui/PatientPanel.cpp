#include "PatientPanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QMessageBox>
#include <QDialog>
#include <QFormLayout>
#include <QDialogButtonBox>
#include <QDate>
#include <QComboBox>
#include <QLabel>
#include "../model/GeneralPatient.h"
#include "../model/EmergencyPatient.h"
#include "../model/FollowUpPatient.h"
#include "../utils/IDGenerator.h"
#include "../model/ClinicException.h"

namespace SmartClinic {
    class PatientRegisterDialog : public QDialog {
    public:
        QString id;
        QString name;
        int age;
        QString contact;
        PatientCategory category;
        QString extraField1;
        QString extraField2;

        QComboBox* catCombo;
        QLineEdit* nameEdit;
        QLineEdit* ageEdit;
        QLineEdit* contactEdit;
        QLineEdit* extra1Edit;
        QLineEdit* extra2Edit;
        QLabel* extra1Label;
        QLabel* extra2Label;

        PatientRegisterDialog(QWidget* parent = nullptr) : QDialog(parent) {
            setWindowTitle("Register New Patient");
            QFormLayout* form = new QFormLayout(this);

            id = QString::fromStdString(IDGenerator::generatePatientId());
            form->addRow("Generated ID:", new QLabel(id));

            nameEdit = new QLineEdit(this);
            form->addRow("Full Name:", nameEdit);

            ageEdit = new QLineEdit(this);
            form->addRow("Age:", ageEdit);

            contactEdit = new QLineEdit(this);
            form->addRow("Contact Info:", contactEdit);

            catCombo = new QComboBox(this);
            catCombo->addItem("General");
            catCombo->addItem("Emergency");
            catCombo->addItem("Follow-Up");
            form->addRow("Category:", catCombo);

            extra1Label = new QLabel("Triage Severity:", this);
            extra1Edit = new QLineEdit(this);
            form->addRow(extra1Label, extra1Edit);

            extra2Label = new QLabel("Last Visit Date:", this);
            extra2Edit = new QLineEdit(this);
            form->addRow(extra2Label, extra2Edit);

            extra1Label->hide(); extra1Edit->hide();
            extra2Label->hide(); extra2Edit->hide();

            connect(catCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), this, [=](int idx){
                if (idx == 0) {
                    extra1Label->hide(); extra1Edit->hide();
                    extra2Label->hide(); extra2Edit->hide();
                } else if (idx == 1) {
                    extra1Label->setText("Triage Severity:");
                    extra1Label->show(); extra1Edit->show();
                    extra2Label->hide(); extra2Edit->hide();
                } else if (idx == 2) {
                    extra1Label->setText("Original Diagnosis:");
                    extra1Label->show(); extra1Edit->show();
                    extra2Label->setText("Last Visit Date:");
                    extra2Label->show(); extra2Edit->show();
                }
            });

            QDialogButtonBox* buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
            form->addRow(buttons);
            connect(buttons, &QDialogButtonBox::accepted, this, &QDialog::accept);
            connect(buttons, &QDialogButtonBox::rejected, this, &QDialog::reject);
        }

        void accept() override {
            try {
                if (nameEdit->text().trimmed().isEmpty()) throw ClinicException("Patient name cannot be empty.");
                bool ok;
                int a = ageEdit->text().toInt(&ok);
                if (!ok || a < 0 || a > 120) throw ClinicException("Age must be between 0 and 120.");

                name = nameEdit->text();
                age = a;
                contact = contactEdit->text();
                int idx = catCombo->currentIndex();
                if (idx == 0) category = PatientCategory::General;
                else if (idx == 1) { category = PatientCategory::Emergency; extraField1 = extra1Edit->text(); }
                else { category = PatientCategory::FollowUp; extraField1 = extra1Edit->text(); extraField2 = extra2Edit->text(); }

                QDialog::accept();
            } catch (const std::exception& e) {
                QMessageBox::warning(this, "Validation Error", e.what());
            }
        }
    };

    PatientPanel::PatientPanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database) {
        setupUI();
        refreshTable();
    }

    void PatientPanel::setupUI() {
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* topBar = new QHBoxLayout();
        QPushButton* regBtn = new QPushButton("Register New Patient", this);
        QPushButton* delBtn = new QPushButton("Delete Selected", this);
        searchLineEdit = new QLineEdit(this);
        searchLineEdit->setPlaceholderText("Search by Name or ID...");
        categoryFilterCombo = new QComboBox(this);
        categoryFilterCombo->addItem("All Categories");
        categoryFilterCombo->addItem("General");
        categoryFilterCombo->addItem("Emergency");
        categoryFilterCombo->addItem("Follow-Up");

        topBar->addWidget(regBtn);
        topBar->addWidget(delBtn);
        topBar->addWidget(new QLabel("Filter:"));
        topBar->addWidget(categoryFilterCombo);
        topBar->addWidget(searchLineEdit);
        layout->addLayout(topBar);

        tableWidget = new QTableWidget(this);
        tableWidget->setColumnCount(6);
        tableWidget->setHorizontalHeaderLabels({"Patient ID", "Full Name", "Age", "Contact", "Category", "Registration Date"});
        tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        layout->addWidget(tableWidget);

        connect(regBtn, &QPushButton::clicked, this, &PatientPanel::onRegisterClicked);
        connect(delBtn, &QPushButton::clicked, this, &PatientPanel::onDeleteClicked);
        connect(searchLineEdit, &QLineEdit::textChanged, this, &PatientPanel::onSearchTextChanged);
        connect(categoryFilterCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &PatientPanel::onCategoryFilterChanged);
    }

    void PatientPanel::refreshTable() {
        tableWidget->setRowCount(0);
        const auto& patients = db.getPatients();
        int filterCat = categoryFilterCombo->currentIndex();
        QString query = searchLineEdit->text().trimmed().toLower();

        for (const auto& p : patients) {
            if (filterCat == 1 && p->getCategory() != PatientCategory::General) continue;
            if (filterCat == 2 && p->getCategory() != PatientCategory::Emergency) continue;
            if (filterCat == 3 && p->getCategory() != PatientCategory::FollowUp) continue;

            if (!query.isEmpty()) {
                QString id = QString::fromStdString(p->getPatientId()).toLower();
                QString name = QString::fromStdString(p->getFullName()).toLower();
                if (!id.contains(query) && !name.contains(query)) continue;
            }

            int row = tableWidget->rowCount();
            tableWidget->insertRow(row);
            tableWidget->setItem(row, 0, new QTableWidgetItem(QString::fromStdString(p->getPatientId())));
            tableWidget->setItem(row, 1, new QTableWidgetItem(QString::fromStdString(p->getFullName())));
            tableWidget->setItem(row, 2, new QTableWidgetItem(QString::number(p->getAge())));
            tableWidget->setItem(row, 3, new QTableWidgetItem(QString::fromStdString(p->getContactInfo())));
            tableWidget->setItem(row, 4, new QTableWidgetItem(QString::fromStdString(p->getCategoryString())));
            tableWidget->setItem(row, 5, new QTableWidgetItem(QString::fromStdString(p->getRegistrationDate())));

            if (p->getCategory() == PatientCategory::Emergency) {
                for (int col = 0; col < 6; ++col) {
                    tableWidget->item(row, col)->setBackground(QColor(255, 230, 230));
                }
            }
        }
    }

    void PatientPanel::onRegisterClicked() {
        PatientRegisterDialog dlg(this);
        if (dlg.exec() == QDialog::Accepted) {
            try {
                std::string id = dlg.id.toStdString();
                std::string name = dlg.name.toStdString();
                int age = dlg.age;
                std::string contact = dlg.contact.toStdString();
                std::string regDate = QDate::currentDate().toString("yyyy-MM-dd").toStdString();

                std::shared_ptr<PatientRecord> newPat;
                if (dlg.category == PatientCategory::General) {
                    newPat = std::make_shared<GeneralPatient>(id, name, age, contact, regDate);
                } else if (dlg.category == PatientCategory::Emergency) {
                    newPat = std::make_shared<EmergencyPatient>(id, name, age, contact, regDate, dlg.extraField1.toStdString());
                } else {
                    newPat = std::make_shared<FollowUpPatient>(id, name, age, contact, regDate, dlg.extraField1.toStdString(), dlg.extraField2.toStdString());
                }

                db.addPatient(newPat);
                refreshTable();
                QMessageBox::information(this, "Success", "Patient registered successfully.");
            } catch (const std::exception& e) {
                QMessageBox::critical(this, "Error", e.what());
            }
        }
    }

    void PatientPanel::onDeleteClicked() {
        int row = tableWidget->currentRow();
        if (row < 0) {
            QMessageBox::warning(this, "Selection", "Please select a patient row to delete.");
            return;
        }
        QString id = tableWidget->item(row, 0)->text();
        if (QMessageBox::question(this, "Confirm", "Delete patient record " + id + "?") == QMessageBox::Yes) {
            db.deletePatient(id.toStdString());
            refreshTable();
            QMessageBox::information(this, "Deleted", "Patient record deleted.");
        }
    }

    void PatientPanel::onSearchTextChanged(const QString&) { refreshTable(); }
    void PatientPanel::onCategoryFilterChanged(int) { refreshTable(); }
}