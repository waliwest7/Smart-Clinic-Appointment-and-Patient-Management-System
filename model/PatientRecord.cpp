#include "PatientRecord.h"

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