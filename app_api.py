import pyautogui
import time

# prompts you want to send
prompts = [
    "Write a short story about a robot learning emotions.",
    "Explain quantum computing in simple words.",
    "Give 5 startup ideas using AI."
]

print("You have 5 seconds to click inside the Meta AI prompt box...")

# wait so you can focus the app
time.sleep(5)

for prompt in prompts:

    # type prompt
    pyautogui.write(prompt, interval=0.02)

    # press enter
    pyautogui.press("enter")

    print("Sent:", prompt)

    # wait for response before next prompt
    time.sleep(12)

print("Done sending prompts.")