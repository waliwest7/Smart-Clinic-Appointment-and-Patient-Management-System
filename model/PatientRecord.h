#ifndef PATIENTRECORD_H
#define PATIENTRECORD_H

#include <string>
#include <memory>
#include "Appointable.h"

namespace SmartClinic {
    enum class PatientCategory {
        General,
        Emergency,
        FollowUp
    };

    class PatientRecord : public Appointable {
    protected:
        std::string patientId;
        std::string fullName;
        int age;
        std::string contactInfo;
        PatientCategory category;
        std::string registrationDate;
        int appointmentCount;

    public:
        PatientRecord(std::string id, std::string name, int patientAge, std::string contact, PatientCategory cat, std::string regDate);
        virtual ~PatientRecord() = default;

        std::string getPatientId() const;
        std::string getFullName() const;
        int getAge() const;
        std::string getContactInfo() const;
        PatientCategory getCategory() const;
        std::string getRegistrationDate() const;
        int getAppointmentCount() const;

        void setFullName(const std::string& name);
        void setAge(int patientAge);
        void setContactInfo(const std::string& contact);
        void incrementAppointmentCount();

        void scheduleAppointment() override;
        void cancelAppointment() override;

        virtual std::string getCategoryString() const;
        virtual std::string serialize() const = 0;
        virtual std::shared_ptr<PatientRecord> clone() const = 0;
    };
}

#endif // PATIENTRECORD_H