#ifndef APPOINTMENT_H
#define APPOINTMENT_H

#include <string>

namespace SmartClinic {
    enum class AppointmentStatus {
        Pending,
        Scheduled,
        Completed,
        Cancelled
    };

    class Appointment {
    private:
        std::string appointmentId;
        std::string patientId;
        std::string patientName;
        std::string date;
        std::string time;
        std::string service;
        std::string clinician;
        std::string reason;
        AppointmentStatus status;

    public:
        Appointment(std::string appId, std::string patId, std::string patName, std::string appDate, std::string appTime, std::string srv, std::string doc, std::string rsn, AppointmentStatus st);

        std::string getAppointmentId() const;
        std::string getPatientId() const;
        std::string getPatientName() const;
        std::string getDate() const;
        std::string getTime() const;
        std::string getService() const;
        std::string getClinician() const;
        std::string getReason() const;
        AppointmentStatus getStatus() const;
        std::string getStatusString() const;

        void setStatus(AppointmentStatus st);
        void setDate(const std::string& d);
        void setTime(const std::string& t);
        void setService(const std::string& s);
        void setClinician(const std::string& c);
        void setReason(const std::string& r);
        void setPatientName(const std::string& name);

        std::string serialize() const;
    };
}

#endif // APPOINTMENT_H