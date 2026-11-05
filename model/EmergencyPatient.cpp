#include "EmergencyPatient.h"

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