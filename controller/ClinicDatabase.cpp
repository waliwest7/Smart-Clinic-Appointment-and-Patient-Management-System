#include "ClinicDatabase.h"
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