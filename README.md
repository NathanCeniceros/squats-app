# squats-app
app to encourage and keep track of squats every 45 minutes throughout the day 
Here’s the README file presented in a simple, copyable format:

---

# Squats Reminder App 🏋️‍♀️

## New Features
- **Snooze Reminders**: Users can now snooze reminders for 5 minutes.
- **Improved Error Handling**: The app gracefully handles missing or corrupted tracker files.

## Overview
The **Squats Reminder App** is a dynamic fitness tool designed to keep you active throughout your day by providing periodic reminders to perform squats. It tracks your progress and motivates you with encouraging messages as you complete each set. Whether you're working, studying, or relaxing, this app ensures you stay active and engaged in your fitness routine.

## Features
### 🕐 **Time Slot Tracking**
- The app divides the day into predefined time slots (e.g., 8:00 AM, 8:45 AM, etc.).
- Tracks whether squats have been completed for each time slot.
- Automatically marks missed slots based on the current time.

### 🎯 **Progress Tracker**
- Displays a progress bar to visually track your daily squat completion.
- Updates dynamically as you complete or undo sets.

### 🚀 **Undo Feature**
- Allows you to undo completed time slots in case of accidental clicks, ensuring accurate tracking.

### 👏 **Motivational Messages**
- Shows a congratulatory pop-up after completing each set, boosting motivation with random encouraging messages.

### 📖 **Persistent Tracking**
- Saves progress to a file (`squats_tracker.txt`) to ensure continuity across sessions.
- Logs all activities (e.g., completed, skipped, undone actions) to `squats_log.txt`.

### 🖥️ **User-Friendly Interface**
- Simple, clean design powered by `tkinter`.
- Auto-adjusts to fit content dynamically for intuitive usability.

### ⏱️ **Reminder Pop-Ups**
- Periodic reminders appear with specific time slot details to prompt squat completion.
- Includes options to mark the set as complete or skip.

## Requirements
- Python 3.x
- Libraries:
  - `tkinter` (standard GUI library)
  - `random`
  - `datetime`
  - `threading`

## Installation
1. **Clone or Download**:
   - Clone the repository or download the source code.
   ```
   git clone https://github.com/your-repo/squats-reminder.git
   ```
   
2. **Install Python**:
   - Ensure Python 3.x is installed on your system.

3. **Run the Script**:
   - Navigate to the project folder and execute:
     ```
     python squats.py
     ```

4. **Optional: Create an Executable**:
   - Use `PyInstaller` to generate a standalone `.exe` file:
     ```
     pyinstaller --onefile --noconsole --icon=squat-icon.ico squats.py
     ```

## Usage
1. Launch the app:
   - Open the Python script or `.exe` file.

2. Interact with the tracker:
   - View missed, completed, and upcoming time slots.
   - Click on time slots to mark them as completed or undo an action.

3. Complete your squats:
   - Follow pop-up reminders and update progress after each set.

4. Stay motivated:
   - Enjoy the congratulatory messages for reaching fitness milestones.

## Files Created
- **`squats_tracker.txt`**:
  - Records daily squat progress for each time slot.
- **`squats_log.txt`**:
  - Logs all user activity and app events (e.g., completed sets, skipped actions).

## Known Issues & Troubleshooting
- **No GUI on startup**:
  - Run the script in the command prompt to check for errors.
  - Ensure tkinter is installed and supported.

- **Logs or tracker file not created**:
  - Check write permissions for the directory.
  - Ensure the paths are correct and writable.

- **Time issues**:
  - Verify your system's clock and time zone settings.

## Future Enhancements
- Add customizable time slots.
- Enable notifications on multiple devices.
- Include additional fitness exercises.

## Contributors
- **Nathan Ceniceros with lots of AI help**: Developer & Designer



---

