#include "FollowUpPatient.h"

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