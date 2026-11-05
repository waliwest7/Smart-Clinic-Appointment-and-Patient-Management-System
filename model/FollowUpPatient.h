#ifndef FOLLOWUPPATIENT_H
#define FOLLOWUPPATIENT_H

#include "PatientRecord.h"

namespace SmartClinic {
    class FollowUpPatient : public PatientRecord {
    private:
        std::string originalDiagnosis;
        std::string lastVisitDate;

    public:
        FollowUpPatient(std::string id, std::string name, int age, std::string contact, std::string regDate, std::string diagnosis, std::string lastVisit);
        std::string getOriginalDiagnosis() const;
        std::string getLastVisitDate() const;
        void setOriginalDiagnosis(const std::string& diag);
        void setLastVisitDate(const std::string& date);

        bool canScheduleAppointment() const override;
        std::string getSpecialInstructions() const override;
        std::string serialize() const override;
        std::shared_ptr<PatientRecord> clone() const override;
    };
}

#endif // FOLLOWUPPATIENT_H