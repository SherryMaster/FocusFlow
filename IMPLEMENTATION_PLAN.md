# FocusFlow — Complete Implementation Roadmap

**Project Status:** Phase 2 Complete (Window & UI Layout Ready)  
**Completion Timeline:** 4-7 focused days  
**Last Updated:** March 1, 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Environment Setup Checklist](#environment-setup-checklist)
3. [Current Project Status](#current-project-status)
4. [Phase-by-Phase Ladder](#phase-by-phase-ladder)
5. [Checkpoint Testing Guide](#checkpoint-testing-guide)
6. [Troubleshooting Reference](#troubleshooting-reference)

---

## Project Overview

### What is FocusFlow?

A dark-themed desktop productivity application that combines:

- **Task Manager**: Add, check off, and persist tasks
- **Pomodoro Timer**: 25-minute focused work sessions with 5-minute breaks
- **Dark UI**: Modern, distraction-free interface

### Core Requirements

✅ Add tasks dynamically  
✅ Mark tasks complete with checkboxes  
✅ Run non-blocking countdown timer  
✅ Persist tasks between app restarts  
✅ Responsive, freezing-free UI

### Tech Stack

| Component     | Version  | Purpose                |
| ------------- | -------- | ---------------------- |
| Python        | 3.10+    | Core language          |
| customtkinter | Latest   | Modern dark UI library |
| JSON          | Built-in | Task persistence       |
| Tkinter       | Built-in | UI framework base      |

---

## Environment Setup Checklist

### Prerequisites Verification

Run this command in Command Prompt to verify Python installation:

```bash
python --version
```

**Expected Output:** `Python 3.10.x` or higher

### Install Required Dependencies

Run in Command Prompt:

```bash
pip install customtkinter
```

### Verify Installation

Open Command Prompt and verify customtkinter is accessible:

```bash
python -c "import customtkinter; print('customtkinter imported successfully')"
```

**Expected Output:** `customtkinter imported successfully`

### Project Structure Status

```
e:\Projects\Python\FocusFlow\
├── main.py                 [✓ CREATED]
├── IMPLEMENTATION_PLAN.md  [✓ THIS FILE]
├── requirements.txt        [⏳ TODO: Phase 5]
├── tasks.json             [⏳ Auto-created: Phase 5]
└── assets/                [⏳ Optional: Future phases]
```

---

## Current Project Status

### What's Already Done (Phases 1-2)

Your `main.py` currently has:

- ✅ Window scaffolding with dark theme
- ✅ 750x480 window size
- ✅ Two-panel grid layout (tasks on left, timer on right)
- ✅ Task frame and timer frame configured

### What's Next (Phases 3-5)

| Phase       | Goal                           | Complexity | Est. Time |
| ----------- | ------------------------------ | ---------- | --------- |
| **Phase 3** | Task input & dynamic task list | Easy       | 1-2 hours |
| **Phase 4** | Pomodoro timer engine          | Medium     | 2-3 hours |
| **Phase 5** | Save/load tasks to JSON        | Easy       | 1 hour    |

---

## Phase-by-Phase Ladder

Follow this ladder step-by-step. Complete one phase before moving to the next.

---

### 🎯 PHASE 3: Task Manager Logic

**Goal:** Users can add unlimited tasks dynamically and see them in a scrollable list.

**Difficulty:** Easy  
**Time Estimate:** 1-2 hours  
**Checkpoint:** Add 3 tasks and verify they appear in the UI

---

#### Step 3.1: Add Task Input & Button Widgets

**What to do:** Add an entry field and "Add Task" button at the top of the task panel.

**Location:** Inside `__init__()`, after creating `self.task_frame`

**Code to add:**

```python
# Task input section
self.task_entry = ctk.CTkEntry(
    self.task_frame,
    placeholder_text="Enter a new task..."
)
self.task_entry.pack(padx=10, pady=10, fill="x")

self.add_btn = ctk.CTkButton(
    self.task_frame,
    text="Add Task",
    command=self.add_task
)
self.add_btn.pack(padx=10, pady=5)

# Initialize task storage
self.all_tasks = []
```

**Why this matters:**

- `CTkEntry`: Text input field for task names
- `CTkButton`: Clickable button that triggers `add_task()` function
- `command=self.add_task`: Connects button click to function
- `self.all_tasks`: List to store all task checkboxes

**Visual Result:** Entry box and button appear at top of left panel

**Common Mistake:**

- ❌ Forgetting `self.all_tasks = []` → later code crashes when trying to append
- ❌ Not using `pack()` → widgets don't appear

---

#### Step 3.2: Create Scrollable Task Container

**What to do:** Add a scrollable frame to hold unlimited tasks (scrolls when list gets long).

**Location:** Inside `__init__()`, after the button code from Step 3.1

**Code to add:**

```python
# Scrollable container for tasks
self.scroll_frame = ctk.CTkScrollableFrame(self.task_frame)
self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
```

**Why this matters:**

- `CTkScrollableFrame`: Automatically adds scrollbars when content exceeds window height
- `fill="both"`: Stretches horizontally AND vertically
- `expand=True`: Takes up all available space in task_frame

**Visual Result:** Empty scrollable area appears below the input button

**Common Mistake:**

- ❌ Using regular `CTkFrame` instead of `CTkScrollableFrame` → can't scroll (wastes space or hides tasks)
- ❌ Forgetting `expand=True` → scroll frame doesn't grow with window

---

#### Step 3.3: Implement `add_task()` Function

**What to do:** Create the function that runs when user clicks "Add Task".

**Location:** Inside the `FocusFlowApp` class, below `__init__()`

**Code to add:**

```python
def add_task(self):
    """Add a new task from user input"""
    text = self.task_entry.get().strip()

    # Validate: ignore empty input
    if not text:
        return

    # Create checkbox for this task
    checkbox = ctk.CTkCheckBox(self.scroll_frame, text=text)
    checkbox.pack(anchor="w", pady=2)

    # Track the checkbox
    self.all_tasks.append(checkbox)

    # Clear input field
    self.task_entry.delete(0, "end")
```

**Line-by-line explanation:**

| Code                               | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `self.task_entry.get().strip()`    | Get text from entry, remove spaces from edges |
| `if not text: return`              | Skip if empty (don't create blank tasks)      |
| `ctk.CTkCheckBox(...)`             | Create checkbox widget with task text         |
| `checkbox.pack(...)`               | Display checkbox in scroll frame              |
| `self.all_tasks.append(checkbox)`  | Save reference for later (Phase 5)            |
| `self.task_entry.delete(0, "end")` | Clear input field after task added            |

**Visual Result:**

1. Enter "Buy groceries" in input box
2. Click "Add Task"
3. Checkbox with text "Buy groceries" appears below
4. Input field clears

**Common Mistakes:**

- ❌ Forgetting `.strip()` → allows tasks that are just spaces
- ❌ Not clearing input field → confusing UX (user forgets they typed input)
- ❌ Not appending to `self.all_tasks` → can't save tasks later (Phase 5)

**Mini Checkpoint:**

```
✓ Can type in the entry field
✓ Clicking "Add Task" creates a checkbox
✓ Checkbox shows the text you entered
✓ Input field clears after adding task
✓ Can add multiple tasks (they stack vertically)
```

---

### ⏱️ PHASE 4: Pomodoro Timer Engine

**Goal:** Build a 25-minute countdown timer that doesn't freeze the UI.

**Difficulty:** Medium  
**Time Estimate:** 2-3 hours  
**Checkpoint:** Timer counts down smoothly from 25:00 to 00:00

**Critical Warning:** Never use `time.sleep()` or `while True` loops → freezes entire UI!

---

#### Step 4.1: Initialize Timer State Variables

**What to do:** Add variables to track timer state.

**Location:** Inside `__init__()`, after `self.all_tasks = []`

**Code to add:**

```python
# Timer state
self.time_left = 25 * 60  # 25 minutes in seconds
self.is_running = False
```

**Why this matters:**

- `time_left`: Tracks remaining seconds (1500 = 25 min × 60)
- `is_running`: Boolean flag to pause/resume without resetting

**Note:** Don't call timer functions yet — just initialize variables

---

#### Step 4.2: Create Timer Display UI

**What to do:** Add timer label and Start/Stop buttons to the timer panel.

**Location:** Inside `__init__()`, after the timer state variables (Step 4.1)

**Code to add:**

```python
# Timer display
self.timer_label = ctk.CTkLabel(
    self.timer_frame,
    text="25:00",
    font=("Arial", 48, "bold")
)
self.timer_label.pack(pady=40)

# Timer controls
self.start_btn = ctk.CTkButton(
    self.timer_frame,
    text="Start",
    command=self.start_timer
)
self.start_btn.pack(pady=10)

self.stop_btn = ctk.CTkButton(
    self.timer_frame,
    text="Stop",
    command=self.stop_timer
)
self.stop_btn.pack(pady=5)

self.reset_btn = ctk.CTkButton(
    self.timer_frame,
    text="Reset",
    command=self.reset_timer
)
self.reset_btn.pack(pady=5)
```

**Visual Result:**

- Large "25:00" text in center of right panel
- Three buttons below: Start, Stop, Reset

**Common Mistake:**

- ❌ Font size too small → hard to read during work sessions
- ❌ Forgetting `command=` parameter → buttons don't do anything when clicked

---

#### Step 4.3: Implement `start_timer()` Function

**What to do:** Start the countdown without freezing UI.

**Location:** Inside class, after `add_task()` method

**Code to add:**

```python
def start_timer(self):
    """Start the countdown timer"""
    if self.is_running:
        return  # Already running, ignore

    self.is_running = True
    self.update_timer()
```

**Why this matters:**

- `if self.is_running: return` → prevents multiple timers running simultaneously
- `self.is_running = True` → flag tells system timer is active
- `self.update_timer()` → kick off the countdown (see next step)

**Visual Result:** Clicking "Start" begins countdown

---

#### Step 4.4: Implement `update_timer()` Function — THE CORE TIMER LOGIC

**What to do:** Update timer display and schedule next update without freezing.

**Location:** Inside class, after `start_timer()` method

**Code to add:**

```python
def update_timer(self):
    """Update timer display and schedule next tick"""
    # Convert seconds to MM:SS format
    minutes = self.time_left // 60
    seconds = self.time_left % 60

    # Update label with formatted time
    self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    # If timer is still running and time remains
    if self.time_left > 0 and self.is_running:
        self.time_left -= 1
        # Schedule next update in 1000 milliseconds (1 second)
        self.after(1000, self.update_timer)
    else:
        # Timer finished
        self.is_running = False
```

**Critical Explanation — How `after()` Prevents Freezing:**

| Traditional (WRONG)                 | CustomTkinter (CORRECT)                       |
| ----------------------------------- | --------------------------------------------- |
| `time.sleep(1)` → blocks everything | `self.after(1000, ...)` → returns immediately |
| UI freezes for 1 second             | UI stays responsive                           |
| Other clicks don't register         | User can click buttons anytime                |

`self.after(1000, self.update_timer)` means: "In 1000ms, call this function again"

**Line-by-line breakdown:**

```python
minutes = self.time_left // 60        # 100 seconds → 1 minute
seconds = self.time_left % 60         # 100 seconds → 40 seconds
text=f"{minutes:02d}:{seconds:02d}"  # Formats as "01:40" (zero-padded)
```

**Example walkthrough (first 3 seconds):**

```
Initial: time_left = 1500 (25:00)

Call 1: Display "25:00", schedule call 2 for 1 second later
Call 2: time_left becomes 1499, display "24:59", schedule call 3
Call 3: time_left becomes 1498, display "24:58", schedule call 4
...continues until time_left = 0
```

**Mini Checkpoint:**

```
✓ Click Start → timer begins counting down
✓ Display updates every 1 second (no stuttering)
✓ Can still click buttons while timer runs
✓ Timer reaches 00:00
```

**Common Mistakes:**

- ❌ Using `time.sleep(1)` instead of `self.after()` → UI freezes completely
- ❌ Using `while True` loop → same freezing problem
- ❌ Not checking `self.is_running` → multiple timers run at once
- ❌ Forgetting `// 60` and `% 60` → math gives wrong display

---

#### Step 4.5: Implement Stop & Reset Functions

**What to do:** Add helper functions to pause and reset timer.

**Location:** Inside class, after `update_timer()`

**Code to add:**

```python
def stop_timer(self):
    """Pause the timer"""
    self.is_running = False

def reset_timer(self):
    """Reset timer to 25:00"""
    self.is_running = False
    self.time_left = 25 * 60
    self.timer_label.configure(text="25:00")
```

**Visual Result:**

- "Stop" button pauses timer (can click "Start" to resume)
- "Reset" button clears timer back to 25:00

**Common Mistake:**

- ❌ Forgetting `self.is_running = False` in stop → timer keeps running

---

### 💾 PHASE 5: Persistent Task Saving

**Goal:** Tasks remain even after closing and reopening the app.

**Difficulty:** Easy  
**Time Estimate:** 1 hour  
**Checkpoint:** Close app, reopen, tasks still there with same checkbox states

---

#### Step 5.1: Add Imports at Top of File

**What to do:** Import JSON library for saving/loading data.

**Location:** At the very top of `main.py`, after first line

**Current imports:**

```python
import customtkinter as ctk
```

**Add these imports:**

```python
import json
import os
```

**Full top section should look like:**

```python
import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
```

**Why this matters:**

- `json`: Convert Python lists/dictionaries to text format
- `os`: Check if file exists before reading

---

#### Step 5.2: Create `save_data()` Function

**What to do:** Save all tasks and their checkbox states to `tasks.json`.

**Location:** Inside class, after `reset_timer()`

**Code to add:**

```python
def save_data(self):
    """Save all tasks to tasks.json"""
    data = []

    # Extract info from each checkbox widget
    for task in self.all_tasks:
        task_info = {
            "text": task.cget("text"),      # Get the text of the checkbox
            "done": task.get()               # Get if checked (True/False)
        }
        data.append(task_info)

    # Write to file
    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ Saved {len(data)} tasks")
```

**What this creates (example):**

File: `tasks.json`

```json
[
	{
		"text": "Buy groceries",
		"done": false
	},
	{
		"text": "Call Mom",
		"done": true
	}
]
```

**Common Mistake:**

- ❌ Forgetting `.cget("text")` → can't extract text from checkbox

---

#### Step 5.3: Create `load_data()` Function

**What to do:** Load tasks from `tasks.json` when app starts.

**Location:** Inside class, after `save_data()`

**Code to add:**

```python
def load_data(self):
    """Load tasks from tasks.json"""
    # If file doesn't exist, nothing to load
    if not os.path.exists("tasks.json"):
        return

    # Read file
    with open("tasks.json", "r") as f:
        data = json.load(f)

    # Recreate each task
    for item in data:
        checkbox = ctk.CTkCheckBox(self.scroll_frame, text=item["text"])
        checkbox.pack(anchor="w", pady=2)

        # If task was marked done, check it
        if item["done"]:
            checkbox.select()

        self.all_tasks.append(checkbox)

    print(f"✓ Loaded {len(data)} tasks")
```

**Why this matters:**

- `os.path.exists()`: Prevents crash if file doesn't exist yet
- `checkbox.select()`: Programmatically check boxes for completed tasks
- Recreates exact state from last session

---

#### Step 5.4: Call Load at Startup

**What to do:** Load saved tasks when app opens.

**Location:** Inside `__init__()`, at the very end (last line before `mainloop()`)

**Code to add this line:**

```python
self.load_data()
```

**Full `__init__()` end should look like:**

```python
    # ... all other code ...

    self.reset_btn = ctk.CTkButton(...)
    self.reset_btn.pack(pady=5)

    self.load_data()  # ← ADD THIS LINE
```

---

#### Step 5.5: Call Save on Window Close

**What to do:** Automatically save tasks when user closes app.

**Location:** Inside `__init__()`, after `self.load_data()`

**Code to add:**

```python
# Save tasks when window closes
self.protocol("WM_DELETE_WINDOW", self.on_closing)

def on_closing(self):
    """Handle app closing"""
    self.save_data()
    self.destroy()
```

**Why this matters:**

- `protocol()`: Intercepts window close button
- `on_closing()`: Custom function runs before app actually closes
- `self.destroy()`: Properly close the application

**Mini Checkpoint:**

```
✓ Add some tasks
✓ Check off a few
✓ Close the app
✓ Reopen it
✓ Tasks are there with same checked states ← MAGIC!
```

---

#### Step 5.6: Create requirements.txt

**What to do:** Document project dependencies for easy reinstall.

**Location:** Create new file in same folder as `main.py`

**File name:** `requirements.txt`

**Content:**

```
customtkinter>=5.0.0
```

**Why this matters:**

- Other developers (or you on another PC) can run: `pip install -r requirements.txt`
- Ensures everyone has compatible versions

---

## Checkpoint Testing Guide

### Before Each Phase

1. **Open Command Prompt in project folder**

   ```bash
   cd e:\Projects\Python\FocusFlow
   python main.py
   ```

2. **Expected: App window opens and stays open**

3. **After each phase, verify the checkpoint below:**

---

### Phase 3 Checkpoint (Task Manager)

**Test this:**

1. Type "Test Task 1" in the entry field
2. Click "Add Task"
3. **✓ Checkbox appears with text "Test Task 1"**
4. **✓ Entry field is now empty**
5. Add 2-3 more tasks
6. **✓ All tasks stack vertically**
7. Scroll down (if list is long)
8. **✓ Scrollbar appears and works**

**If checkbox doesn't appear:**

- Check that `CTkScrollableFrame` is created
- Verify `self.add_task` function exists
- Check for Python errors in terminal

---

### Phase 4 Checkpoint (Timer)

**Test this:**

1. **Display:** Large "25:00" appears on right side
2. Click "Start" button
3. **✓ Display changes to "24:59" after 1 second**
4. **✓ Counting happens smoothly (1 sec per update)**
5. **✓ Can still click buttons while timer runs**
6. Click "Stop" button
7. **✓ Timer pauses (stops counting)**
8. Click "Start" again
9. **✓ Timer resumes from where it stopped**
10. Click "Reset" button
11. **✓ Display goes back to "25:00"**
12. Let timer run all the way to "00:00"
13. **✓ Timer stops at 0 (doesn't go negative)**

**If timer freezes UI:**

- You're probably using `time.sleep()` somewhere
- Replace with `self.after()`

**If display doesn't update:**

- Check that `update_timer()` is being called
- Verify `self.time_left` variable exists

---

### Phase 5 Checkpoint (Persistence)

**Test this:**

1. Add 3 tasks: "Learn Python", "Exercise", "Rest"
2. Check off "Exercise"
3. Click the X to close the app
4. **✓ Tasks were saved (terminal shows "✓ Saved 3 tasks")**
5. Run `python main.py` again
6. **✓ "Learn Python" appears (unchecked)**
7. **✓ "Exercise" appears (checked)**
8. **✓ "Rest" appears (unchecked)**
9. Open `tasks.json` in text editor
10. **✓ File contains JSON data with tasks**

**If tasks don't load:**

- Check that `load_data()` is called in `__init__()`
- Verify `tasks.json` file actually exists
- Look for error messages in terminal

---

## Troubleshooting Reference

### Common Problems & Solutions

#### Problem: "No module named 'customtkinter'"

**Cause:** Plugin not installed  
**Solution:**

```bash
pip install customtkinter
```

**Verify:**

```bash
python -c "import customtkinter; print('OK')"
```

---

#### Problem: Window opens then closes immediately

**Cause:** Missing `app.mainloop()`  
**Solution:** Check end of file has:

```python
if __name__ == "__main__":
    app = FocusFlowApp()
    app.mainloop()  # ← MUST be here
```

---

#### Problem: Buttons don't work when clicked

**Cause:** Forgot `command=function_name` parameter  
**Example WRONG:**

```python
button = ctk.CTkButton(frame, text="Click me")  # No command!
```

**Example CORRECT:**

```python
button = ctk.CTkButton(frame, text="Click me", command=self.add_task)
```

---

#### Problem: Timer display shows wrong time format

**Cause:** Missing zero-padding in format string  
**WRONG:**

```python
text=f"{minutes}:{seconds}"  # Shows "1:5" instead of "01:05"
```

**CORRECT:**

```python
text=f"{minutes:02d}:{seconds:02d}"  # Shows "01:05"
```

---

#### Problem: Timer freezes the entire UI

**Cause:** Using `time.sleep()` instead of `self.after()`  
**WRONG:**

```python
import time
while True:
    time.sleep(1)  # ← NEVER DO THIS
```

**CORRECT:**

```python
self.after(1000, self.update_timer)  # ← USE THIS
```

---

#### Problem: Tasks disappear after closing app

**Cause:** Missing `save_data()` call on close  
**Solution:** Verify in `__init__()` you have:

```python
self.protocol("WM_DELETE_WINDOW", self.on_closing)
```

And your `on_closing()` function calls `self.save_data()`

---

#### Problem: Terminal shows errors with JSON

**Cause:** Usually a malformed `tasks.json` file  
**Solution:**

1. Delete `tasks.json` file
2. Restart app (fresh save)

Or verify it's valid JSON:

```bash
python -c "import json; json.load(open('tasks.json'))"
```

---

## Development Best Practices

### After Every Step: Test Your Work

```bash
python main.py
```

Don't code 5 steps ahead and test once. Test after every single step.

### Debug Using `print()` Statements

When something doesn't work:

```python
def add_task(self):
    text = self.task_entry.get().strip()
    print(f"DEBUG: User entered: '{text}'")  # ← Add this
    if not text:
        return
    print(f"DEBUG: Creating checkbox for: {text}")  # ← And this
    # ... rest of code
```

Run app and look at terminal for debug messages.

### Keep Backups After Major Milestones

After each phase works:

```bash
copy main.py main.py.backup_phase3
```

If you break something, you can quickly revert.

### Reading Error Messages

When Python crashes, read the error backwards:

```
Traceback (most recent call last):
  File "main.py", line 45, in add_task
    self.all_tasks.append(checkbox)
AttributeError: 'FocusFlowApp' has no attribute 'all_tasks'
                                            ↑ The actual problem
```

This means: You forgot to initialize `self.all_tasks = []` in `__init__()`

---

## Code Organization Checklist

Your final `main.py` should have this structure:

```python
import customtkinter as ctk  ← Phase 5
import json                   ← Phase 5
import os                     ← Phase 5

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FocusFlowApp(ctk.CTk):
    def __init__(self):
        # Window setup (Phase 1)
        # Grid configuration (Phase 2)
        # Task widgets (Phase 3)
        # Timer widgets (Phase 4)
        # Persistence setup (Phase 5)
        self.load_data()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):              ← Phase 3
        # Implementation

    def start_timer(self):           ← Phase 4
        # Implementation

    def stop_timer(self):            ← Phase 4
        # Implementation

    def reset_timer(self):           ← Phase 4
        # Implementation

    def update_timer(self):          ← Phase 4 (CRITICAL)
        # Implementation

    def save_data(self):             ← Phase 5
        # Implementation

    def load_data(self):             ← Phase 5
        # Implementation

    def on_closing(self):            ← Phase 5
        # Implementation

if __name__ == "__main__":
    app = FocusFlowApp()
    app.mainloop()
```

---

## Success Criteria — Project Complete When:

✅ App opens in dark mode  
✅ Can add unlimited tasks  
✅ Tasks appear as checkboxes in scrollable list  
✅ Can check/uncheck tasks  
✅ Timer displays 25:00 and counts down smoothly  
✅ Timer doesn't freeze UI  
✅ Stop/Reset buttons work  
✅ Closing app saves tasks  
✅ Opening app reloads saved tasks  
✅ No crashes or error messages

---

## Next Steps After Completion (Optional)

Once FocusFlow is fully working, consider:

- Add 5-minute break timer after work session
- Add task delete button
- Add sound notification when timer ends
- Customize colors or fonts
- Share on GitHub

---

**Remember:** Build confidence by testing after EVERY small change. This is how professionals work. Slow and steady wins the race. 🎯

Good luck! You've got this! 💪
