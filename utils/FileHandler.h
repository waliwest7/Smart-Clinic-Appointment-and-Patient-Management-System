#ifndef FILEHANDLER_H
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

            file << "[PATIENTS]\n";
            for (const auto& p : patients) {
                file << p->serialize() << "\n";
            }

            file << "[APPOINTMENTS]\n";
            for (const auto& a : appointments) {
                file << a.serialize() << "\n";
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