#ifndef PATIENT_PANEL_H
#define PATIENT_PANEL_H

#include <QWidget>
#include <QTableWidget>
#include <QLineEdit>
#include <QComboBox>
#include <QPushButton>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class PatientPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QTableWidget* tableWidget;
        QLineEdit* searchLineEdit;
        QComboBox* categoryFilterCombo;

        void setupUI();

    public:
        explicit PatientPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshTable();

    private slots:
        void onRegisterClicked();
        void onDeleteClicked();
        void onSearchTextChanged(const QString& text);
        void onCategoryFilterChanged(int index);
    };
}

#endif // PATIENT_PANEL_H