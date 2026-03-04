# 🎯 FocusFlow

> A minimalist Pomodoro timer and task manager designed for focused, distraction-free productivity.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](setup.py)

---

## ✨ Features

- **⏱️ Customizable Pomodoro Timer**: 25-minute focused work sessions with 5-minute breaks
- **📝 Task Management**: Add, track, and manage your tasks with detailed descriptions
- **🎨 Smart Color Coding**: Color-coded UI themes for work sessions (red) and breaks (green)
- **🔔 Smart Notifications**: Pop-up alerts with audio cues when sessions change
- **🌓 Dark/Light Theme Support**: Automatic system theme detection
- **🎯 Distraction-Free UI**: Clean, modern interface focused on productivity

---

## 📸 Screenshots

The application features a professional two-pane interface:

- **Left Pane**: Task management with add/delete capabilities
- **Right Pane**: Study timer with real-time countdown and progress visualization

![FocusFlow Main Interface](./public/FocusFlow%20Image.png)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** or higher
- Windows, macOS, or Linux

### Installation Methods

#### Option 1: Using Python (Recommended for Development)

1. **Clone or download the repository**

   ```bash
   git clone https://github.com/SherryMaster/FocusFlow.git
   cd FocusFlow
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   ```
   - On Windows
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

#### Option 2: Windows Executable (Easiest for Users)

Download the latest `.exe` installer from the [releases page](https://github.com/SherryMaster/FocusFlow/releases), then run it to install FocusFlow as a desktop application. 

---

## 📖 Usage Guide

### Starting a Session

1. **Launch FocusFlow** - Run `python main.py` or open the installed application
2. **Add Tasks** (Optional) - Enter tasks in the left pane to stay organized
3. **Start Timer** - Click the **"▶ START"** button to begin your first focus session

### During a Session

- **Work Phase**: 25 minutes of focused time (displayed in red)
  - Stay focused and don't switch contexts
  - All your tasks remain visible on the left
- **Break Phase**: 5 minutes of rest (displayed in green)
  - The app will automatically notify you when it's time to break
  - Audio alert and pop-up window will appear

### Managing Tasks

- **Add a Task**: Type task name in the entry field and click "Add Task"
- **Add Description**: Optionally add a detailed description for your task
- **View Tasks**: Scroll through your task list in the left panel
- **Mark Complete**: Click the checkmark button next to a task to mark it complete
- **Delete a Task**: Click the delete button next to a task to remove it from the list

### Session Controls

| Button      | Action                           |
| ----------- | -------------------------------- |
| **▶ START** | Begin the current session        |
| **⏸ PAUSE** | Pause/resume the timer           |
| **↻ RESET** | Reset timer to original state    |

### Notifications

When transitioning between sessions, you'll receive:

- 🔔 Pop-up window with session information
- 🔊 Audio alert to grab your attention
- 🎨 Color-coded message (red for work, green for breaks)

---

## ⚙️ Customization for devs

### Adjusting Pomodoro Durations

Edit the following constants in `main.py`:

```python
POMODORO_WORK_DURATION = 25 * 60      # Work session duration in seconds
POMODORO_BREAK_DURATION = 5 * 60      # Break session duration in seconds
```

For example, for testing or preferences:

- Set to `5 * 60` for 5-minute sessions
- Set to `50 * 60` for 50-minute sessions

### Color Schemes

The app includes three customizable color schemes in `main.py`:

- `WORK_COLOR_SCHEME` - Colors for work sessions (vibrant red theme)
- `BREAK_COLOR_SCHEME` - Colors for break sessions (forest green theme)
- `DEFAULT_COLOR_SCHEME` - Colors for the main UI (ocean blue theme)

Each scheme includes:

- Background color
- Text colors (primary & secondary)
- Progress bar color
- Hover states

### Disabling Notifications

To disable pop-up notifications:

1. Look for `self.notifications_enabled = True` in `main.py`
2. Change to `self.notifications_enabled = False`
3. Restart the application

---

## 📁 Project Structure

```
FocusFlow/
├── main.py                 # Main application file with all GUI and logic
├── setup.py               # Python package setup configuration
├── requirements.txt       # Project dependencies
├── FocusFlow.iss          # Inno Setup configuration for Windows installer
├── assets/                # Logos and branding materials
│   ├── FocusFlow logo.png
│   ├── FocusFlow logo Green.png
│   ├── FocusFlow logo Red.png
│   └── [.ico files]
└── README.md              # This file
```

---

## 🛠️ Technologies & Dependencies

### Core Technologies

- **Python 3.10+** - Programming language
- **Tkinter** - GUI framework support
- **CustomTkinter** - Modern, beautiful Tkinter wrapper

### Dependencies

| Package           | Version | Purpose                |
| ----------------- | ------- | ---------------------- |
| **customtkinter** | 5.2.2   | Modern GUI components  |
| **darkdetect**    | 0.8.0   | System theme detection |
| **packaging**     | 26.0    | Version management     |

### Optional Dependencies (for building)

- **PyInstaller** - Convert Python to executable (.exe)
- **Inno Setup** - Create Windows installer (installed separately from https://jrsoftware.org/isinfo.php)

---

## 🤝 Contributing

Contributions are welcome! To contribute to FocusFlow:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution

- 🗂️ Persistent task storage (save/load from database)
- 📊 Statistics & productivity reports
- 🌍 Multi-language support
- 🔧 Additional customization options
- 📱 Mobile companion app
- 🎵 Custom notification sounds
- ⌨️ Keyboard shortcuts
- 🎯 Built-in productivity tips

---

**Happy focusing! 🎯**

_Track your tasks, manage your time, achieve your goals._
