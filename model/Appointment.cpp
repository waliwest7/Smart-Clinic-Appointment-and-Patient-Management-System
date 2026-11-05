#include "Appointment.h"

namespace SmartClinic {
    Appointment::Appointment(std::string appId, std::string patId, std::string patName, std::string appDate, std::string appTime, std::string srv, std::string doc, std::string rsn, AppointmentStatus st)
        : appointmentId(std::move(appId)), patientId(std::move(patId)), patientName(std::move(patName)), date(std::move(appDate)), time(std::move(appTime)), service(std::move(srv)), clinician(std::move(doc)), reason(std::move(rsn)), status(st) {}

    std::string Appointment::getAppointmentId() const { return appointmentId; }
    std::string Appointment::getPatientId() const { return patientId; }
    std::string Appointment::getPatientName() const { return patientName; }
    std::string Appointment::getDate() const { return date; }
    std::string Appointment::getTime() const { return time; }
    std::string Appointment::getService() const { return service; }
    std::string Appointment::getClinician() const { return clinician; }
    std::string Appointment::getReason() const { return reason; }
    AppointmentStatus Appointment::getStatus() const { return status; }

    std::string Appointment::getStatusString() const {
        switch (status) {
            case AppointmentStatus::Pending: return "Pending";
            case AppointmentStatus::Scheduled: return "Scheduled";
            case AppointmentStatus::Completed: return "Completed";
            case AppointmentStatus::Cancelled: return "Cancelled";
        }
        return "Unknown";
    }

    void Appointment::setStatus(AppointmentStatus st) { status = st; }
    void Appointment::setDate(const std::string& d) { date = d; }
    void Appointment::setTime(const std::string& t) { time = t; }
    void Appointment::setService(const std::string& s) { service = s; }
    void Appointment::setClinician(const std::string& c) { clinician = c; }
    void Appointment::setReason(const std::string& r) { reason = r; }
    void Appointment::setPatientName(const std::string& name) { patientName = name; }

    std::string Appointment::serialize() const {
        return appointmentId + "|" + patientId + "|" + patientName + "|" + date + "|" + time + "|" + service + "|" + clinician + "|" + reason + "|" + getStatusString();
    }
}