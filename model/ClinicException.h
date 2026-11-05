#ifndef CLINIC_EXCEPTION_H
#define CLINIC_EXCEPTION_H

#include <stdexcept>
#include <string>

namespace SmartClinic {
    class ClinicException : public std::runtime_error {
    public:
        explicit ClinicException(const std::string& message)
            : std::runtime_error("Clinic Error: " + message) {}
    };
}

#endif // CLINIC_EXCEPTION_H