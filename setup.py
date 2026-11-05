import os

files = {
    "CMakeLists.txt": """cmake_minimum_required(VERSION 3.16)
project(SmartClinicSystem LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

set(PROJECT_SOURCES
    main.cpp
    model/ClinicException.h
    model/Appointable.h
    model/PatientRecord.h
    model/PatientRecord.cpp
    model/GeneralPatient.h
    model/GeneralPatient.cpp
    model/EmergencyPatient.h
    model/EmergencyPatient.cpp
    model/FollowUpPatient.h
    model/FollowUpPatient.cpp
    model/Appointment.h
    model/Appointment.cpp
    controller/ClinicDatabase.h
    controller/ClinicDatabase.cpp
    controller/SearchEngine.h
    controller/AppointmentController.h
    utils/IDGenerator.h
    utils/UndoManager.h
    utils/FileHandler.h
    gui/DashboardPanel.h
    gui/DashboardPanel.cpp
    gui/PatientPanel.h
    gui/PatientPanel.cpp
    gui/AppointmentPanel.h
    gui/AppointmentPanel.cpp
    gui/QueuePanel.h
    gui/QueuePanel.cpp
    gui/SearchPanel.h
    gui/SearchPanel.cpp
    gui/ReportsPanel.h
    gui/ReportsPanel.cpp
    gui/MainWindow.h
    gui/MainWindow.cpp
)

add_executable(SmartClinicSystem ${PROJECT_SOURCES})
target_link_libraries(SmartClinicSystem PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
""",

    "main.cpp": """#include <QApplication>
#include "gui/MainWindow.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setStyle("Fusion");

    SmartClinic::MainWindow window;
    window.resize(1280, 800);
    window.show();

    return app.exec();
}
""",

    "model/ClinicException.h": """#ifndef CLINIC_EXCEPTION_H
#define CLINIC_EXCEPTION_H

#include <stdexcept>
#include <string>

namespace SmartClinic {
    class ClinicException : public std::runtime_error {
    public:
        explicit ClinicException(const std::string& message)
            : std::runtime_error("Clinic Error: " + message) {}
    };
}

#endif // CLINIC_EXCEPTION_H
""",

    "model/Appointable.h": """#ifndef APPOINTABLE_H
#define APPOINTABLE_H

#include <string>

namespace SmartClinic {
    class Appointable {
    public:
        virtual ~Appointable() = default;
        virtual bool canScheduleAppointment() const = 0;
        virtual std::string getSpecialInstructions() const = 0;
        virtual void scheduleAppointment() = 0;
        virtual void cancelAppointment() = 0;
    };
}

#endif // APPOINTABLE_H
""",

    "model/PatientRecord.h": """#ifndef PATIENTRECORD_H
#define PATIENTRECORD_H

#include <string>
#include <memory>
#include "Appointable.h"

namespace SmartClinic {
    enum class PatientCategory {
        General,
        Emergency,
        FollowUp
    };

    class PatientRecord : public Appointable {
    protected:
        std::string patientId;
        std::string fullName;
        int age;
        std::string contactInfo;
        PatientCategory category;
        std::string registrationDate;
        int appointmentCount;

    public:
        PatientRecord(std::string id, std::string name, int patientAge, std::string contact, PatientCategory cat, std::string regDate);
        virtual ~PatientRecord() = default;

        std::string getPatientId() const;
        std::string getFullName() const;
        int getAge() const;
        std::string getContactInfo() const;
        PatientCategory getCategory() const;
        std::string getRegistrationDate() const;
        int getAppointmentCount() const;

        void setFullName(const std::string& name);
        void setAge(int patientAge);
        void setContactInfo(const std::string& contact);
        void incrementAppointmentCount();

        void scheduleAppointment() override;
        void cancelAppointment() override;

        virtual std::string getCategoryString() const;
        virtual std::string serialize() const = 0;
        virtual std::shared_ptr<PatientRecord> clone() const = 0;
    };
}

#endif // PATIENTRECORD_H
""",

    "model/PatientRecord.cpp": """#include "PatientRecord.h"

namespace SmartClinic {
    PatientRecord::PatientRecord(std::string id, std::string name, int patientAge, std::string contact, PatientCategory cat, std::string regDate)
        : patientId(std::move(id)), fullName(std::move(name)), age(patientAge), contactInfo(std::move(contact)), category(cat), registrationDate(std::move(regDate)), appointmentCount(0) {}

    std::string PatientRecord::getPatientId() const { return patientId; }
    std::string PatientRecord::getFullName() const { return fullName; }
    int PatientRecord::getAge() const { return age; }
    std::string PatientRecord::getContactInfo() const { return contactInfo; }
    PatientCategory PatientRecord::getCategory() const { return category; }
    std::string PatientRecord::getRegistrationDate() const { return registrationDate; }
    int PatientRecord::getAppointmentCount() const { return appointmentCount; }

    void PatientRecord::setFullName(const std::string& name) { fullName = name; }
    void PatientRecord::setAge(int patientAge) { age = patientAge; }
    void PatientRecord::setContactInfo(const std::string& contact) { contactInfo = contact; }
    void PatientRecord::incrementAppointmentCount() { appointmentCount++; }

    void PatientRecord::scheduleAppointment() { appointmentCount++; }
    void PatientRecord::cancelAppointment() { if (appointmentCount > 0) appointmentCount--; }

    std::string PatientRecord::getCategoryString() const {
        switch (category) {
            case PatientCategory::General: return "General";
            case PatientCategory::Emergency: return "Emergency";
            case PatientCategory::FollowUp: return "Follow-Up";
        }
        return "Unknown";
    }
}
""",

    "model/GeneralPatient.h": """#ifndef GENERALPATIENT_H
#define GENERALPATIENT_H

#include "PatientRecord.h"

namespace SmartClinic {
    class GeneralPatient : public PatientRecord {
    public:
        GeneralPatient(std::string id, std::string name, int age, std::string contact, std::string regDate);
        bool canScheduleAppointment() const override;
        std::string getSpecialInstructions() const override;
        std::string serialize() const override;
        std::shared_ptr<PatientRecord> clone() const override;
    };
}

#endif // GENERALPATIENT_H
""",

    "model/GeneralPatient.cpp": """#include "GeneralPatient.h"

namespace SmartClinic {
    GeneralPatient::GeneralPatient(std::string id, std::string name, int age, std::string contact, std::string regDate)
        : PatientRecord(std::move(id), std::move(name), age, std::move(contact), PatientCategory::General, std::move(regDate)) {}

    bool GeneralPatient::canScheduleAppointment() const { return true; }
    std::string GeneralPatient::getSpecialInstructions() const { return "Standard consultation procedures apply."; }

    std::string GeneralPatient::serialize() const {
        return "GENERAL|" + patientId + "|" + fullName + "|" + std::to_string(age) + "|" + contactInfo + "|" + registrationDate + "|" + std::to_string(appointmentCount);
    }

    std::shared_ptr<PatientRecord> GeneralPatient::clone() const {
        return std::make_shared<GeneralPatient>(*this);
    }
}
""",

    "model/EmergencyPatient.h": """#ifndef EMERGENCYPATIENT_H
#define EMERGENCYPATIENT_H

#include "PatientRecord.h"

namespace SmartClinic {
    class EmergencyPatient : public PatientRecord {
    private:
        std::string triageSeverity;

    public:
        EmergencyPatient(std::string id, std::string name, int age, std::string contact, std::string regDate, std::string severity);
        std::string getTriageSeverity() const;
        void setTriageSeverity(const std::string& severity);

        bool canScheduleAppointment() const override;
        std::string getSpecialInstructions() const override;
        std::string serialize() const override;
        std::shared_ptr<PatientRecord> clone() const override;
    };
}

#endif // EMERGENCYPATIENT_H
""",

    "model/EmergencyPatient.cpp": """#include "EmergencyPatient.h"

namespace SmartClinic {
    EmergencyPatient::EmergencyPatient(std::string id, std::string name, int age, std::string contact, std::string regDate, std::string severity)
        : PatientRecord(std::move(id), std::move(name), age, std::move(contact), PatientCategory::Emergency, std::move(regDate)), triageSeverity(std::move(severity)) {}

    std::string EmergencyPatient::getTriageSeverity() const { return triageSeverity; }
    void EmergencyPatient::setTriageSeverity(const std::string& severity) { triageSeverity = severity; }

    bool EmergencyPatient::canScheduleAppointment() const { return true; }
    std::string EmergencyPatient::getSpecialInstructions() const { return "HIGH PRIORITY: Immediate medical evaluation required (" + triageSeverity + ")."; }

    std::string EmergencyPatient::serialize() const {
        return "EMERGENCY|" + patientId + "|" + fullName + "|" + std::to_string(age) + "|" + contactInfo + "|" + registrationDate + "|" + std::to_string(appointmentCount) + "|" + triageSeverity;
    }

    std::shared_ptr<PatientRecord> EmergencyPatient::clone() const {
        return std::make_shared<EmergencyPatient>(*this);
    }
}
""",

    "model/FollowUpPatient.h": """#ifndef FOLLOWUPPATIENT_H
#define FOLLOWUPPATIENT_H

#include "PatientRecord.h"

namespace SmartClinic {
    class FollowUpPatient : public PatientRecord {
    private:
        std::string originalDiagnosis;
        std::string lastVisitDate;

    public:
        FollowUpPatient(std::string id, std::string name, int age, std::string contact, std::string regDate, std::string diagnosis, std::string lastVisit);
        std::string getOriginalDiagnosis() const;
        std::string getLastVisitDate() const;
        void setOriginalDiagnosis(const std::string& diag);
        void setLastVisitDate(const std::string& date);

        bool canScheduleAppointment() const override;
        std::string getSpecialInstructions() const override;
        std::string serialize() const override;
        std::shared_ptr<PatientRecord> clone() const override;
    };
}

#endif // FOLLOWUPPATIENT_H
""",

    "model/FollowUpPatient.cpp": """#include "FollowUpPatient.h"

namespace SmartClinic {
    FollowUpPatient::FollowUpPatient(std::string id, std::string name, int age, std::string contact, std::string regDate, std::string diagnosis, std::string lastVisit)
        : PatientRecord(std::move(id), std::move(name), age, std::move(contact), PatientCategory::FollowUp, std::move(regDate)), originalDiagnosis(std::move(diagnosis)), lastVisitDate(std::move(lastVisit)) {}

    std::string FollowUpPatient::getOriginalDiagnosis() const { return originalDiagnosis; }
    std::string FollowUpPatient::getLastVisitDate() const { return lastVisitDate; }
    void FollowUpPatient::setOriginalDiagnosis(const std::string& diag) { originalDiagnosis = diag; }
    void FollowUpPatient::setLastVisitDate(const std::string& date) { lastVisitDate = date; }

    bool FollowUpPatient::canScheduleAppointment() const { return true; }
    std::string FollowUpPatient::getSpecialInstructions() const { return "Review previous diagnosis: " + originalDiagnosis + " (Last visit: " + lastVisitDate + ")."; }

    std::string FollowUpPatient::serialize() const {
        return "FOLLOWUP|" + patientId + "|" + fullName + "|" + std::to_string(age) + "|" + contactInfo + "|" + registrationDate + "|" + std::to_string(appointmentCount) + "|" + originalDiagnosis + "|" + lastVisitDate;
    }

    std::shared_ptr<PatientRecord> FollowUpPatient::clone() const {
        return std::make_shared<FollowUpPatient>(*this);
    }
}
""",

    "model/Appointment.h": """#ifndef APPOINTMENT_H
#define APPOINTMENT_H

#include <string>

namespace SmartClinic {
    enum class AppointmentStatus {
        Pending,
        Scheduled,
        Completed,
        Cancelled
    };

    class Appointment {
    private:
        std::string appointmentId;
        std::string patientId;
        std::string patientName;
        std::string date;
        std::string time;
        std::string service;
        std::string clinician;
        std::string reason;
        AppointmentStatus status;

    public:
        Appointment(std::string appId, std::string patId, std::string patName, std::string appDate, std::string appTime, std::string srv, std::string doc, std::string rsn, AppointmentStatus st);

        std::string getAppointmentId() const;
        std::string getPatientId() const;
        std::string getPatientName() const;
        std::string getDate() const;
        std::string getTime() const;
        std::string getService() const;
        std::string getClinician() const;
        std::string getReason() const;
        AppointmentStatus getStatus() const;
        std::string getStatusString() const;

        void setStatus(AppointmentStatus st);
        void setDate(const std::string& d);
        void setTime(const std::string& t);
        void setService(const std::string& s);
        void setClinician(const std::string& c);
        void setReason(const std::string& r);
        void setPatientName(const std::string& name);

        std::string serialize() const;
    };
}

#endif // APPOINTMENT_H
""",

    "model/Appointment.cpp": """#include "Appointment.h"

namespace SmartClinic {
    Appointment::Appointment(std::string appId, std::string patId, std::string patName, std::string appDate, std::string appTime, std::string srv, std::string doc, std::string rsn, AppointmentStatus st)
        : appointmentId(std::move(appId)), patientId(std::move(patId)), patientName(std::move(patName)), date(std::move(appDate)), time(std::move(appTime)), service(std::move(srv)), clinician(std::move(doc)), reason(std::move(rsn)), status(st) {}

    std::string Appointment::getAppointmentId() const { return appointmentId; }
    std::string Appointment::getPatientId() const { return patientId; }
    std::string Appointment::getPatientName() const { return patientName; }
    std::string Appointment::getDate() const { return date; }
    std::string Appointment::getTime() const { return time; }
    std::string Appointment::getService() const { return service; }
    std::string Appointment::getClinician() const { return clinician; }
    std::string Appointment::getReason() const { return reason; }
    AppointmentStatus Appointment::getStatus() const { return status; }

    std::string Appointment::getStatusString() const {
        switch (status) {
            case AppointmentStatus::Pending: return "Pending";
            case AppointmentStatus::Scheduled: return "Scheduled";
            case AppointmentStatus::Completed: return "Completed";
            case AppointmentStatus::Cancelled: return "Cancelled";
        }
        return "Unknown";
    }

    void Appointment::setStatus(AppointmentStatus st) { status = st; }
    void Appointment::setDate(const std::string& d) { date = d; }
    void Appointment::setTime(const std::string& t) { time = t; }
    void Appointment::setService(const std::string& s) { service = s; }
    void Appointment::setClinician(const std::string& c) { clinician = c; }
    void Appointment::setReason(const std::string& r) { reason = r; }
    void Appointment::setPatientName(const std::string& name) { patientName = name; }

    std::string Appointment::serialize() const {
        return appointmentId + "|" + patientId + "|" + patientName + "|" + date + "|" + time + "|" + service + "|" + clinician + "|" + reason + "|" + getStatusString();
    }
}
""",

    "utils/IDGenerator.h": """#ifndef IDGENERATOR_H
#define IDGENERATOR_H

#include <string>
#include <random>

namespace SmartClinic {
    class IDGenerator {
    public:
        static std::string generatePatientId() {
            static std::random_device rd;
            static std::mt19937 gen(rd());
            static std::uniform_int_distribution<> dis(10000, 99999);
            return "PAT-" + std::to_string(dis(gen));
        }

        static std::string generateAppointmentId() {
            static std::random_device rd;
            static std::mt19937 gen(rd());
            static std::uniform_int_distribution<> dis(10000, 99999);
            return "APT-" + std::to_string(dis(gen));
        }
    };
}

#endif // IDGENERATOR_H
""",

    "utils/UndoManager.h": """#ifndef UNDOMANAGER_H
#define UNDOMANAGER_H

#include <stack>
#include <functional>
#include <string>

namespace SmartClinic {
    struct UndoAction {
        std::string description;
        std::function<void()> undoFunction;
    };

    class UndoManager {
    private:
        std::stack<UndoAction> undoStack;

    public:
        void pushAction(const std::string& desc, std::function<void()> func) {
            undoStack.push({desc, func});
        }

        bool canUndo() const {
            return !undoStack.empty();
        }

        std::string popAndExecute() {
            if (undoStack.empty()) return "";
            UndoAction action = undoStack.top();
            undoStack.pop();
            action.undoFunction();
            return action.description;
        }

        void clear() {
            while (!undoStack.empty()) undoStack.pop();
        }
    };
}

#endif // UNDOMANAGER_H
""",

    "utils/FileHandler.h": """#ifndef FILEHANDLER_H
#define FILEHANDLER_H

#include <vector>
#include <memory>
#include <string>
#include <fstream>
#include <sstream>
#include "../model/PatientRecord.h"
#include "../model/GeneralPatient.h"
#include "../model/EmergencyPatient.h"
#include "../model/FollowUpPatient.h"
#include "../model/Appointment.h"
#include "../model/ClinicException.h"

namespace SmartClinic {
    class FileHandler {
    public:
        static bool saveData(const std::string& filepath, const std::vector<std::shared_ptr<PatientRecord>>& patients, const std::vector<Appointment>& appointments) {
            std::ofstream file(filepath);
            if (!file.is_open()) return false;

            file << "[PATIENTS]\\n";
            for (const auto& p : patients) {
                file << p->serialize() << "\\n";
            }

            file << "[APPOINTMENTS]\\n";
            for (const auto& a : appointments) {
                file << a.serialize() << "\\n";
            }

            return file.good();
        }

        static bool loadData(const std::string& filepath, std::vector<std::shared_ptr<PatientRecord>>& outPatients, std::vector<Appointment>& outAppointments) {
            std::ifstream file(filepath);
            if (!file.is_open()) return false;

            std::vector<std::shared_ptr<PatientRecord>> tempPatients;
            std::vector<Appointment> tempAppointments;

            std::string line;
            bool readingPatients = false;
            bool readingAppointments = false;

            try {
                while (std::getline(file, line)) {
                    if (line.empty()) continue;
                    if (line == "[PATIENTS]") {
                        readingPatients = true;
                        readingAppointments = false;
                        continue;
                    } else if (line == "[APPOINTMENTS]") {
                        readingPatients = false;
                        readingAppointments = true;
                        continue;
                    }

                    if (readingPatients) {
                        std::stringstream ss(line);
                        std::string type, id, name, ageStr, contact, regDate;
                        std::getline(ss, type, '|');
                        std::getline(ss, id, '|');
                        std::getline(ss, name, '|');
                        std::getline(ss, ageStr, '|');
                        std::getline(ss, contact, '|');
                        std::getline(ss, regDate, '|');

                        int age = std::stoi(ageStr);
                        if (age < 0 || age > 120) throw ClinicException("Loaded age out of range.");

                        if (type == "GENERAL") {
                            std::string appCountStr;
                            std::getline(ss, appCountStr, '|');
                            tempPatients.push_back(std::make_shared<GeneralPatient>(id, name, age, contact, regDate));
                        } else if (type == "EMERGENCY") {
                            std::string appCountStr, severity;
                            std::getline(ss, appCountStr, '|');
                            std::getline(ss, severity, '|');
                            tempPatients.push_back(std::make_shared<EmergencyPatient>(id, name, age, contact, regDate, severity));
                        } else if (type == "FOLLOWUP") {
                            std::string appCountStr, diag, lastVisit;
                            std::getline(ss, appCountStr, '|');
                            std::getline(ss, diag, '|');
                            std::getline(ss, lastVisit, '|');
                            tempPatients.push_back(std::make_shared<FollowUpPatient>(id, name, age, contact, regDate, diag, lastVisit));
                        }
                    } else if (readingAppointments) {
                        std::stringstream ss(line);
                        std::string appId, patId, patName, date, time, srv, doc, rsn, stStr;
                        std::getline(ss, appId, '|');
                        std::getline(ss, patId, '|');
                        std::getline(ss, patName, '|');
                        std::getline(ss, date, '|');
                        std::getline(ss, time, '|');
                        std::getline(ss, srv, '|');
                        std::getline(ss, doc, '|');
                        std::getline(ss, rsn, '|');
                        std::getline(ss, stStr, '|');

                        AppointmentStatus st = AppointmentStatus::Pending;
                        if (stStr == "Scheduled") st = AppointmentStatus::Scheduled;
                        else if (stStr == "Completed") st = AppointmentStatus::Completed;
                        else if (stStr == "Cancelled") st = AppointmentStatus::Cancelled;

                        tempAppointments.emplace_back(appId, patId, patName, date, time, srv, doc, rsn, st);
                    }
                }
            } catch (...) {
                return false;
            }

            outPatients = std::move(tempPatients);
            outAppointments = std::move(tempAppointments);
            return true;
        }
    };
}

#endif // FILEHANDLER_H
""",

    "controller/SearchEngine.h": """#ifndef SEARCHENGINE_H
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
""",

    "controller/ClinicDatabase.h": """#ifndef CLINICDATABASE_H
#define CLINICDATABASE_H

#include <vector>
#include <queue>
#include <memory>
#include <array>
#include "../model/PatientRecord.h"
#include "../model/Appointment.h"
#include "../utils/UndoManager.h"

namespace SmartClinic {
    class ClinicDatabase {
    private:
        std::vector<std::shared_ptr<PatientRecord>> patients;
        std::vector<Appointment> appointments;
        std::queue<std::shared_ptr<PatientRecord>> waitingQueue;
        UndoManager undoManager;

        std::array<std::shared_ptr<PatientRecord>, 10> patientCache{};
        size_t cacheSize = 0;

        void purgeCacheForId(const std::string& id);

    public:
        ClinicDatabase();

        void addPatient(std::shared_ptr<PatientRecord> patient, bool recordUndo = true);
        bool deletePatient(const std::string& patientId, bool recordUndo = true);
        bool editPatient(const std::string& patientId, const std::string& newName, int newAge, const std::string& newContact, bool recordUndo = true);
        std::shared_ptr<PatientRecord> findPatient(const std::string& patientId);
        std::vector<std::shared_ptr<PatientRecord>>& getPatients();

        void addAppointment(const Appointment& app, bool recordUndo = true);
        bool cancelAppointment(const std::string& appointmentId, bool recordUndo = true);
        bool completeAppointment(const std::string& appointmentId);
        std::vector<Appointment>& getAppointments();

        void enqueuePatient(std::shared_ptr<PatientRecord> patient);
        std::shared_ptr<PatientRecord> dequeuePatient();
        std::queue<std::shared_ptr<PatientRecord>> getWaitingQueueCopy() const;
        void clearQueue();
        bool isPatientInQueue(const std::string& patientId) const;

        void updateCache(std::shared_ptr<PatientRecord> patient);
        std::shared_ptr<PatientRecord> getCachedPatient(const std::string& id);

        UndoManager& getUndoManager();
        void clearAllData();
    };
}

#endif // CLINICDATABASE_H
""",

    "controller/ClinicDatabase.cpp": """#include "ClinicDatabase.h"
#include "../model/ClinicException.h"

namespace SmartClinic {
    ClinicDatabase::ClinicDatabase() {
        patientCache.fill(nullptr);
    }

    void ClinicDatabase::purgeCacheForId(const std::string& id) {
        for (size_t i = 0; i < cacheSize; ++i) {
            if (patientCache[i] && patientCache[i]->getPatientId() == id) {
                for (size_t j = i; j < cacheSize - 1; ++j) {
                    patientCache[j] = patientCache[j + 1];
                }
                patientCache[--cacheSize] = nullptr;
                break;
            }
        }
    }

    void ClinicDatabase::addPatient(std::shared_ptr<PatientRecord> patient, bool recordUndo) {
        if (findPatient(patient->getPatientId()) != nullptr) {
            throw ClinicException("Patient ID " + patient->getPatientId() + " already exists.");
        }
        if (patient->getAge() < 0 || patient->getAge() > 120) {
            throw ClinicException("Patient age must be between 0 and 120.");
        }

        patients.push_back(patient);
        updateCache(patient);

        if (recordUndo) {
            std::string id = patient->getPatientId();
            undoManager.pushAction("Register Patient: " + id, [this, id]() {
                this->deletePatient(id, false);
            });
        }
    }

    bool ClinicDatabase::deletePatient(const std::string& patientId, bool recordUndo) {
        for (auto it = patients.begin(); it != patients.end(); ++it) {
            if ((*it)->getPatientId() == patientId) {
                if (recordUndo) {
                    auto cloned = (*it)->clone();
                    undoManager.pushAction("Delete Patient: " + patientId, [this, c = cloned]() mutable {
                        this->addPatient(c, false);
                    });
                }
                purgeCacheForId(patientId);
                patients.erase(it);
                return true;
            }
        }
        return false;
    }

    bool ClinicDatabase::editPatient(const std::string& patientId, const std::string& newName, int newAge, const std::string& newContact, bool recordUndo) {
        auto pat = findPatient(patientId);
        if (!pat) return false;

        if (newAge < 0 || newAge > 120) {
            throw ClinicException("Patient age must be between 0 and 120.");
        }

        std::string oldName = pat->getFullName();
        int oldAge = pat->getAge();
        std::string oldContact = pat->getContactInfo();

        if (recordUndo) {
            undoManager.pushAction("Edit Patient: " + patientId, [this, patientId, oldName, oldAge, oldContact]() {
                this->editPatient(patientId, oldName, oldAge, oldContact, false);
            });
        }

        pat->setFullName(newName);
        pat->setAge(newAge);
        pat->setContactInfo(newContact);

        for (auto& app : appointments) {
            if (app.getPatientId() == patientId) {
                app.setPatientName(newName);
            }
        }
        return true;
    }

    std::shared_ptr<PatientRecord> ClinicDatabase::findPatient(const std::string& patientId) {
        auto cached = getCachedPatient(patientId);
        if (cached) return cached;

        for (const auto& p : patients) {
            if (p->getPatientId() == patientId) {
                updateCache(p);
                return p;
            }
        }
        return nullptr;
    }

    std::vector<std::shared_ptr<PatientRecord>>& ClinicDatabase::getPatients() {
        return patients;
    }

    void ClinicDatabase::addAppointment(const Appointment& app, bool recordUndo) {
        appointments.push_back(app);
        auto pat = findPatient(app.getPatientId());
        if (pat) pat->scheduleAppointment();

        if (recordUndo) {
            std::string appId = app.getAppointmentId();
            undoManager.pushAction("Schedule Appointment: " + appId, [this, appId]() {
                this->cancelAppointment(appId, false);
            });
        }
    }

    bool ClinicDatabase::cancelAppointment(const std::string& appointmentId, bool recordUndo) {
        for (auto it = appointments.begin(); it != appointments.end(); ++it) {
            if (it->getAppointmentId() == appointmentId) {
                if (it->getStatus() == AppointmentStatus::Cancelled) {
                    throw ClinicException("Appointment is already cancelled.");
                }

                Appointment backup = *it;
                it->setStatus(AppointmentStatus::Cancelled);
                auto pat = findPatient(it->getPatientId());
                if (pat) pat->cancelAppointment();

                if (recordUndo) {
                    undoManager.pushAction("Cancel Appointment: " + appointmentId, [this, backup]() {
                        for (auto& app : appointments) {
                            if (app.getAppointmentId() == backup.getAppointmentId()) {
                                app = backup;
                                auto p = findPatient(backup.getPatientId());
                                if (p && backup.getStatus() == AppointmentStatus::Scheduled) p->scheduleAppointment();
                                return;
                            }
                        }
                    });
                }
                return true;
            }
        }
        return false;
    }

    bool ClinicDatabase::completeAppointment(const std::string& appointmentId) {
        for (auto& app : appointments) {
            if (app.getAppointmentId() == appointmentId) {
                if (app.getStatus() == AppointmentStatus::Cancelled) {
                    throw ClinicException("Cannot complete a cancelled appointment.");
                }
                app.setStatus(AppointmentStatus::Completed);
                return true;
            }
        }
        return false;
    }

    std::vector<Appointment>& ClinicDatabase::getAppointments() {
        return appointments;
    }

    void ClinicDatabase::enqueuePatient(std::shared_ptr<PatientRecord> patient) {
        waitingQueue.push(patient);
    }

    std::shared_ptr<PatientRecord> ClinicDatabase::dequeuePatient() {
        if (waitingQueue.empty()) return nullptr;
        auto p = waitingQueue.front();
        waitingQueue.pop();
        return p;
    }

    std::queue<std::shared_ptr<PatientRecord>> ClinicDatabase::getWaitingQueueCopy() const {
        return waitingQueue;
    }

    void ClinicDatabase::clearQueue() {
        std::queue<std::shared_ptr<PatientRecord>> emptyQueue;
        std::swap(waitingQueue, emptyQueue);
    }

    bool ClinicDatabase::isPatientInQueue(const std::string& patientId) const {
        std::queue<std::shared_ptr<PatientRecord>> temp = waitingQueue;
        while (!temp.empty()) {
            if (temp.front()->getPatientId() == patientId) return true;
            temp.pop();
        }
        return false;
    }

    void ClinicDatabase::updateCache(std::shared_ptr<PatientRecord> patient) {
        for (size_t i = 0; i < cacheSize; ++i) {
            if (patientCache[i] == patient) return;
        }
        if (cacheSize < 10) {
            patientCache[cacheSize++] = patient;
        } else {
            for (size_t i = 0; i < 9; ++i) {
                patientCache[i] = patientCache[i + 1];
            }
            patientCache[9] = patient;
        }
    }

    std::shared_ptr<PatientRecord> ClinicDatabase::getCachedPatient(const std::string& id) {
        for (size_t i = 0; i < cacheSize; ++i) {
            if (patientCache[i] && patientCache[i]->getPatientId() == id) {
                return patientCache[i];
            }
        }
        return nullptr;
    }

    UndoManager& ClinicDatabase::getUndoManager() {
        return undoManager;
    }

    void ClinicDatabase::clearAllData() {
        patients.clear();
        appointments.clear();
        clearQueue();
        undoManager.clear();
        patientCache.fill(nullptr);
        cacheSize = 0;
    }
}
""",

    "controller/AppointmentController.h": """#ifndef APPOINTMENTCONTROLLER_H
#define APPOINTMENTCONTROLLER_H

#include "ClinicDatabase.h"
#include "../model/Appointment.h"
#include "../model/ClinicException.h"

namespace SmartClinic {
    class AppointmentController {
    private:
        ClinicDatabase& db;

    public:
        explicit AppointmentController(ClinicDatabase& database) : db(database) {}

        void bookAppointment(const std::string& appId, const std::string& patId, const std::string& date, const std::string& time, const std::string& service, const std::string& clinician, const std::string& reason) {
            auto patient = db.findPatient(patId);
            if (!patient) {
                throw ClinicException("Patient ID " + patId + " not found.");
            }

            for (const auto& app : db.getAppointments()) {
                if (app.getPatientId() == patId && app.getDate() == date && app.getTime() == time && app.getStatus() != AppointmentStatus::Cancelled) {
                    throw ClinicException("Duplicate booking detected for this patient at the same date/time.");
                }
            }

            Appointment newApp(appId, patId, patient->getFullName(), date, time, service, clinician, reason, AppointmentStatus::Scheduled);
            db.addAppointment(newApp);
        }
    };
}

#endif // APPOINTMENTCONTROLLER_H
""",

    "gui/DashboardPanel.h": """#ifndef DASHBOARD_PANEL_H
#define DASHBOARD_PANEL_H

#include <QWidget>
#include <QLabel>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class DashboardPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QLabel* totalPatientsVal;
        QLabel* todayApptsVal;
        QLabel* pendingApptsVal;
        QLabel* waitingQueueVal;
        QLabel* emergencyCountVal;

        void setupUI();

    public:
        explicit DashboardPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshDashboard();
    };
}

#endif // DASHBOARD_PANEL_H
""",

    "gui/DashboardPanel.cpp": """#include "DashboardPanel.h"
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
        header->setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;");
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
""",

    "gui/PatientPanel.h": """#ifndef PATIENT_PANEL_H
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
""",

    "gui/PatientPanel.cpp": """#include "PatientPanel.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QMessageBox>
#include <QDialog>
#include <QFormLayout>
#include <QDialogButtonBox>
#include <QDate>
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
""",

    "gui/AppointmentPanel.h": """#ifndef APPOINTMENT_PANEL_H
#define APPOINTMENT_PANEL_H

#include <QWidget>
#include <QTableWidget>
#include "../controller/ClinicDatabase.h"
#include "../controller/AppointmentController.h"

namespace SmartClinic {
    class AppointmentPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        AppointmentController appointmentController;
        QTableWidget* tableWidget;

        void setupUI();

    public:
        explicit AppointmentPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void refreshTable();

    private slots:
        void onScheduleClicked();
        void onCancelClicked();
        void onCompleteClicked();
    };
}

#endif // APPOINTMENT_PANEL_H
""",

    "gui/AppointmentPanel.cpp": """#include "AppointmentPanel.h"
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
""",

    "gui/QueuePanel.h": """#ifndef QUEUE_PANEL_H
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
""",

    "gui/QueuePanel.cpp": """#include "QueuePanel.h"
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
        QMessageBox::information(this, "Calling Patient", QString::fromStdString("Calling next patient for consultation:\\n\\nName: " + pat->getFullName() + "\\nInstructions: " + pat->getSpecialInstructions()));
    }

    void QueuePanel::onClearQueueClicked() {
        if (QMessageBox::question(this, "Confirm", "Clear the entire waiting queue?") == QMessageBox::Yes) {
            db.clearQueue();
            refreshTable();
        }
    }
}
""",

    "gui/SearchPanel.h": """#ifndef SEARCH_PANEL_H
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
""",

    "gui/SearchPanel.cpp": """#include "SearchPanel.h"
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
""",

    "gui/ReportsPanel.h": """#ifndef REPORTS_PANEL_H
#define REPORTS_PANEL_H

#include <QWidget>
#include <QTextEdit>
#include "../controller/ClinicDatabase.h"

namespace SmartClinic {
    class ReportsPanel : public QWidget {
        Q_OBJECT
    private:
        ClinicDatabase& db;
        QTextEdit* reportTextEdit;

        void setupUI();

    public:
        explicit ReportsPanel(ClinicDatabase& database, QWidget* parent = nullptr);
        void generateReports();
    };
}

#endif // REPORTS_PANEL_H
""",

    "gui/ReportsPanel.cpp": """#include "ReportsPanel.h"
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
        reportTextEdit->setStyleSheet("font-family: Consolas, monospace; font-size: 13px; background-color: #f8f9fa;");
        layout->addWidget(reportTextEdit);

        connect(refreshBtn, &QPushButton::clicked, this, &ReportsPanel::generateReports);
    }

    void ReportsPanel::generateReports() {
        QString report;
        QTextStream out(&report);

        out << "===================================================\\n";
        out << "          UNIVERSITY CLINIC MANAGEMENT SYSTEM      \\n";
        out << "                   OFFICIAL REPORTS                \\n";
        out << "===================================================\\n\\n";

        out << "1. MOST FREQUENTLY ATTENDED PATIENTS (Ranked)\\n";
        out << "---------------------------------------------------\\n";
        auto patList = db.getPatients();
        std::sort(patList.begin(), patList.end(), [](const auto& a, const auto& b) {
            return a->getAppointmentCount() > b->getAppointmentCount();
        });
        int rank = 1;
        for (const auto& p : patList) {
            out << rank++ << ". " << QString::fromStdString(p->getFullName()) 
                << " (ID: " << QString::fromStdString(p->getPatientId()) << ") - " 
                << p->getAppointmentCount() << " appointments\\n";
        }
        out << "\\n";

        out << "2. PATIENTS WITH PENDING / SCHEDULED APPOINTMENTS\\n";
        out << "---------------------------------------------------\\n";
        for (const auto& a : db.getAppointments()) {
            if (a.getStatus() == AppointmentStatus::Scheduled || a.getStatus() == AppointmentStatus::Pending) {
                out << "- Appt ID: " << QString::fromStdString(a.getAppointmentId()) 
                    << " | Patient: " << QString::fromStdString(a.getPatientName()) 
                    << " | Date: " << QString::fromStdString(a.getDate()) 
                    << " @ " << QString::fromStdString(a.getTime()) << "\\n";
            }
        }
        out << "\\n";

        out << "3. PATIENT CATEGORY DISTRIBUTION\\n";
        out << "---------------------------------------------------\\n";
        int genCount = 0, emgCount = 0, folCount = 0;
        for (const auto& p : patList) {
            if (p->getCategory() == PatientCategory::General) genCount++;
            else if (p->getCategory() == PatientCategory::Emergency) emgCount++;
            else if (p->getCategory() == PatientCategory::FollowUp) folCount++;
        }
        out << "- General Patients:   " << genCount << "\\n";
        out << "- Emergency Patients: " << emgCount << "\\n";
        out << "- Follow-Up Patients: " << folCount << "\\n";
        out << "- Total Registered:   " << patList.size() << "\\n\\n";

        out << "4. DAILY APPOINTMENT SUMMARY\\n";
        out << "---------------------------------------------------\\n";
        int totalAppts = db.getAppointments().size();
        int completed = 0, pending = 0, scheduled = 0, cancelled = 0;
        for (const auto& a : db.getAppointments()) {
            if (a.getStatus() == AppointmentStatus::Completed) completed++;
            else if (a.getStatus() == AppointmentStatus::Pending) pending++;
            else if (a.getStatus() == AppointmentStatus::Scheduled) scheduled++;
            else if (a.getStatus() == AppointmentStatus::Cancelled) cancelled++;
        }
        out << "- Total Appointments: " << totalAppts << "\\n";
        out << "- Scheduled:          " << scheduled << "\\n";
        out << "- Pending:            " << pending << "\\n";
        out << "- Completed:          " << completed << "\\n";
        out << "- Cancelled:          " << cancelled << "\\n";
        out << "===================================================\\n";

        reportTextEdit->setPlainText(report);
    }
}
""",

    "gui/MainWindow.h": """#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QListWidget>
#include <QLabel>
#include "../controller/ClinicDatabase.h"
#include "DashboardPanel.h"
#include "PatientPanel.h"
#include "AppointmentPanel.h"
#include "QueuePanel.h"
#include "SearchPanel.h"
#include "ReportsPanel.h"

namespace SmartClinic {
    class MainWindow : public QMainWindow {
        Q_OBJECT

    private:
        ClinicDatabase clinicDb;
        QStackedWidget* stackedWidget;
        QListWidget* navListWidget;
        QLabel* statusLabel;

        DashboardPanel* dashboardPanel;
        PatientPanel* patientPanel;
        AppointmentPanel* appointmentPanel;
        QueuePanel* queuePanel;
        SearchPanel* searchPanel;
        ReportsPanel* reportsPanel;

        void setupUI();
        void createMenus();

    public:
        MainWindow(QWidget* parent = nullptr);
        ~MainWindow() = default;

    private slots:
        void handleNavigation(int row);
        void onSaveTriggered();
        void onLoadTriggered();
        void onUndoTriggered();
    };
}

#endif // MAINWINDOW_H
""",

    "gui/MainWindow.cpp": """#include "MainWindow.h"
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QMenuBar>
#include <QStatusBar>
#include <QMessageBox>
#include <QFileDialog>
#include "../utils/FileHandler.h"

namespace SmartClinic {
    MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
        setWindowTitle("Smart Clinic Appointment & Patient Management System");
        setupUI();
        createMenus();
    }

    void MainWindow::setupUI() {
        QWidget* centralWidget = new QWidget(this);
        QHBoxLayout* mainLayout = new QHBoxLayout(centralWidget);
        mainLayout->setContentsMargins(0, 0, 0, 0);

        navListWidget = new QListWidget(this);
        navListWidget->addItem("📊 Dashboard");
        navListWidget->addItem("👥 Patient Records");
        navListWidget->addItem("📅 Appointments");
        navListWidget->addItem("⏳ Waiting Queue");
        navListWidget->addItem("🔍 Search & Sort");
        navListWidget->addItem("📈 Reports");
        navListWidget->setFixedWidth(220);
        navListWidget->setStyleSheet("QListWidget { background-color: #2c3e50; color: white; font-size: 14px; border: none; padding: 10px; }"
                                     "QListWidget::item { padding: 12px; border-radius: 6px; margin-bottom: 4px; }"
                                     "QListWidget::item:selected { background-color: #3498db; color: white; }");

        stackedWidget = new QStackedWidget(this);

        dashboardPanel = new DashboardPanel(clinicDb, this);
        patientPanel = new PatientPanel(clinicDb, this);
        appointmentPanel = new AppointmentPanel(clinicDb, this);
        queuePanel = new QueuePanel(clinicDb, this);
        searchPanel = new SearchPanel(clinicDb, this);
        reportsPanel = new ReportsPanel(clinicDb, this);

        stackedWidget->addWidget(dashboardPanel);   // Index 0
        stackedWidget->addWidget(patientPanel);     // Index 1
        stackedWidget->addWidget(appointmentPanel); // Index 2
        stackedWidget->addWidget(queuePanel);       // Index 3
        stackedWidget->addWidget(searchPanel);      // Index 4
        stackedWidget->addWidget(reportsPanel);     // Index 5

        mainLayout->addWidget(navListWidget);
        mainLayout->addWidget(stackedWidget);
        setCentralWidget(centralWidget);

        connect(navListWidget, &QListWidget::rowChanged, this, &MainWindow::handleNavigation);
        navListWidget->setCurrentRow(0);

        statusLabel = new QLabel("Ready", this);
        statusBar()->addPermanentWidget(statusLabel);
    }

    void MainWindow::createMenus() {
        QMenu* fileMenu = menuBar()->addMenu("&File");
        
        QAction* saveAction = fileMenu->addAction("&Save Data");
        saveAction->setShortcut(QKeySequence::Save);
        connect(saveAction, &QAction::triggered, this, &MainWindow::onSaveTriggered);

        QAction* loadAction = fileMenu->addAction("&Load Data");
        loadAction->setShortcut(QKeySequence::Open);
        connect(loadAction, &QAction::triggered, this, &MainWindow::onLoadTriggered);

        fileMenu->addSeparator();
        QAction* exitAction = fileMenu->addAction("E&xit");
        exitAction->setShortcut(QKeySequence::Quit);
        connect(exitAction, &QAction::triggered, this, &QWidget::close);

        QMenu* editMenu = menuBar()->addMenu("&Edit");
        QAction* undoAction = editMenu->addAction("&Undo Last Operation");
        undoAction->setShortcut(QKeySequence::Undo);
        connect(undoAction, &QAction::triggered, this, &MainWindow::onUndoTriggered);
    }

    void MainWindow::handleNavigation(int row) {
        stackedWidget->setCurrentIndex(row);
        if (row == 0) dashboardPanel->refreshDashboard();
        else if (row == 2) appointmentPanel->refreshTable();
        else if (row == 3) queuePanel->refreshTable();
        else if (row == 5) reportsPanel->generateReports();

        statusLabel->setText("Switched workspace section: " + navListWidget->item(row)->text());
    }

    void MainWindow::onSaveTriggered() {
        QString fileName = QFileDialog::getSaveFileName(this, "Save Clinic Data", "", "Clinic Data Files (*.dat);;All Files (*)");
        if (fileName.isEmpty()) return;

        bool success = FileHandler::saveData(fileName.toStdString(), clinicDb.getPatients(), clinicDb.getAppointments());
        if (success) {
            statusLabel->setText("Data successfully saved to " + fileName);
            QMessageBox::information(this, "Success", "Clinic records saved successfully.");
        } else {
            QMessageBox::critical(this, "Error", "Failed to save data to file.");
        }
    }

    void MainWindow::onLoadTriggered() {
        QString fileName = QFileDialog::getOpenFileName(this, "Load Clinic Data", "", "Clinic Data Files (*.dat);;All Files (*)");
        if (fileName.isEmpty()) return;

        std::vector<std::shared_ptr<PatientRecord>> loadedPatients;
        std::vector<Appointment> loadedAppointments;

        bool success = FileHandler::loadData(fileName.toStdString(), loadedPatients, loadedAppointments);
        if (success) {
            clinicDb.clearAllData();
            for (auto& p : loadedPatients) {
                clinicDb.addPatient(p, false);
            }
            for (auto& a : loadedAppointments) {
                clinicDb.addAppointment(a, false);
            }
            dashboardPanel->refreshDashboard();
            patientPanel->refreshTable();
            appointmentPanel->refreshTable();
            queuePanel->refreshTable();
            reportsPanel->generateReports();

            statusLabel->setText("Data successfully loaded from " + fileName);
            QMessageBox::information(this, "Success", "Clinic records loaded successfully.");
        } else {
            QMessageBox::critical(this, "Error", "Failed to load data or file validation failed.");
        }
    }

    void MainWindow::onUndoTriggered() {
        if (!clinicDb.getUndoManager().canUndo()) {
            QMessageBox::information(this, "Undo", "No operations available to undo.");
            return;
        }
        std::string desc = clinicDb.getUndoManager().popAndExecute();
        dashboardPanel->refreshDashboard();
        patientPanel->refreshTable();
        appointmentPanel->refreshTable();
        queuePanel->refreshTable();
        reportsPanel->generateReports();

        statusLabel->setText(QString::fromStdString("Undid operation: " + desc));
        QMessageBox::information(this, "Undo Successful", QString::fromStdString("Successfully reversed: " + desc));
    }
}
"""
}

for filepath, content in files.items():
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Successfully generated: {filepath}")

print("\\nAll project files and directories have been created successfully!")