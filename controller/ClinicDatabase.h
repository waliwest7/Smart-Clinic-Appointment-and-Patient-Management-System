#ifndef CLINICDATABASE_H
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