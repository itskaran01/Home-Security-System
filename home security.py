import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import datetime
import random
from PIL import Image, ImageTk
import os

class HomeSecuritySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartGuard Home Security System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # System state variables
        self.system_armed = False
        self.alarm_triggered = False
        self.door_locked = True
        self.lights_on = False
        self.camera_active = False
        
        # Initialize sensors and their status labels separately
        self.sensor_status = {
            "Front Door": False,
            "Back Door": False,
            "Living Room Window": False,
            "Bedroom Window": False,
            "Motion Kitchen": False,
            "Motion Living Room": False
        }
        self.sensor_labels = {}  # To store the label references
        
        self.activity_log = []
        
        # Load images (placeholder paths - replace with your own)
        self.load_images()
        
        # Create GUI
        self.create_gui()
        
        # Simulate occasional sensor triggers
        self.simulate_sensor_activity()
    
    def load_images(self):
        """Load images for the GUI (placeholder implementation)"""
        try:
            # These paths should be replaced with actual image paths
            self.logo_img = PhotoImage(file="logo.png") if os.path.exists("logo.png") else None
            self.armed_img = PhotoImage(file="armed.png") if os.path.exists("armed.png") else None
            self.disarmed_img = PhotoImage(file="disarmed.png") if os.path.exists("disarmed.png") else None
            self.door_img = PhotoImage(file="door.png") if os.path.exists("door.png") else None
            self.window_img = PhotoImage(file="window.png") if os.path.exists("window.png") else None
            self.motion_img = PhotoImage(file="motion.png") if os.path.exists("motion.png") else None
            self.camera_img = PhotoImage(file="camera.png") if os.path.exists("camera.png") else None
            self.light_on_img = PhotoImage(file="light_on.png") if os.path.exists("light_on.png") else None
            self.light_off_img = PhotoImage(file="light_off.png") if os.path.exists("light_off.png") else None
        except:
            # If images don't exist, set to None
            self.logo_img = None
            self.armed_img = None
            self.disarmed_img = None
            self.door_img = None
            self.window_img = None
            self.motion_img = None
            self.camera_img = None
            self.light_on_img = None
            self.light_off_img = None
    
    def create_gui(self):
        """Create the main GUI components"""
        # Create a style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Status.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('Arm.TButton', foreground='white', background='#e74c3c')
        style.configure('Disarm.TButton', foreground='white', background='#2ecc71')
        style.configure('TNotebook', background='#2c3e50', borderwidth=0)
        style.configure('TNotebook.Tab', background='#34495e', foreground='white', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#2980b9')])
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        if self.logo_img:
            logo_label = ttk.Label(header_frame, image=self.logo_img)
            logo_label.pack(side=tk.LEFT, padx=10)
        
        title_label = ttk.Label(header_frame, text="SmartGuard Home Security", style='Header.TLabel')
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Status: DISARMED")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, style='Status.TLabel',
                              relief=tk.SUNKEN, anchor=tk.W, padding=5)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Tab control
        tab_control = ttk.Notebook(main_frame)
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Control Tab
        control_tab = ttk.Frame(tab_control)
        tab_control.add(control_tab, text='Control Panel')
        
        # Create control panel
        self.create_control_panel(control_tab)
        
        # Sensors Tab
        sensors_tab = ttk.Frame(tab_control)
        tab_control.add(sensors_tab, text='Sensors')
        
        # Create sensors panel
        self.create_sensors_panel(sensors_tab)
        
        # Logs Tab
        logs_tab = ttk.Frame(tab_control)
        tab_control.add(logs_tab, text='Activity Log')
        
        # Create logs panel
        self.create_logs_panel(logs_tab)
    
    def create_control_panel(self, parent):
        """Create the control panel with system controls"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # System control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=20)
        
        self.arm_button = ttk.Button(button_frame, text="ARM SYSTEM", style='Arm.TButton',
                                    command=self.arm_system)
        self.arm_button.pack(side=tk.LEFT, padx=10)
        
        self.disarm_button = ttk.Button(button_frame, text="DISARM SYSTEM", style='Disarm.TButton',
                                      command=self.disarm_system, state=tk.DISABLED)
        self.disarm_button.pack(side=tk.LEFT, padx=10)
        
        # Quick actions frame
        quick_frame = ttk.LabelFrame(control_frame, text="Quick Actions", padding=10)
        quick_frame.pack(fill=tk.X, pady=10)
        
        # Quick action buttons
        ttk.Button(quick_frame, text="Lock All Doors", command=self.lock_all_doors).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Unlock All Doors", command=self.unlock_all_doors).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Turn On Lights", command=self.turn_on_lights).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Turn Off Lights", command=self.turn_off_lights).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Activate Camera", command=self.toggle_camera).pack(side=tk.LEFT, padx=5)
        
        # Status indicators
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, pady=20)
        
        # Door status
        door_frame = ttk.Frame(status_frame)
        door_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(door_frame, text="Doors:").pack()
        self.door_status = ttk.Label(door_frame, text="LOCKED", foreground="green")
        self.door_status.pack()
        
        # Lights status
        lights_frame = ttk.Frame(status_frame)
        lights_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(lights_frame, text="Lights:").pack()
        self.lights_status = ttk.Label(lights_frame, text="OFF", foreground="red")
        self.lights_status.pack()
        
        # Camera status
        camera_frame = ttk.Frame(status_frame)
        camera_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(camera_frame, text="Camera:").pack()
        self.camera_status = ttk.Label(camera_frame, text="INACTIVE", foreground="red")
        self.camera_status.pack()
        
        # Alarm status
        alarm_frame = ttk.Frame(status_frame)
        alarm_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(alarm_frame, text="Alarm:").pack()
        self.alarm_status = ttk.Label(alarm_frame, text="READY", foreground="green")
        self.alarm_status.pack()
    
    def create_sensors_panel(self, parent):
        """Create the sensors status panel"""
        sensors_frame = ttk.Frame(parent)
        sensors_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a list of sensor names to iterate through
        sensor_names = list(self.sensor_status.keys())
        
        # Create sensor status indicators
        for i, sensor_name in enumerate(sensor_names):
            frame = ttk.Frame(sensors_frame)
            frame.grid(row=i//2, column=i%2, sticky="nsew", padx=10, pady=10)
            
            # Sensor icon based on type
            if "Door" in sensor_name and self.door_img:
                icon = self.door_img
            elif "Window" in sensor_name and self.window_img:
                icon = self.window_img
            elif "Motion" in sensor_name and self.motion_img:
                icon = self.motion_img
            else:
                icon = None
            
            if icon:
                ttk.Label(frame, image=icon).pack(side=tk.LEFT, padx=5)
            
            # Sensor info
            info_frame = ttk.Frame(frame)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            ttk.Label(info_frame, text=sensor_name, font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            
            status_label = ttk.Label(info_frame, text="Status: Secure", foreground="green")
            status_label.pack(anchor=tk.W)
            
            # Store the label reference in a separate dictionary
            self.sensor_labels[sensor_name] = status_label
        
        # Configure grid weights
        sensors_frame.grid_columnconfigure(0, weight=1)
        sensors_frame.grid_columnconfigure(1, weight=1)
        sensors_frame.grid_rowconfigure(0, weight=1)
        sensors_frame.grid_rowconfigure(1, weight=1)
        sensors_frame.grid_rowconfigure(2, weight=1)
    
    def create_logs_panel(self, parent):
        """Create the activity log panel"""
        logs_frame = ttk.Frame(parent)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log text area with scrollbar
        scrollbar = ttk.Scrollbar(logs_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(logs_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD,
                              bg='#34495e', fg='white', insertbackground='white',
                              font=('Consolas', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.log_text.yview)
        
        # Add sample logs
        self.update_logs()
    
    def arm_system(self):
        """Arm the security system"""
        self.system_armed = True
        self.status_var.set("System Status: ARMED")
        self.arm_button.config(state=tk.DISABLED)
        self.disarm_button.config(state=tk.NORMAL)
        self.alarm_status.config(text="ARMED", foreground="orange")
        self.log_activity("System armed")
        
        # Check if any sensors are triggered before arming
        triggered = any(self.sensor_status.values())
        if triggered:
            self.trigger_alarm("Sensor triggered while arming")
    
    def disarm_system(self):
        """Disarm the security system"""
        self.system_armed = False
        self.alarm_triggered = False
        self.status_var.set("System Status: DISARMED")
        self.arm_button.config(state=tk.NORMAL)
        self.disarm_button.config(state=tk.DISABLED)
        self.alarm_status.config(text="READY", foreground="green")
        self.log_activity("System disarmed")
    
    def lock_all_doors(self):
        """Lock all doors"""
        self.door_locked = True
        self.door_status.config(text="LOCKED", foreground="green")
        self.log_activity("All doors locked")
    
    def unlock_all_doors(self):
        """Unlock all doors"""
        self.door_locked = False
        self.door_status.config(text="UNLOCKED", foreground="red")
        self.log_activity("All doors unlocked")
        
        if self.system_armed:
            self.trigger_alarm("Door unlocked while system armed")
    
    def turn_on_lights(self):
        """Turn on all lights"""
        self.lights_on = True
        self.lights_status.config(text="ON", foreground="green")
        self.log_activity("All lights turned on")
    
    def turn_off_lights(self):
        """Turn off all lights"""
        self.lights_on = False
        self.lights_status.config(text="OFF", foreground="red")
        self.log_activity("All lights turned off")
    
    def toggle_camera(self):
        """Toggle camera state"""
        self.camera_active = not self.camera_active
        status = "ACTIVE" if self.camera_active else "INACTIVE"
        color = "green" if self.camera_active else "red"
        self.camera_status.config(text=status, foreground=color)
        action = "activated" if self.camera_active else "deactivated"
        self.log_activity(f"Security camera {action}")
    
    def trigger_alarm(self, reason):
        """Trigger the alarm system"""
        if not self.system_armed:
            return
            
        self.alarm_triggered = True
        self.alarm_status.config(text="ALARM!", foreground="red")
        self.log_activity(f"ALARM TRIGGERED: {reason}")
        
        # Show alarm popup
        messagebox.showerror("SECURITY ALERT", 
                           f"ALARM TRIGGERED!\nReason: {reason}\n\nTake appropriate action immediately!")
        
        # In a real system, this would trigger sirens, notifications, etc.
    
    def log_activity(self, message):
        """Log system activity"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.activity_log.append(log_entry)
        self.update_logs()
    
    def update_logs(self):
        """Update the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for entry in self.activity_log[-50:]:  # Show last 50 entries
            self.log_text.insert(tk.END, entry + "\n")
        
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
    
    def simulate_sensor_activity(self):
        """Simulate random sensor activity"""
        if self.system_armed and not self.alarm_triggered:
            # Small chance of a sensor triggering
            if random.random() < 0.05:
                sensor_name = random.choice(list(self.sensor_status.keys()))
                self.sensor_status[sensor_name] = True
                self.sensor_labels[sensor_name].config(text="Status: Triggered", foreground="red")
                self.trigger_alarm(f"{sensor_name} sensor triggered")
        
        # Schedule next simulation
        self.root.after(5000, self.simulate_sensor_activity)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeSecuritySystem(root)
    app.run()