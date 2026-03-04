import customtkinter as ctk
import time
import json
import os
import winsound
import tkinter as tk

ctk.set_appearance_mode("system")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")

# Pomodoro durations in seconds (for testing, you can set these to shorter times like 5 seconds for work and 5 seconds for break)
POMODORO_WORK_DURATION = 25 * 60  # 25 minutes in seconds
POMODORO_BREAK_DURATION = 5 * 60  # 5 minutes in seconds

WORK_COLOR_SCHEME = {
    "bg_color": ("#E63946", "#E63946"),  # Background color for work sessions (vibrant red)
    "text_color": ("#FF6B6B", "#FF6B6B"),  # Primary text color for work sessions (bright red)
    "primary_text": ("#F77F88", "#F77F88"),  # Primary text color for work sessions (redish pink)
    "secondary_text": ("#F0F0F0", "#F0F0F0"),  # Secondary text color for work sessions (light gray)
    "progress_color": ("#F77F88", "#F77F88"),  # Progress bar color for work sessions (coral red)
    "hover_color": ("#D62828", "#D62828")  # Hover color for work session buttons (darker red)
}

BREAK_COLOR_SCHEME = {
    "bg_color": ("#06A77D", "#06A77D"),  # Background color for break sessions (forest green)
    "text_color": ("#52B788", "#52B788"),  # Primary text color for break sessions (sage green)
    "primary_text": ("#06D584", "#06D584"),  # Primary text color for break sessions (bright green)
    "secondary_text": ("#E0F5F0", "#E0F5F0"),  # Secondary text color for break sessions (very light teal)
    "progress_color": ("#52B788", "#52B788"),  # Progress bar color for break sessions (sage green)
    "hover_color": ("#048659", "#048659")  # Hover color for break session buttons (darker green)
}

DEFAULT_COLOR_SCHEME = {
    "bg_color": ("#0077B6", "#0077B6"),  # Background color for normal sessions (ocean blue)
    "text_color": ("#00B4D8", "#00B4D8"),  # Primary text color for normal sessions (sky blue)
    "primary_text": ("#0096C7", "#0096C7"),  # Primary text color for normal sessions (medium blue)
    "secondary_text": ("#E0F4FF", "#E0F4FF"),  # Secondary text color for normal sessions (light blue)
    "progress_color": ("#00B4D8", "#00B4D8"),  # Progress bar color for normal sessions (sky blue)
    "hover_color": ("#005A87", "#005A87")  # Hover color for normal session buttons (darker blue)
}

class NotificationHandler:
    def __init__(self, app: FocusFlowApp):
        # Store app reference to allow sending notifications through the app's UI
        self.app = app

    def notify_session_change(self, old_session, new_session, cycle):
        
        if not self._should_show_notifications():
            return # If the logic determines that we should not show notifications (e.g., based on user settings), we return early and do not proceed with showing a notification for the session change
        
        # prepare session info dict
        session_info = {
            "old": old_session,
            "new": new_session,
            "cycle": cycle,
            "total_cycles": self.app.total_cycles
        }
        
        self._bring_window_to_focus()
        self._create_popup_window(session_info)
    
    def _should_show_notifications(self):
        return self.app.notifications_enabled # Check the notifications_enabled flag in the main application to determine whether notifications should be shown. This allows the user to toggle notifications on or off, and this method centralizes that logic for easy checking before showing any notification.
    
    def _create_popup_window(self, session_info):
        old_session = session_info["old"]
        new_session = session_info["new"]
        cycle = session_info["cycle"]
        total_cycles = session_info["total_cycles"]
        
        if new_session == "break":
            title = "Time for a Break!" # Title for the notification when transitioning to a break session
            message = f"Work Session Completed. Take a short break!\nCurrent Cycle: {cycle}/{total_cycles}" # Message for the notification when transitioning to a break session, including the current cycle and total cycles
            color_scheme = BREAK_COLOR_SCHEME # Use the break color scheme for the notification when transitioning to a break session
        elif new_session == "work":
            title = "Back to Work!" # Title for the notification when transitioning to a work session
            message = f"Cycle {cycle} of {total_cycles} starting now. Focus up!" # Message for the notification when transitioning to a work session, including the current cycle and total cycles
            color_scheme = WORK_COLOR_SCHEME # Use the work color scheme for the notification when transitioning to a work session
        elif new_session == "complete":
            title = "Session Complete!" # Title for the notification when the entire Pomodoro session is complete
            message = f"Congratulations! You've completed all {total_cycles} cycles. Take a well-deserved break!" # Message for the notification when the entire Pomodoro session is complete, including the total number of cycles completed
            color_scheme = WORK_COLOR_SCHEME # Use the work color scheme for the notification when the session is complete, as it's a celebratory message related to completing the work sessions
        else:
            return # If the new session type is not recognized, we return early and do not create a notification
        
        popup = ctk.CTkToplevel(self.app) # Create a new top-level window (popup) that is a child of the main application window (self.app) to display the notification message
        popup.title("FocusFlow Alert!") # Set the title of the popup window to the appropriate title based on the session change
        popup.geometry("400x200") # Set the size of the popup window to 400 pixels wide and 200 pixels tall
        
        popup.attributes("-topmost", True) # Make the popup window stay on top of all other windows to ensure it is visible to the user when it appears
        
        # Center the popup on screen
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        title_label = ctk.CTkLabel(popup, text=title, font=("Arial", 16, "bold"), text_color=color_scheme["primary_text"]) # Create a label widget for the title of the notification, with the appropriate title text and styling based on the session change. This label is a child of the popup window (popup).
        title_label.pack(pady=(20, 10)) # Pack the title label into the popup window with vertical padding of 20 pixels on top and 10 pixels on the bottom (pady=(20, 10)).
        
        message_label = ctk.CTkLabel(popup, text=message, font=("Arial", 12), text_color=color_scheme["secondary_text"]) # Create a label widget for the message of the notification, with the appropriate message text and styling based on the session change. This label is a child of the popup window (popup).
        message_label.pack(pady=(0, 20)) # Pack the message label into the popup window with vertical padding of 0 pixels on top and 20 pixels on the bottom (pady=(0, 20)).
        
        if new_session != "complete":
            cycle_label = ctk.CTkLabel(popup, text=f"Cycle {cycle} of {total_cycles}", font=("Arial", 10), text_color=color_scheme["secondary_text"]) # Create a label widget to display the current cycle count relative to the total number of cycles (e.g., "Cycle 1 of 4"), with appropriate styling based on the session change. This label is only created if the new session is not "complete", as it is relevant for work and break session changes but not for the completion notification. This label is a child of the popup window (popup).
            cycle_label.pack(pady=(0, 10)) # Pack the cycle label into the popup window with vertical padding of 0 pixels on top and 10 pixels on the bottom (pady=(0, 10)).
        
        ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy, width=80, fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"]) # Create a button widget with the text "OK" that destroys the popup window when clicked. The button has a fixed width of 80 pixels and styling based on the session change. This button is a child of the popup window (popup).
        ok_button.pack(pady=(0, 10)) # Pack the ok button into the popup window with vertical padding of 0 pixels on top and 10 pixels on the bottom (pady=(0, 10)).
        
        popup.grab_set() # Grab the focus to the popup window to ensure that the user interacts with it before returning to the main application window, which is important for acknowledging the session change notification.
        popup.focus_force() # Force focus on the popup window to ensure it is active and ready for user interaction when it appears, which helps ensure that the notification is seen and acknowledged by the user.
        
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Play a system sound (exclamation) to alert the user when the notification popup appears, providing an auditory cue in addition to the visual notification to help ensure that the user notices the session change.

    def _bring_window_to_focus(self):
        try:
            self.app.deiconify() # Restore the window if it is minimized
            self.app.lift() # Bring the window to the front
            self.app.focus_force() # Force focus on the window
            
        except Exception as e:
            print(f"Error bringing window to focus: {e}") # Log any exceptions that occur while trying to bring the window to focus, which can help with debugging issues related to notifications not appearing correctly
            try:
                self.app.update()
                self.app.state('normal')
                self.app.attributes('-topmost', 1)
                self.app.attributes('-topmost', 0)
            except:
                pass

class FocusFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__() # Initialize the parent class (CTk) to set up the main application window
        self.title("FocusFlow") # Set the title of the application window to "FocusFlow"
        self.geometry("750x480") # Set the initial size of the application window to 750 pixels wide and 480 pixels tall
        
        self.grid_columnconfigure(0, weight=1) # Configure the grid layout of the main window to have two columns, with the first column (index 0) having a weight of 1 (expandable)
        self.grid_columnconfigure(1, weight=1) # Configure the second column (index 1) to also have a weight of 1, allowing it to expand equally with the first column
        self.grid_rowconfigure(0, weight=1) # Configure the single row (index 0) to have a weight of 1, allowing it to expand vertically to fill the available space
        
        # Timer state variables
        self.timer_job = None # Variable to hold the reference to the scheduled timer update job, initialized to None (no job scheduled)
        self.next_tick_at = None # Variable to track the scheduled time for the next timer tick, initialized to None (no tick scheduled)
        self.tick_interval_ms = 1000 # Timer tick interval in milliseconds (1000 ms = 1 second)
        self.remaining_to_next_tick_ms = self.tick_interval_ms # Variable to track the remaining time in milliseconds until the next timer tick, initialized to the full tick interval (1000 ms)
        
        self.all_tasks = [] # List to hold all Task objects created in the application, initialized as an empty list
        self.is_timer_running = False # Boolean flag to track whether the timer is currently running, initialized to False (timer is not running)
        self.is_pomodoro_active = False # Boolean flag to track whether a Pomodoro session is currently active, initialized to False (no Pomodoro session is active)
        self.progress_mode = "completed" # Variable to track the current mode of the progress bar, initialized to "completed" (indicating that the progress bar will show completed time by default) - can be toggled to "remaining" to show remaining time instead
        
        # Pomodoro session tracking variables
        self.current_cycle = 1 # Variable to track the current Pomodoro cycle, initialized to 1 (starting with the first cycle)
        self.total_cycles = 4 # Total number of Pomodoro cycles to complete, set to 4 (default for a standard Pomodoro session)
        self.is_work_session = True # Boolean flag to track whether the current session is a work session (True) or a break session (False), initialized to True (starting with a work session)
        
        self.notification_handler = NotificationHandler(self) # Create an instance of the NotificationHandler class, passing a reference to the main application (self) to allow it to send notifications through the app's UI. This handler will be responsible for managing notifications related to session changes and other events in the application.
        self.notifications_enabled = True # Boolean flag to track whether notifications are enabled, initialized to True (notifications will be shown by default)
        
        # Get initial duration
        self.time_left = self.get_current_duration() # Variable to track the remaining time in seconds for the current session, initialized by calling the get_current_duration method which returns the appropriate duration based on whether it's a work or break session
        self.current_session_total_duration = self.time_left # Variable to store the total duration of the current session, initialized to the same value as time_left for reference when calculating progress
        self.progress_ratio = 0 if self.progress_mode == "completed" else 1 # Variable to track the current progress ratio for the progress bar, initialized to 0 if showing completed time (indicating no progress at the start) or 1 if showing remaining time (indicating full time remaining at the start)
        
        ## UI Setup ##
        # Create two main frames: one for tasks and one for the timer, arranged side by side in the grid layout of the main window
        
        # Task Frame
        self.task_frame = ctk.CTkFrame(self) # Create a frame for the task management section of the application, which will contain the task entry, add button, and the list of tasks. This frame is a child of the main application window (self).
        self.task_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Place the task frame in the grid at row 0, column 0, and make it expand to fill the available space in both directions (sticky="nsew"). Add padding of 10 pixels on all sides (padx=10, pady=10).
        
        # Timer Frame
        self.timer_frame = ctk.CTkFrame(self) # Create a frame for the timer section of the application, which will contain the timer display, control buttons, and session information. This frame is also a child of the main application window (self).
        self.timer_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10) # Place the timer frame in the grid at row 0, column 1, and make it expand to fill the available space in both directions (sticky="nsew"). Add padding of 10 pixels on all sides (padx=10, pady=10).
        
        # -- TASK FRAME --
        # Title
        self.task_title = ctk.CTkLabel(
            self.task_frame,
            text="Task List",
            font=("Arial", 18, "bold")
        ) # Create a label widget for the title of the task section, with the text "Task List" and a bold Arial font of size 18. This label is a child of the task frame (self.task_frame).
        self.task_title.pack(pady=(10, 0)) # Pack the task title label into the task frame with vertical padding of 10 pixels on top and 0 pixels on the bottom (pady=(10, 0)).

        # Task input section
        input_frame = ctk.CTkFrame(self.task_frame) # Create a frame to hold the task input entry and add button, which will be placed below the title in the task frame. This frame is a child of the task frame (self.task_frame).
        input_frame.pack(pady=10, padx=10, fill="x") # Pack the input frame into the task frame with padding of 10 pixels on all sides (pady=10, padx=10) and make it fill horizontally (fill="x").
        
        input_frame.grid_columnconfigure(0, weight=2) # Configure the grid layout of the input frame to have two columns, with the first column (index 0) having a weight of 2 (taking up more space for the entry)...
        input_frame.grid_columnconfigure(1, weight=1) # ...and the second column (index 1) having a weight of 1 (taking up less space for the button).
        
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter a new task") # Create an entry widget for the user to input a new task, with placeholder text "Enter a new task". This entry is a child of the input frame (input_frame).
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5)) # Place the task entry in the grid at row 0, column 0 of the input frame, make it expand horizontally (sticky="ew"), and add padding of 5 pixels to the right (padx=(0, 5)).
        
        self.add_task_button = ctk.CTkButton(input_frame, text="Add Task", command=self.add_task) # Create a button widget with the text "Add Task" that calls the add_task method when clicked. This button is a child of the input frame (input_frame).
        self.add_task_button.grid(row=0, column=1, sticky="ew") # Place the add task button in the grid at row 0, column 1 of the input frame and make it expand horizontally (sticky="ew").
        
        self.task_description = ctk.CTkEntry(input_frame, placeholder_text="Task Description (optional)") # Create another entry widget for the user to input an optional description for the task, with placeholder text "Task Description (optional)". This entry is also a child of the input frame (input_frame).
        self.task_description.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0)) # Place the task description entry in the grid at row 1, column 0 of the input frame, spanning both columns (columnspan=2), make it expand horizontally (sticky="ew"), and add vertical padding of 5 pixels on top (pady=(5, 0)).
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.task_frame) # Create a scrollable frame to hold the list of tasks, which will allow the user to scroll through their tasks if they exceed the visible area. This scrollable frame is a child of the task frame (self.task_frame).
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True) # Pack the scrollable frame into the task frame with padding of 10 pixels on all sides (pady=10, padx=10), make it fill both horizontally and vertically (fill="both"), and allow it to expand to fill any remaining space (expand=True).
        
        # -- TIMER FRAME --
        # Title
        self.timer_title = ctk.CTkLabel(
            self.timer_frame,
            text="Study Timer",
            font=("Arial", 18, "bold")
        ) # Create a label widget for the title of the timer section, with the text "Study Timer" and a bold Arial font of size 18. This label is a child of the timer frame (self.timer_frame).
        self.timer_title.pack(pady=(10, 20)) # Pack the timer title label into the timer frame with vertical padding of 10 pixels on top and 20 pixels on the bottom (pady=(10, 20)).

        # Timer display frame
        timer_display_frame = ctk.CTkFrame(
            self.timer_frame,
            fg_color=("gray20", "gray20"),
            corner_radius=500
        ) # Create a frame to hold the timer display, with a foreground color of gray20 and a large corner radius to make it circular. This frame is a child of the timer frame (self.timer_frame).
        timer_display_frame.pack(pady=20, padx=20, fill="both", expand=True) # Pack the timer display frame into the timer frame with padding of 20 pixels on all sides (pady=20, padx=20), make it fill both horizontally and vertically (fill="both"), and allow it to expand to fill any remaining space (expand=True).
        
        self.center_container = ctk.CTkFrame(timer_display_frame, fg_color="transparent") # Create a transparent frame to center the timer label and progress bar within the timer display frame. This frame is a child of the timer display frame (timer_display_frame).
        self.center_container.pack(expand=True) # Pack the center container frame into the timer display frame and allow it to expand to fill the available space, which will help center its contents (the timer label and progress bar).
        
        self.timer_label = ctk.CTkLabel(
            self.center_container,
            text=f"{self.time_left // 60:02d}:{self.time_left % 60:02d}",
            font=("Arial", 64, "bold"),
            text_color=("#00B4D8", "#00B4D8")
        ) # Create a label widget to display the timer countdown, with the initial text formatted as MM:SS based on the time_left variable. The font is set to a bold Arial font of size 64, and the text color is set to a specific shade of blue (#00B4D8). This label is a child of the center container frame (self.center_container).
        self.timer_label.pack(pady=(40, 0)) # Pack the timer label into the center container frame with vertical padding of 40 pixels on top and 0 pixels on the bottom (pady=(40, 0)).

        self.timer_progress_bar = ctk.CTkProgressBar(self.center_container, width=200, height=5) # Create a progress bar widget to visually represent the remaining time in the current session, with a width of 200 pixels and a height of 5 pixels. This progress bar is a child of the center container frame (self.center_container).
        self.timer_progress_bar.set(self.progress_ratio) # Set the initial value of the timer progress bar to the current progress ratio (which is initialized to 0, indicating no progress at the start).
        self.timer_progress_bar.pack() # Pack the timer progress bar into the center container frame with vertical padding of 5 pixels on top and 40 pixels on the bottom (pady=(5, 40)), which will position it below the timer label and add spacing around it.
        
        self.progress_mode_label = ctk.CTkLabel(
            self.center_container,
            text=f"Progress Mode: {self.progress_mode.title()}",
            font=("Arial", 10),
            text_color="gray"
        ) # Create a label widget to indicate the current mode of the progress bar (showing completed time), with the text "Progress Mode: Completed", an Arial font of size 10, and gray text color. This label is a child of the center container frame (self.center_container).
        self.progress_mode_label.pack() # Pack the progress mode label into the center container frame with vertical padding of 0 pixels on top and 10 pixels on the bottom (pady=(0, 10)), placing it below the progress bar.

        # Button controls frame
        buttons_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent") # Create a frame to hold the timer control buttons (start, pause, reset), with a transparent background color. This frame is a child of the timer frame (self.timer_frame).
        buttons_frame.pack(pady=15, padx=10, fill="x") # Pack the buttons frame into the timer frame with vertical padding of 15 pixels and horizontal padding of 10 pixels (pady=15, padx=10), and make it fill horizontally (fill="x").
        
        buttons_frame.grid_columnconfigure(0, weight=1) # Configure the grid layout of the buttons frame to have three columns, with the first column (index 0) having a weight of 1 (taking up equal space for the start button)...
        buttons_frame.grid_columnconfigure(1, weight=1) # ...the second column (index 1) having a weight of 1 (taking up equal space for the pause button)...
        buttons_frame.grid_columnconfigure(2, weight=1) # ...and the third column (index 2) having a weight of 1 (taking up equal space for the reset button), ensuring that all buttons are evenly spaced across the width of the buttons frame.

        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶ START",
            command=self.start_timer,
            font=("Arial", 12, "bold"),
            width=80
        ) # Create a button widget with the text "▶ START" that calls the start_timer method when clicked. The button has a bold Arial font of size 12 and a fixed width of 80 pixels. This button is a child of the buttons frame (buttons_frame).
        self.start_btn.grid(row=0, column=0, padx=5) # Place the start button in the grid at row 0, column 0 of the buttons frame and add horizontal padding of 5 pixels (padx=5).

        self.pause_btn = ctk.CTkButton(
            buttons_frame,
            text="⏸ PAUSE",
            command=self.stop_timer,
            font=("Arial", 12, "bold"),
            width=80
        ) # Create a button widget with the text "⏸ PAUSE" that calls the stop_timer method when clicked. The button has a bold Arial font of size 12 and a fixed width of 80 pixels. This button is a child of the buttons frame (buttons_frame).
        self.pause_btn.grid(row=0, column=1, padx=5) # Place the pause button in the grid at row 0, column 1 of the buttons frame and add horizontal padding of 5 pixels (padx=5).

        self.reset_btn = ctk.CTkButton(
            buttons_frame,
            text="↻ RESET",
            command=self.reset_timer,
            font=("Arial", 12, "bold"),
            width=80
        ) # Create a button widget with the text "↻ RESET" that calls the reset_timer method when clicked. The button has a bold Arial font of size 12 and a fixed width of 80 pixels. This button is a child of the buttons frame (buttons_frame).
        self.reset_btn.grid(row=0, column=2, padx=5) # Place the reset button in the grid at row 0, column 2 of the buttons frame and add horizontal padding of 5 pixels (padx=5).

        # Session info frame
        info_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent") # Create a frame to hold the session information labels (session type, duration, cycles), with a transparent background color. This frame is a child of the timer frame (self.timer_frame).
        info_frame.pack(pady=(0, 10), padx=10, fill="x") # Pack the info frame into the timer frame with vertical padding of 0 pixels on top and 10 pixels on the bottom (pady=(0, 10)), horizontal padding of 10 pixels (padx=10), and make it fill horizontally (fill="x").

        self.session_label = ctk.CTkLabel(
            info_frame,
            text="FOCUS SESSION",
            font=("Arial", 11, "bold"),
            text_color="gray"
        ) # Create a label widget to display the current session type (e.g., "FOCUS SESSION" or "BREAK TIME"), with a bold Arial font of size 11 and gray text color. This label is a child of the info frame (info_frame).
        self.session_label.pack() # Pack the session label into the info frame with default padding.

        self.duration_label = ctk.CTkLabel(
            info_frame,
            text=f"Duration: {POMODORO_WORK_DURATION // 60} mins",
            font=("Arial", 10),
            text_color="gray"
        ) # Create a label widget to display the duration of the current session in minutes (e.g., "Duration: 25 mins"), with an Arial font of size 10 and gray text color. The initial text is set based on the work duration. This label is a child of the info frame (info_frame).
        self.duration_label.pack() # Pack the duration label into the info frame with default padding.

        self.cycles_label = ctk.CTkLabel(
            info_frame,
            text=f"Cycles: {self.current_cycle} / {self.total_cycles}",
            font=("Arial", 10),
            text_color="gray"
        ) # Create a label widget to display the current cycle count relative to the total number of cycles (e.g., "Cycles: 1 / 4"), with an Arial font of size 10 and gray text color. The initial text is set based on the current cycle and total cycles. This label is a child of the info frame (info_frame).
        self.cycles_label.pack() # Pack the cycles label into the info frame with default padding.
        
        self.notification_toggle = ctk.CTkCheckBox(
            info_frame,
            text="Enable Notifications",
            font=("Arial", 10),
            text_color="gray",
            command=self.toggle_notifications
        ) # Create a checkbox widget to allow the user to enable or disable notifications, with the text "Enable Notifications", an Arial font of size 10, and gray text color. The checkbox calls the toggle_notifications method when toggled. This checkbox is a child of the info frame (info_frame).
        self.notification_toggle.pack(pady=(10, 0)) # Pack the notification toggle checkbox into the info frame with vertical padding of 10 pixels on top and 0 pixels on the bottom (pady=(10, 0)).
        self.notification_toggle.select() # Set the notification toggle checkbox to be selected (enabled) by default when the application starts.
        
        self.update_session_info() # Call the update_session_info method to set the initial session information labels based on the current session type (work session) and cycle count when the application starts.

        self.apply_theme()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Set the protocol for handling the window close event (when the user clicks the close button on the window) to call the on_closing method, which can be used to perform any necessary cleanup (e.g., saving data) before the application exits.
        self.load_data() # Call the load_data method to load any previously saved tasks from a file when the application starts, allowing the user to continue where they left off with their task list.
    
    def set_logo(self, logo_path):
        """
        Set the application logo in the title bar using an ICO, PNG, or GIF image file.
        Args:
            logo_path (str): The file path to the image to be used as the application logo.
        """
        try:
            logo_path = self.resource_path(logo_path)
            if logo_path.lower().endswith('.ico'):
                # ICO files require iconbitmap()
                self.iconbitmap(logo_path)
            else:
                # PNG and GIF files use tk.PhotoImage
                self.app_logo = tk.PhotoImage(file=logo_path)
                self.iconphoto(True, self.app_logo)
        except Exception as e:
            print(f"Error loading logo image: {e}")
    
    def resource_path(self, relative_path):
        """Resolve asset paths for both dev and PyInstaller builds"""
        import sys
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    # Task management methods
    
    def add_task(self):
        """
        Add a new task to the task list with title and description.
        Retrieves task title and description from input fields, validates the title
        is not empty, creates a visual task element in the UI with a checkbox,
        description label, and delete button, stores the task in the internal list,
        and clears the input fields.
        The task element is displayed in a frame with the title as a checkbox,
        an optional description below it in gray text, and a delete button on the right.
        Returns:
            None: If task title is empty, the function returns early without adding the task.
        """
        color_scheme = self.get_current_color_scheme() # Get the current color scheme based on the session type (work or break) to use for the task element styling
        
        text = self.task_entry.get().strip() # Get the task title from the entry widget and remove leading/trailing whitespace
        description = self.task_description.get().strip() # Get the task description from the entry widget and remove leading/trailing whitespace
        
        if not text: # If the task title is empty after stripping whitespace, do not add the task and return early
            return # Task title is required, so we return early if it's empty
        
        # Create the task element in the UI
        task_element = ctk.CTkFrame(self.scroll_frame) # Create a frame to represent the individual task element in the UI, which will contain the checkbox for the task title, the description label, and the delete button. This frame is a child of the scrollable frame (self.scroll_frame) that holds all tasks.
        task_element.pack(pady=2, padx=10, fill="x") # Pack the task element frame into the scrollable frame with vertical padding of 2 pixels and horizontal padding of 10 pixels (pady=2, padx=10), and make it fill horizontally (fill="x").
        
        # Configure grid layout for task element
        task_element.grid_columnconfigure(0, weight=2) # Configure the grid layout of the task element frame to have two columns, with the first column (index 0) having a weight of 2 (taking up more space for the checkbox and description)...
        task_element.grid_columnconfigure(1, weight=1) # ...and the second column (index 1) having a weight of 1 (taking up less space for the delete button).
        
        # Create the checkbox for the task title
        checkbox = ctk.CTkCheckBox(task_element, text=text, text_color=color_scheme["primary_text"], fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"]) # Create a checkbox widget for the task title, with the text set to the task title and text color set to the primary text color of the current color scheme. This checkbox is a child of the task element frame (task_element).
        checkbox.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(10, 0)) # Place the checkbox in the grid at row 0, column 0 of the task element frame, align it to the left (sticky="w"), and add padding of 10 pixels on the left and top (padx=(10, 0), pady=(10, 0)).
        
        # Create the label for the task description
        description_label = ctk.CTkLabel(task_element, text=description if description else "No description", font=ctk.CTkFont(size=10), text_color=color_scheme["secondary_text"]) # Create a label widget for the task description, with the text set to the task description if provided, or "No description" if the description is empty. The font size is set to 10 and the text color is set to the secondary text color of the current color scheme. This label is a child of the task element frame (task_element).
        description_label.grid(row=1, column=0, sticky="w", padx=(20, 0), pady=(0, 5)) # Place the description label in the grid at row 1, column 0 of the task element frame, align it to the left (sticky="w"), and add padding of 20 pixels on the left and 5 pixels on the bottom (padx=(20, 0), pady=(0, 5)).
        
        # Create the delete button for the task
        delete_button = ctk.CTkButton(task_element, text="Delete", width=60, command=lambda: self.delete_task(task_element), fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"]) # Create a button widget with the text "Delete" that calls the delete_task method with the task_element as an argument when clicked. This button is a child of the task element frame (task_element).
        delete_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0, 10), pady=10) # Place the delete button in the grid at row 0, column 1 of the task element frame, make it span both rows (rowspan=2), align it to the right (sticky="e"), and add padding of 10 pixels on the right and top/bottom (padx=(0, 10), pady=10).
        
        # Store the task in the internal list
        self.all_tasks.append(task_element) # Add the task element frame to the internal list of tasks (self.all_tasks) to keep track of it for future reference (e.g., for deletion or updates). Note that this currently stores the UI element rather than a separate Task object, which may be something to consider for better data management.
        
        # Clear the input fields after adding the task
        self.task_entry.delete(0, "end") # Clear the task title entry widget by deleting the text from index 0 to the end, effectively resetting it for the next input
        self.task_description.delete(0, "end") # Clear the task description entry widget by deleting the text from index 0 to the end, resetting it for the next input
    
    def delete_task(self, task_element):
        """
        Delete a task element from the UI.
        
        Args:
            task_element: The task widget element to be destroyed/removed from the display.
        
        Note:
            This method removes the task from the UI only. Consider also removing the 
            corresponding Task object from self.all_tasks to maintain consistency between 
            the UI and the internal data model.
        """
        task_element.destroy() # Destroy the task element widget, which removes it from the UI. This does not currently remove the corresponding Task object from the internal list (self.all_tasks), so the data model will still contain the task unless additional logic is implemented to handle that.
        
        self.all_tasks = [task for task in self.all_tasks if task != task_element] # Update the internal list of tasks by filtering out the deleted task element. This ensures that the internal data model remains consistent with the UI after a task is deleted.
        
    # Timer utility methods

    def get_current_duration(self):
        """
        Get the current session duration based on the session type.
        
        Returns:
            int: The duration in minutes for the current session.
                 Returns POMODORO_WORK_DURATION if the current session is a work session,
                 otherwise returns POMODORO_BREAK_DURATION for a break session.
        """
        return POMODORO_WORK_DURATION if self.is_work_session else POMODORO_BREAK_DURATION
    
    def get_current_color_scheme(self):
        return (WORK_COLOR_SCHEME if self.is_work_session else BREAK_COLOR_SCHEME) if self.is_pomodoro_active else DEFAULT_COLOR_SCHEME
    
    def apply_theme(self):
        color_scheme = self.get_current_color_scheme()
        
        # Apply the logo based on current color scheme (default, work, or break)
        if color_scheme == WORK_COLOR_SCHEME:
            self.set_logo("assets/FocusFlow logo Red.ico") # Set the application logo to the light version for work sessions
        elif color_scheme == BREAK_COLOR_SCHEME:
            self.set_logo("assets/FocusFlow logo Green.ico") # Set the application logo to the dark version for break sessions
        else:
            self.set_logo("assets/FocusFlow logo.ico") # Set the application logo to the default version for non-Pomodoro sessions
        
        self.start_btn.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
        self.pause_btn.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
        self.reset_btn.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
        self.add_task_button.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
        self.timer_label.configure(text_color=color_scheme["text_color"])
        self.timer_progress_bar.configure(progress_color=color_scheme["progress_color"])
        self.session_label.configure(text_color=color_scheme["primary_text"])
        self.duration_label.configure(text_color=color_scheme["secondary_text"])
        self.cycles_label.configure(text_color=color_scheme["secondary_text"])
        self.notification_toggle.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
        
        for task_element in self.scroll_frame.winfo_children():
            for widget in task_element.winfo_children():
                widget_type = type(widget).__name__
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.configure(text_color=color_scheme["primary_text"], fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])
                elif isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=color_scheme["secondary_text"])
                elif isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color=color_scheme["bg_color"], hover_color=color_scheme["hover_color"])

    # Timer methods
    
    def start_timer(self):
        """
        Start or resume the timer.
        Checks if the timer is already running or if time has expired.
        If valid, sets the timer to running state and schedules the next
        tick update based on the remaining time to the next tick.
        Does nothing if:
        - Timer is already running
        - Remaining time is less than or equal to 0 (user should reset first)
        """
        if self.is_timer_running:
            return  # Timer is already running
        if self.time_left <= 0:
            return # Cannot start if time is already up, user should reset first
        
        self.is_timer_running = True # Start or resume the timer
        self.is_pomodoro_active = True # Mark that a Pomodoro session is active when the timer starts
        delay_ms = max(1, self.remaining_to_next_tick_ms) # Ensure we don't schedule with 0 or negative delay
        self.next_tick_at = time.monotonic() + (delay_ms / 1000) # Schedule the next update based on remaining time to next tick
        self.timer_job = self.after(delay_ms, self.update_timer) # Schedule the first update immediately or after the remaining time to next tick
        self.apply_theme() # Apply the appropriate color scheme based on the session type when the timer starts (work or break)
    
    def stop_timer(self):
        """
        Stop the timer and cancel any pending timer updates.

        This method halts the timer's execution by setting the running flag to False.
        If a timer job is scheduled, it calculates the remaining time until the next tick
        and stores it, then cancels the scheduled update. All timer state variables are
        reset to None.

        Returns:
            None
        """
        self.is_timer_running = False # Stop the timer
        if self.timer_job: # If there's a scheduled timer update, calculate remaining time to next tick and cancel it
            if self.next_tick_at is not None: # Calculate remaining time to next tick in milliseconds
                remaining_ms = int(round((self.next_tick_at - time.monotonic()) * 1000)) # Convert to milliseconds
                self.remaining_to_next_tick_ms = min(self.tick_interval_ms, max(1, remaining_ms)) # Ensure it's between 1 ms and the tick interval
            self.after_cancel(self.timer_job)  # Cancel the scheduled timer update
            self.timer_job = None # Reset timer job state
        self.next_tick_at = None # Reset next tick time state
            
    def reset_timer(self):
        """
        Reset the timer to its initial state.

        Stops the currently running timer, restores the time_left to the current session duration,
        resets the remaining milliseconds until the next tick to the full tick interval, and updates
        both the timer display and session information in the UI.
        """
        self.stop_timer() # Stop the timer to ensure no updates are occurring while we reset the state
        
        # Reset session state for a new cycle
        self.is_work_session = True # Reset to the first session type (work session)
        self.current_cycle = 1 # Reset to the first cycle
        self.is_pomodoro_active = False # Mark that no Pomodoro session is active after reset until the user starts the timer again
        self.time_left = self.get_current_duration() # Reset the remaining time to the initial duration based on the session type
        self.remaining_to_next_tick_ms = self.tick_interval_ms # Reset the remaining time to the next tick to the full tick interval
        self.current_session_total_duration = self.time_left # Reset the total duration for the current session to match the reset time_left
        self.progress_ratio = 0 if self.progress_mode == "completed" else 1 # Reset the progress ratio based on the current progress mode (0 for completed, 1 for remaining)
        self.timer_progress_bar.set(self.progress_ratio) # Update the timer progress bar to reflect the reset progress ratio
        self.apply_theme() # Apply the appropriate color scheme based on the reset session type (work session)
        
        self.update_timer_display()
        self.update_session_info()

    def save_data(self):
        try:
            data_path = self.get_data_folder() # Get the path to the data folder where tasks will be saved
            task_data = []
            for task_element in self.all_tasks:
                task_info = {}
                for widget in task_element.winfo_children():
                    if isinstance(widget, ctk.CTkCheckBox):
                        task_info["title"] = widget.cget("text")
                        task_info["completed"] = widget.get()
                    elif isinstance(widget, ctk.CTkLabel):
                        task_info["description"] = widget.cget("text")
                task_data.append(task_info)
            
            with open(os.path.join(data_path, "tasks.json"), "w") as f:
                json.dump(task_data, f, indent=4)
            
            settings_data = {
                "notifications_enabled": self.notifications_enabled,
            }
            
            with open(os.path.join(data_path, "settings.json"), "w") as f:
                json.dump(settings_data, f, indent=4)
            
        except Exception as e:
            print(f"Error saving data: {e}") # Print any exceptions that occur during the save process to the console for debugging purposes
            time.sleep(3) # Sleep briefly to allow the user to see the error message before the application closes, especially important for PyInstaller bundles where the console may close immediately after the application exits

    def on_closing(self):     
        self.save_data() # Save the current tasks to a file before closing the application to ensure that user data is not lost when they exit the app.
        self.destroy() # Destroy the main application window, which will close the application.

    def load_data(self):
        data_path = self.get_data_folder()
        tasks_file = os.path.join(data_path, "tasks.json")
        settings_file = os.path.join(data_path, "settings.json")
        
        # load tasks
        if os.path.exists(tasks_file):
            with open(tasks_file, "r") as f:
                task_data = json.load(f)
                for task in task_data:
                    self.task_entry.delete(0, "end")
                    self.task_description.delete(0, "end")
                    self.task_entry.insert(0, task.get("title", ""))
                    self.task_description.insert(0, task.get("description", ""))
                    self.add_task()
                    if task.get("completed", False):
                        last_task_element = self.all_tasks[-1]
                        for widget in last_task_element.winfo_children():
                            if isinstance(widget, ctk.CTkCheckBox):
                                widget.select() # Mark the checkbox as selected if the task was completed in the saved data
            
            self.task_entry.delete(0, "end") # Clear the task entry after loading tasks to reset the input field
            self.task_description.delete(0, "end") # Clear the task description entry after loading tasks to reset the input field
        
        # load settings
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                settings_data = json.load(f)
                self.notifications_enabled = settings_data.get("notifications_enabled", True) # Load the notifications enabled state from the saved settings, defaulting to True if not found
                if self.notifications_enabled:
                    self.notification_toggle.select() # Set the notification toggle checkbox to selected if notifications are enabled in the loaded settings
                else:
                    self.notification_toggle.deselect() # Set the notification toggle checkbox to deselected if notifications are disabled in the loaded settings
    
    def get_data_folder(self):
        data_path: str | None = os.getenv("LOCALAPPDATA")
        if data_path is None:
            data_path = os.path.expanduser("~")
        data_path = os.path.join(data_path, "FocusFlow")
        
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        return data_path
    
    def update_session_info(self):
        """
        Update the session information labels based on the current session type.
        Updates the session type label to display either "FOCUS SESSION" or "BREAK TIME",
        sets the duration label with the appropriate session duration in minutes,
        and displays the current cycle count relative to the total number of cycles.
        The duration is determined by POMODORO_WORK_DURATION for work sessions and
        POMODORO_BREAK_DURATION for break sessions.
        """
        if self.is_work_session: # If the current session is a work session, update the session label to "FOCUS SESSION" and set the duration label to show the work duration in minutes
            self.session_label.configure(text="FOCUS SESSION") # Update the session label to indicate it's a focus session
            work_mins = POMODORO_WORK_DURATION // 60 # Calculate the work duration in minutes by dividing the work duration in seconds by 60
            self.duration_label.configure(text=f"Duration: {work_mins} mins") # Update the duration label to show the work duration in minutes
        else: # If the current session is a break session, update the session label to "BREAK TIME" and set the duration label to show the break duration in minutes
            self.session_label.configure(text="BREAK TIME") # Update the session label to indicate it's break time
            break_mins = POMODORO_BREAK_DURATION // 60 # Calculate the break duration in minutes by dividing the break duration in seconds by 60
            self.duration_label.configure(text=f"Duration: {break_mins} mins") # Update the duration label to show the break duration in minutes
        
        self.cycles_label.configure(text=f"Cycles: {self.current_cycle} / {self.total_cycles}") # Update the cycles label to show the current cycle count relative to the total number of cycles (e.g., "Cycles: 1 / 4")

    def toggle_notifications(self):
        self.notifications_enabled = self.notification_toggle.get() == 1 # Toggle the enabled state of the notification handler based on the current state when the user interacts with the notification toggle checkbox. This allows the user to enable or disable notifications for session changes.

    def update_timer_display(self):
        """
        Update the timer display label with the current time remaining.

        Converts the remaining time (in seconds) to minutes and seconds format,
        then updates the timer_label widget to show the time in MM:SS format.
        """
        minutes = self.time_left // 60 # Calculate the number of whole minutes remaining by performing integer division of time_left by 60
        seconds = self.time_left % 60 # Calculate the remaining seconds by taking the modulus of time_left by 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}") # Update the timer_label widget's text to display the remaining time in MM:SS format, using zero-padding for single-digit minutes and seconds (e.g., 05:09)
        
        raw_ratio = (self.current_session_total_duration - self.time_left) / self.current_session_total_duration if self.current_session_total_duration > 0 else 0 # Calculate the raw progress ratio based on the elapsed time relative to the total session duration. If the total duration is greater than 0, calculate the ratio; otherwise, set it to 0 to avoid division by zero.
        if self.progress_mode == "completed": # If the progress mode is set to "completed
            self.progress_ratio = raw_ratio # In "completed" mode, the progress ratio directly reflects the elapsed time as a ratio of the total session duration (0 at the start, 1 at completion)
        else: # If the progress mode is set to "remaining"
            self.progress_ratio = 1 - raw_ratio # In "remaining" mode, the progress ratio is inverted to reflect the remaining time (1 at the start, 0 at completion)
        self.timer_progress_bar.set(self.progress_ratio) # Update the timer progress bar widget to reflect the new progress ratio, visually indicating how much time has elapsed or remains based on the selected mode.
    
    def update_timer(self):
        """
        Update the timer by decrementing the remaining time and managing the session state.
        Handles the timer tick logic including:
        - Decrementing time_left by 1 unit
        - Updating the timer display
        - Scheduling the next tick if time remains
        - Transitioning between work and break sessions
        - Tracking cycle progression through the Pomodoro sessions
        - Marking session completion when all cycles are finished
        The method manages state transitions:
        - Work session → Break session (if cycles remain)
        - Break session → Next work session (if cycles remain)
        - Final cycle completion → Session complete state
        Does nothing if the timer is not currently running.
        """
        if not self.is_timer_running: # If the timer is not running, we should not update the timer, so we return early.
            return # Timer is not running, so we do not update the timer and return early.

        if self.time_left > 0: # Decrement the remaining time by 1 second if there is still time left
            self.time_left -= 1 # Decrement the remaining time by 1 second

        self.update_timer_display() # Update the timer display to reflect the new remaining time after decrementing

        if self.time_left > 0 and self.is_timer_running: 
            # If there is still time left and the timer is still running, we need to schedule the next update for the timer tick.
            
            self.remaining_to_next_tick_ms = self.tick_interval_ms # Reset the remaining time to the next tick to the full tick interval (1000 ms) since we just completed a tick
            self.next_tick_at = time.monotonic() + (self.tick_interval_ms / 1000) # Schedule the next tick by setting the next_tick_at to the current time plus the tick interval (converted to seconds)
            self.timer_job = self.after(self.tick_interval_ms, self.update_timer) # Schedule the next update by calling the after method with the tick interval and the update_timer method as the callback, which will cause update_timer to be called again after the specified interval (1000 ms)
        else:
            # Time has run out for the current session, we need to transition to the next session or mark completion if all cycles are done. We also need to stop the timer since the current session is complete.
            
            self.is_timer_running = False # Stop the timer since the current session has completed
            self.timer_job = None # Reset the timer job state since we are no longer scheduling updates
            self.next_tick_at = None # Reset the next tick time state since we are no longer scheduling updates
            self.remaining_to_next_tick_ms = self.tick_interval_ms # Reset the remaining time to the next tick to the full tick interval for the next session
            
            if self.is_work_session:
                # Work session completed
                if self.current_cycle < self.total_cycles: # If we have not yet completed all cycles, we need to transition to the break session for the current cycle
                    
                    self.is_work_session = False # Transition to break session
                    self.time_left = self.get_current_duration() # Reset the remaining time to the duration of the break session by calling get_current_duration, which will return the appropriate duration based on the current session type (break session in this case)
                    self.update_session_info() # Update the session information labels to reflect the new session type (break session) and current cycle
                    self.update_timer_display() # Update the timer display to show the new remaining time for the break session
                    self.apply_theme() # Apply the new color scheme for the break session
                    self.notification_handler.notify_session_change("work", "break", self.current_cycle) # Send a notification to indicate that we have transitioned from a work session to a break session, including the current cycle number in the notification
                else:
                    self.session_label.configure(text="SESSION COMPLETE!") # If we have completed all cycles after finishing the last work session, we update the session_label to show "SESSION COMPLETE!" to indicate that the entire Pomodoro session is finished.
                    self.notification_handler.notify_session_change("work", "complete", self.current_cycle) # Send a notification to indicate that the entire Pomodoro session is complete, including the current cycle number in the notification
            else:
                # Break completed
                if self.current_cycle < self.total_cycles: # If we have not yet completed all cycles, we need to transition to the next work session for the next cycle
                    # Transition to next work cycle
                    self.current_cycle += 1 # Increment the current cycle count since we are moving to the next cycle
                    self.is_work_session = True # Transition to work session for the next cycle
                    self.time_left = self.get_current_duration() # Reset the remaining time to the duration of the work session for the next cycle by calling get_current_duration, which will return the appropriate duration based on the current session type (work session in this case)
                    self.update_session_info() # Update the session information labels to reflect the new session type (work session) and current cycle
                    self.update_timer_display() # Update the timer display to show the new remaining time for the work session of the next cycle
                    self.apply_theme() # Apply the new color scheme for the work session of the next cycle
                    self.notification_handler.notify_session_change("break", "work", self.current_cycle) # Send a notification to indicate that we have transitioned from a break session to a work session, including the current cycle number in the notification
                else:
                    # Should not reach here if logic is correct
                    self.session_label.configure(text="SESSION COMPLETE!") # If we have completed all cycles after finishing the last break session, we update the session_label to show "SESSION COMPLETE!" to indicate that the entire Pomodoro session is finished. This case should not normally be reached if the logic is correct, since we should have already marked completion after the last work session, but this is a safeguard in case of any logical errors.
                    self.notification_handler.notify_session_change("break", "complete", self.current_cycle) # Send a notification to indicate that the entire Pomodoro session is complete, including the current cycle number in the notification
        

if __name__ == "__main__":
    # Create an instance of the FocusFlowApp class, which initializes the application and sets up the UI, and then start the main event loop to run the application.
    app = FocusFlowApp() # Create an instance of the FocusFlowApp class, which initializes the application and sets up the user interface (UI) components.
    app.mainloop() # Start the main event loop of the application, which waits for user interactions and updates the UI accordingly. This call blocks until the application window is closed.
