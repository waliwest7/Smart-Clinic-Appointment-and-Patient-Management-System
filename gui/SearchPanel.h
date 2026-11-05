#ifndef SEARCH_PANEL_H
#define SEARCH_PANEL_H

#include <QWidget>
#include <QTableWidget>
#include <QLineEdit>
#include <QComboBox>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class SearchPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QTableWidget* tableWidget;
        QLineEdit* searchInputEdit;
        QComboBox* methodCombo;
        QComboBox* sortAlgoCombo;
        QComboBox* sortFieldCombo;

        void setupUI();

    public:
        explicit SearchPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void displayResults(const std::vector<std::shared_ptr<PatientRecord>>& results);

    private slots:
        void onSearchClicked();
        void onSortClicked();
    };
}

#endif // SEARCH_PANEL_H