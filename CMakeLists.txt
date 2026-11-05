cmake_minimum_required(VERSION 3.16)
project(SmartClinicSystem LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

set(PROJECT_SOURCES
    main.cpp
    model/ClinicException.h
    model/Appointable.h
    model/PatientRecord.h
    model/PatientRecord.cpp
    model/GeneralPatient.h
    model/GeneralPatient.cpp
    model/EmergencyPatient.h
    model/EmergencyPatient.cpp
    model/FollowUpPatient.h
    model/FollowUpPatient.cpp
    model/Appointment.h
    model/Appointment.cpp
    controller/ClinicDatabase.h
    controller/ClinicDatabase.cpp
    controller/SearchEngine.h
    controller/AppointmentController.h
    utils/IDGenerator.h
    utils/UndoManager.h
    utils/FileHandler.h
    gui/DashboardPanel.h
    gui/DashboardPanel.cpp
    gui/PatientPanel.h
    gui/PatientPanel.cpp
    gui/AppointmentPanel.h
    gui/AppointmentPanel.cpp
    gui/QueuePanel.h
    gui/QueuePanel.cpp
    gui/SearchPanel.h
    gui/SearchPanel.cpp
    gui/ReportsPanel.h
    gui/ReportsPanel.cpp
    gui/MainWindow.h
    gui/MainWindow.cpp
)

add_executable(SmartClinicSystem ${PROJECT_SOURCES})
target_link_libraries(SmartClinicSystem PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)