#ifndef UNDOMANAGER_H
#define UNDOMANAGER_H

#include <stack>
#include <functional>
#include <string>

namespace SmartClinic {
    struct UndoAction {
        std::string description;
        std::function<void()> undoFunction;
    };

    class UndoManager {
    private:
        std::stack<UndoAction> undoStack;

    public:
        void pushAction(const std::string& desc, std::function<void()> func) {
            undoStack.push({desc, func});
        }

        bool canUndo() const {
            return !undoStack.empty();
        }

        std::string popAndExecute() {
            if (undoStack.empty()) return "";
            UndoAction action = undoStack.top();
            undoStack.pop();
            action.undoFunction();
            return action.description;
        }

        void clear() {
            while (!undoStack.empty()) undoStack.pop();
        }
    };
}

#endif // UNDOMANAGER_H