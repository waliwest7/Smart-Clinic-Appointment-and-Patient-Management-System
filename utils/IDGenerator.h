#ifndef IDGENERATOR_H
#define IDGENERATOR_H

#include <string>
#include <random>

namespace SmartClinic {
    class IDGenerator {
    public:
        static std::string generatePatientId() {
            static std::random_device rd;
            static std::mt19937 gen(rd());
            static std::uniform_int_distribution<> dis(10000, 99999);
            return "PAT-" + std::to_string(dis(gen));
        }

        static std::string generateAppointmentId() {
            static std::random_device rd;
            static std::mt19937 gen(rd());
            static std::uniform_int_distribution<> dis(10000, 99999);
            return "APT-" + std::to_string(dis(gen));
        }
    };
}

#endif // IDGENERATOR_H