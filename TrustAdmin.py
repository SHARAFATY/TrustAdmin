import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import subprocess
import os

LOG_FILE = "trustadmin.log"

def log_to_file(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

class TrustAdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TrustAdmin – Admin control with Trusted Installer powers")
        self.root.geometry("650x450")
        self.root.configure(bg="white")
        
        self.label = tk.Label(root, text="TrustAdmin – Admin control with Trusted Installer powers", font=("Arial", 12, "bold"), bg="white")
        self.label.pack(pady=10)
        
        self.log_area = scrolledtext.ScrolledText(root, width=75, height=10)
        self.log_area.pack(pady=10)
        
        button_frame = tk.Frame(root, bg="white")
        button_frame.pack(pady=10)
        
        self.status_button = tk.Button(button_frame, text="Check Status", command=self.check_status, bg="blue", fg="white", width=20)
        self.grant_button = tk.Button(button_frame, text="Grant Privileges", command=self.grant_privileges, bg="green", fg="white", width=20)
        self.restore_button = tk.Button(button_frame, text="Restore Permissions", command=self.restore_permissions, bg="orange", fg="white", width=20)
        self.export_log_button = tk.Button(button_frame, text="Export Log", command=self.export_log, bg="purple", fg="white", width=20)
        self.toggle_theme_button = tk.Button(button_frame, text="Toggle Dark Mode", command=self.toggle_theme, bg="gray", fg="black", width=20)
        self.exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="red", fg="white", width=20)
        
        self.status_button.grid(row=0, column=0, padx=10, pady=5)
        self.grant_button.grid(row=0, column=1, padx=10, pady=5)
        self.restore_button.grid(row=1, column=0, padx=10, pady=5)
        self.export_log_button.grid(row=1, column=1, padx=10, pady=5)
        self.toggle_theme_button.grid(row=2, column=0, padx=10, pady=5)
        self.exit_button.grid(row=2, column=1, padx=10, pady=5)
        
        self.credits_label = tk.Label(root, text="Developed by QuickSilver\nGitHub: Quicksilver-lab", font=("Arial", 10, "italic"), bg="white")
        self.credits_label.pack(pady=10)
        
        self.dark_mode = False
    
    def toggle_theme(self):
        colors = {True: ("black", "white", "darkgray"), False: ("white", "black", "gray")}
        bg, fg, btn_bg = colors[self.dark_mode]
        self.root.configure(bg=bg)
        self.label.configure(bg=bg, fg=fg)
        self.credits_label.configure(bg=bg, fg=fg)
        self.toggle_theme_button.configure(bg=btn_bg, fg=fg)
        self.dark_mode = not self.dark_mode
    
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        log_to_file(message)
    
    def command_exists(self, command):
        return subprocess.call(f"where {command}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    
    def check_status(self):
        self.log("Checking ownership status of C:\\Windows...")
        try:
            if not self.command_exists("icacls"):
                self.log("Error: 'icacls' command not found. Ensure you are running on a supported Windows system.")
                messagebox.showerror("Error", "'icacls' command not found. Ensure you are on Windows.")
                return
            result = subprocess.run("icacls C:\\Windows", shell=True, capture_output=True, text=True)
            self.log(result.stdout)
        except Exception as e:
            self.log(f"Error checking status: {str(e)}")
            messagebox.showerror("Error", f"Exception: {str(e)}")
    
    def grant_privileges(self):
        if not os.name == 'nt':
            self.log("This script only works on Windows.")
            messagebox.showerror("Error", "This script is only compatible with Windows.")
            return
        if not self.command_exists("takeown"):
            self.log("Error: 'takeown' command not found. Ensure you are on a Windows system.")
            messagebox.showerror("Error", "'takeown' command not found. Ensure you are on Windows.")
            return
        self.log("Granting Trusted Installer privileges...")
        cmd = "takeown /f C:\\Windows /r /d y && icacls C:\\Windows /grant administrators:F /t /c /q"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("Privileges granted successfully.")
                messagebox.showinfo("Success", "Trusted Installer privileges granted successfully.")
            else:
                self.log(f"Error: {result.stderr}")
                messagebox.showerror("Error", f"Failed to grant privileges: {result.stderr}")
        except Exception as e:
            self.log(f"Exception occurred: {str(e)}")
            messagebox.showerror("Error", f"Exception: {str(e)}")
    
    def restore_permissions(self):
        if not self.command_exists("icacls"):
            self.log("Error: 'icacls' command not found. Ensure you are on a Windows system.")
            messagebox.showerror("Error", "'icacls' command not found. Ensure you are on Windows.")
            return
        self.log("Restoring ownership to TrustedInstaller...")
        cmd = "icacls C:\\Windows /setowner \"NT SERVICE\\TrustedInstaller\" /t /c /q"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("Ownership restored to TrustedInstaller.")
                messagebox.showinfo("Success", "Ownership restored to TrustedInstaller.")
            else:
                self.log(f"Error: {result.stderr}")
                messagebox.showerror("Error", f"Failed to restore permissions: {result.stderr}")
        except Exception as e:
            self.log(f"Exception occurred: {str(e)}")
            messagebox.showerror("Error", f"Exception: {str(e)}")
    
    def export_log(self):
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
            if filepath:
                with open(LOG_FILE, "r") as f:
                    content = f.read()
                with open(filepath, "w") as f:
                    f.write(content)
                messagebox.showinfo("Export Log", "Log exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Exception: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrustAdminGUI(root)
    root.mainloop()
