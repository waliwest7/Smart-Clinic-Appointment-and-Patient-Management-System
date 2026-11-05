#include "GeneralPatient.h"

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