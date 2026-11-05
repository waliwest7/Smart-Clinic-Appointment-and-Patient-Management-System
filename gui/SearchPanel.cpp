#include "SearchPanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QPushButton>
#include <QLabel>
#include <QMessageBox>
#include "../controller/SearchEngine.h"

namespace SmartClinic {
    SearchPanel::SearchPanel(ClinicDatabase& database, QWidget* parent) : QWidget(parent), db(database) {
        setupUI();
    }

    void SearchPanel::setupUI() {
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* searchLayout = new QHBoxLayout();
        methodCombo = new QComboBox(this);
        methodCombo->addItem("Linear Search (by ID)");
        methodCombo->addItem("Binary Search (by ID)");
        methodCombo->addItem("Recursive Search (by Name)");
        searchInputEdit = new QLineEdit(this);
        searchInputEdit->setPlaceholderText("Enter search query (ID or Name)...");
        QPushButton* searchBtn = new QPushButton("Execute Search", this);

        searchLayout->addWidget(new QLabel("Method:"));
        searchLayout->addWidget(methodCombo);
        searchLayout->addWidget(searchInputEdit);
        searchLayout->addWidget(searchBtn);
        layout->addLayout(searchLayout);

        QHBoxLayout* sortLayout = new QHBoxLayout();
        sortAlgoCombo = new QComboBox(this);
        sortAlgoCombo->addItem("Selection Sort");
        sortAlgoCombo->addItem("Merge Sort");
        sortFieldCombo = new QComboBox(this);
        sortFieldCombo->addItem("Sort by Name");
        sortFieldCombo->addItem("Sort by ID");
        sortFieldCombo->addItem("Sort by Age");
        QPushButton* sortBtn = new QPushButton("Execute Sort", this);

        sortLayout->addWidget(new QLabel("Algorithm:"));
        sortLayout->addWidget(sortAlgoCombo);
        sortLayout->addWidget(sortFieldCombo);
        sortLayout->addWidget(sortBtn);
        layout->addLayout(sortLayout);

        tableWidget = new QTableWidget(this);
        tableWidget->setColumnCount(6);
        tableWidget->setHorizontalHeaderLabels({"Patient ID", "Full Name", "Age", "Contact", "Category", "Registration Date"});
        tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        layout->addWidget(tableWidget);

        connect(searchBtn, &QPushButton::clicked, this, &SearchPanel::onSearchClicked);
        connect(sortBtn, &QPushButton::clicked, this, &SearchPanel::onSortClicked);
    }

    void SearchPanel::displayResults(const std::vector<std::shared_ptr<PatientRecord>>& results) {
        tableWidget->setRowCount(0);
        for (const auto& p : results) {
            int row = tableWidget->rowCount();
            tableWidget->insertRow(row);
            tableWidget->setItem(row, 0, new QTableWidgetItem(QString::fromStdString(p->getPatientId())));
            tableWidget->setItem(row, 1, new QTableWidgetItem(QString::fromStdString(p->getFullName())));
            tableWidget->setItem(row, 2, new QTableWidgetItem(QString::number(p->getAge())));
            tableWidget->setItem(row, 3, new QTableWidgetItem(QString::fromStdString(p->getContactInfo())));
            tableWidget->setItem(row, 4, new QTableWidgetItem(QString::fromStdString(p->getCategoryString())));
            tableWidget->setItem(row, 5, new QTableWidgetItem(QString::fromStdString(p->getRegistrationDate())));
        }
    }

    void SearchPanel::onSearchClicked() {
        QString query = searchInputEdit->text().trimmed();
        if (query.isEmpty()) {
            QMessageBox::warning(this, "Input", "Please enter a search query.");
            return;
        }

        int method = methodCombo->currentIndex();
        std::vector<std::shared_ptr<PatientRecord>> results;

        if (method == 0) {
            auto p = SearchEngine::linearSearchById(db.getPatients(), query.toStdString());
            if (p) results.push_back(p);
        } else if (method == 1) {
            auto sortedList = db.getPatients();
            SearchEngine::mergeSort(sortedList, 0, static_cast<int>(sortedList.size()) - 1, SortField::ID);
            auto p = SearchEngine::binarySearchById(sortedList, query.toStdString());
            if (p) results.push_back(p);
        } else if (method == 2) {
            results = SearchEngine::recursiveSearchByName(db.getPatients(), query.toStdString());
        }

        displayResults(results);
        if (results.empty()) {
            QMessageBox::information(this, "Result", "No matching records found.");
        }
    }

    void SearchPanel::onSortClicked() {
        auto listCopy = db.getPatients();
        int algo = sortAlgoCombo->currentIndex();
        int field = sortFieldCombo->currentIndex();
        SortField sf = (field == 0) ? SortField::Name : (field == 1) ? SortField::ID : SortField::Age;

        if (algo == 0) {
            SearchEngine::selectionSort(listCopy, sf);
        } else {
            SearchEngine::mergeSort(listCopy, 0, static_cast<int>(listCopy.size()) - 1, sf);
        }

        displayResults(listCopy);
        QMessageBox::information(this, "Sorted", "Records sorted successfully using " + sortAlgoCombo->currentText() + ".");
    }
}