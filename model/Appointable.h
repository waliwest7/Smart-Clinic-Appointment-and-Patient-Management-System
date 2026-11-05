#ifndef APPOINTABLE_H
#define APPOINTABLE_H

#include <string>

namespace SmartClinic {
    class Appointable {
    public:
        virtual ~Appointable() = default;
        virtual bool canScheduleAppointment() const = 0;
        virtual std::string getSpecialInstructions() const = 0;
        virtual void scheduleAppointment() = 0;
        virtual void cancelAppointment() = 0;
    };
}

#endif // APPOINTABLE_H