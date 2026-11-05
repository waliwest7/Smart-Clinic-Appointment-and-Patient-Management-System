#ifndef EMERGENCYPATIENT_H
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