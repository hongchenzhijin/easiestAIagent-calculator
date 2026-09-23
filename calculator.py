import time
import re

from pywinauto import Desktop
import pyautogui


def use_calculator(expression):
    """
    Open Windows Calculator, perform the expression,
    read the displayed result, and return it.
    """

    print(f"[TOOL] Calculator: {expression}")

    # Security: only allow basic arithmetic characters
    if not re.fullmatch(r"[0-9+\-*/().% ]+", expression):
        return "Error: unsupported characters in expression."

    # Open Windows Calculator
    pyautogui.hotkey("win", "r")
    time.sleep(0.7)

    pyautogui.write("calc")
    pyautogui.press("enter")

    time.sleep(2)

    # Find Calculator windows
    calculators = Desktop(
        backend="uia"
    ).windows(
        title="Calculator",
        class_name="ApplicationFrameWindow",
        top_level_only=True
    )

    if not calculators:
        return "Error: Windows Calculator could not be found."

    # Use the newest Calculator window
    calculator = calculators[-1]

    calculator.set_focus()

    time.sleep(0.5)

    # Enter expression
    pyautogui.write(expression)
    pyautogui.press("enter")

    time.sleep(1)

    # Read result from Calculator UI
    for control in calculator.descendants():

        try:
            name = control.element_info.name

            if name.startswith("Display is "):

                result = name[len("Display is "):]

                print(f"[TOOL] Result: {result}")

                return result

        except Exception:
            pass

    return "Error: Could not read the Calculator result."