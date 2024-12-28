import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading
from urllib.parse import urlparse
from datetime import datetime

class WebsiteChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Website Connectivity Checker")
        self.window.geometry("800x600")
        self.window.configure(bg="#2c3e50")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TButton", 
                           padding=10, 
                           font=("Helvetica", 10, "bold"))
        self.style.configure("Primary.TButton", 
                           background="#3498db", 
                           foreground="white")
        self.style.configure("Secondary.TButton", 
                           background="#95a5a6", 
                           foreground="white")
        
        # main container fr
        self.main_container = ttk.Frame(self.window, padding="20")
        self.main_container.pack(fill="both", expand=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # title
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Website Connectivity Checker",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Check the status and response time of any website",
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subtitle_label.pack(pady=(5, 0))
        

        input_container = tk.Frame(self.main_container, bg="#2c3e50")
        input_container.pack(fill="x", padx=20, pady=20)

        url_frame = tk.Frame(input_container, bg="#2c3e50")
        url_frame.pack(fill="x")
        
        url_label = tk.Label(
            url_frame,
            text="Website URL:",
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        url_label.pack(side="left", padx=(0, 10))
        
        self.url_entry = tk.Entry(
            url_frame,
            font=("Helvetica", 12),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            relief="flat",
            bd=0
        )
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        # Add a thin border under the entry
        border_frame = tk.Frame(url_frame, bg="#3498db", height=2)
        border_frame.pack(fill="x", expand=True, pady=(0, 5))
        
        # Buttons Frame
        buttons_frame = tk.Frame(input_container, bg="#2c3e50")
        buttons_frame.pack(fill="x", pady=(15, 0))
        
        check_button = tk.Button(
            buttons_frame,
            text="Check Website",
            command=self.start_check,
            font=("Helvetica", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        check_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(
            buttons_frame,
            text="Clear Results",
            command=lambda: self.result_text.delete(1.0, tk.END),
            font=("Helvetica", 11),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_button.pack(side="left", padx=5)
        
        # Results Frame
        results_frame = tk.LabelFrame(
            self.main_container,
            text="Results",
            font=("Helvetica", 11, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            padx=10,
            pady=10
        )
        results_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # RESULTS DIPSLAY HERE
        self.result_text = scrolledtext.ScrolledText(
            results_frame,
            font=("Consolas", 11),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            relief="flat",
            padx=10,
            pady=10
        )
        self.result_text.pack(fill="both", expand=True)
        
        # STATUS
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.window,
            textvariable=self.status_var,
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 10),
            pady=5
        )
        status_bar.pack(side="bottom", fill="x")
        
        # HOVER EFFECTIE THINGIES
        for button in [check_button, clear_button]:
            button.bind("<Enter>", lambda e, b=button: self.on_hover(e, b))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
    
    def on_hover(self, event, button):
        if button["bg"] == "#3498db":
            button.configure(bg="#2980b9")
        else:
            button.configure(bg="#7f8c8d")
            
    def on_leave(self, event, button):
        if button["bg"] == "#2980b9":
            button.configure(bg="#3498db")
        else:
            button.configure(bg="#95a5a6")
            
    def validate_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
            
    def check_website(self, url):
        try:
            if not self.validate_url(url):
                self.update_results("⚠️ Invalid URL format\n")
                return
                
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            self.status_var.set(f"Checking {url}...")
            response = requests.get(url, timeout=10)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            status_emoji = "✅" if response.status_code == 200 else "⚠️"
            
            result = f"""
{status_emoji} Check Results for: {url}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕒 Timestamp: {timestamp}
📊 Status Code: {response.status_code}
📝 Reason: {response.reason}
⚡ Response Time: {response.elapsed.total_seconds():.2f} seconds
🖥️ Server: {response.headers.get('Server', 'N/A')}
📄 Content Type: {response.headers.get('Content-Type', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            self.update_results(result)
            self.status_var.set("Ready")
            
        except requests.ConnectionError:
            self.update_results(f"❌ Failed to connect to {url}\n")
            self.status_var.set("Connection Error")
        except requests.Timeout:
            self.update_results(f"⏰ Timeout while connecting to {url}\n")
            self.status_var.set("Timeout Error")
        except Exception as e:
            self.update_results(f"❌ Error checking {url}: {str(e)}\n")
            self.status_var.set("Error Occurred")
            
    def update_results(self, text):
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        
    def start_check(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
            
        self.result_text.delete(1.0, tk.END)
        thread = threading.Thread(target=self.check_website, args=(url,))
        thread.daemon = True
        thread.start()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WebsiteChecker()
    app.run()