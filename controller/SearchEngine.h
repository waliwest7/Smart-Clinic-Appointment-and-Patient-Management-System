#ifndef SEARCHENGINE_H
#define SEARCHENGINE_H

#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
#include "../model/PatientRecord.h"

namespace SmartClinic {
    enum class SortField { Name, ID, Age };
    enum class SortAlgorithm { SelectionSort, MergeSort };

    class SearchEngine {
    private:
        static void recursiveNameSearchHelper(const std::vector<std::shared_ptr<PatientRecord>>& patients, const std::string& lowerQuery, size_t index, std::vector<std::shared_ptr<PatientRecord>>& results) {
            if (index >= patients.size()) return;
            std::string name = patients[index]->getFullName();
            std::string lowerName = name;
            std::transform(lowerName.begin(), lowerName.end(), lowerName.begin(), [](unsigned char c){ return std::tolower(c); });

            if (lowerName.find(lowerQuery) != std::string::npos) {
                results.push_back(patients[index]);
            }
            recursiveNameSearchHelper(patients, lowerQuery, index + 1, results);
        }

    public:
        static std::shared_ptr<PatientRecord> linearSearchById(const std::vector<std::shared_ptr<PatientRecord>>& patients, const std::string& id) {
            for (const auto& p : patients) {
                if (p->getPatientId() == id) {
                    return p;
                }
            }
            return nullptr;
        }

        static std::shared_ptr<PatientRecord> binarySearchById(const std::vector<std::shared_ptr<PatientRecord>>& sortedPatients, const std::string& id) {
            int left = 0;
            int right = static_cast<int>(sortedPatients.size()) - 1;

            while (left <= right) {
                int mid = left + (right - left) / 2;
                if (sortedPatients[mid]->getPatientId() == id) {
                    return sortedPatients[mid];
                }
                if (sortedPatients[mid]->getPatientId() < id) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
            return nullptr;
        }

        static std::vector<std::shared_ptr<PatientRecord>> recursiveSearchByName(const std::vector<std::shared_ptr<PatientRecord>>& patients, const std::string& query) {
            std::string lowerQuery = query;
            std::transform(lowerQuery.begin(), lowerQuery.end(), lowerQuery.begin(), [](unsigned char c){ return std::tolower(c); });
            std::vector<std::shared_ptr<PatientRecord>> results;
            recursiveNameSearchHelper(patients, lowerQuery, 0, results);
            return results;
        }

        static void selectionSort(std::vector<std::shared_ptr<PatientRecord>>& list, SortField field) {
            size_t n = list.size();
            for (size_t i = 0; i < n; ++i) {
                size_t minIdx = i;
                for (size_t j = i + 1; j < n; ++j) {
                    bool condition = false;
                    if (field == SortField::Name) condition = list[j]->getFullName() < list[minIdx]->getFullName();
                    else if (field == SortField::ID) condition = list[j]->getPatientId() < list[minIdx]->getPatientId();
                    else if (field == SortField::Age) condition = list[j]->getAge() < list[minIdx]->getAge();
                    if (condition) minIdx = j;
                }
                if (minIdx != i) std::swap(list[i], list[minIdx]);
            }
        }

        static void merge(std::vector<std::shared_ptr<PatientRecord>>& list, int left, int mid, int right, SortField field) {
            int n1 = mid - left + 1;
            int n2 = right - mid;
            std::vector<std::shared_ptr<PatientRecord>> L(n1);
            std::vector<std::shared_ptr<PatientRecord>> R(n2);
            for (int i = 0; i < n1; i++) L[i] = list[left + i];
            for (int j = 0; j < n2; j++) R[j] = list[mid + 1 + j];

            int i = 0, j = 0, k = left;
            while (i < n1 && j < n2) {
                bool condition = false;
                if (field == SortField::Name) condition = L[i]->getFullName() <= R[j]->getFullName();
                else if (field == SortField::ID) condition = L[i]->getPatientId() <= R[j]->getPatientId();
                else if (field == SortField::Age) condition = L[i]->getAge() <= R[j]->getAge();

                if (condition) list[k++] = L[i++];
                else list[k++] = R[j++];
            }
            while (i < n1) list[k++] = L[i++];
            while (j < n2) list[k++] = R[j++];
        }

        static void mergeSort(std::vector<std::shared_ptr<PatientRecord>>& list, int left, int right, SortField field) {
            if (left < right) {
                int mid = left + (right - left) / 2;
                mergeSort(list, left, mid, field);
                mergeSort(list, mid + 1, right, field);
                merge(list, left, mid, right, field);
            }
        }
    };
}

#endif // SEARCHENGINE_H