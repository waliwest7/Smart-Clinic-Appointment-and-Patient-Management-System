#ifndef APPOINTMENTCONTROLLER_H
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