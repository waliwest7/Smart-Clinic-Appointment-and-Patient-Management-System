#include <QApplication>
#include "gui/MainWindow.h"

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setStyle("Fusion");

    SmartClinic::MainWindow window;
    window.resize(1280, 800);
    window.show();

    return app.exec();
}