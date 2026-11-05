#ifndef GENERALPATIENT_H
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