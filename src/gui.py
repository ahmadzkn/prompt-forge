import customtkinter as ctk
import threading
import pyperclip
from typing import Dict
from src.optimizer import PromptOptimizer
from src.database import DatabaseManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PromptForge - The Ultimate Prompt Optimizer")
        self.geometry("1400x900")
        
        # Initialize Core Logic
        self.db = DatabaseManager()
        self.optimizer = PromptOptimizer()
        
        # Layout Config
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create Sidebar
        self.create_sidebar()
        
        # Create Main Area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1) # Input
        self.main_frame.grid_rowconfigure(1, weight=2) # Elements
        self.main_frame.grid_rowconfigure(2, weight=1) # Output

        self.create_section_a()
        self.create_section_b()
        self.create_section_c()

        self.load_models()
        self.load_history()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="PromptForge", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=20)

        # Settings
        ctk.CTkLabel(self.sidebar_frame, text="Backend URL:", anchor="w").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.url_entry = ctk.CTkEntry(self.sidebar_frame)
        self.url_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.url_entry.insert(0, "http://localhost:1234/v1")

        ctk.CTkLabel(self.sidebar_frame, text="Model:", anchor="w").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.model_option_menu = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False, values=["Loading..."])
        self.model_option_menu.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # History
        ctk.CTkLabel(self.sidebar_frame, text="History:", anchor="w").grid(row=5, column=0, padx=20, pady=(20, 0), sticky="w")
        self.history_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Past Sessions")
        self.history_frame.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")

    def create_section_a(self):
        # Input Section
        self.frame_a = ctk.CTkFrame(self.main_frame)
        self.frame_a.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_a.grid_columnconfigure(0, weight=1)
        self.frame_a.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_a, text="Raw Prompt", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.raw_prompt_textbox = ctk.CTkTextbox(self.frame_a)
        self.raw_prompt_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        self.optimize_btn = ctk.CTkButton(self.frame_a, text="Optimize Prompt", command=self.on_optimize, height=40)
        self.optimize_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ns")

    def create_section_b(self):
        # Structured Elements
        self.frame_b = ctk.CTkScrollableFrame(self.main_frame, label_text="Structured Elements")
        self.frame_b.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_b.grid_columnconfigure(0, weight=1)

        self.element_widgets = {}
        # New expanded list of elements
        elements = [
            "Persona", "Context", "Instruction", "Constraints", "Format", 
            "Exemplars", "Tone", "Delimiters", "Data", "Technique"
        ]
        
        for i, el in enumerate(elements):
            key = el.lower() # keys in JSON are lowercase
            
            frame = ctk.CTkFrame(self.frame_b)
            frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(frame, text=el + ":", width=100, anchor="e").grid(row=0, column=0, padx=10, pady=5)
            
            textbox = ctk.CTkTextbox(frame, height=60)
            textbox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
            
            copy_btn = ctk.CTkButton(frame, text="Copy", width=60, command=lambda t=textbox: self.copy_to_clipboard(t.get("0.0", "end")))
            copy_btn.grid(row=0, column=2, padx=10, pady=5)

            self.element_widgets[key] = textbox

    def create_section_c(self):
        # Final Prompt
        self.frame_c = ctk.CTkFrame(self.main_frame)
        self.frame_c.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_c.grid_columnconfigure(0, weight=1)
        self.frame_c.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_c, text="Final Optimized Prompy", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.final_prompt_textbox = ctk.CTkTextbox(self.frame_c)
        self.final_prompt_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        btn_frame = ctk.CTkFrame(self.frame_c, fg_color="transparent")
        btn_frame.grid(row=1, column=1, sticky="ns")

        self.copy_master_btn = ctk.CTkButton(btn_frame, text="Master Copy", command=lambda: self.copy_to_clipboard(self.final_prompt_textbox.get("0.0", "end")))
        self.copy_master_btn.pack(pady=10, padx=10)

    def on_optimize(self):
        raw_prompt = self.raw_prompt_textbox.get("0.0", "end").strip()
        if not raw_prompt:
            return

        self.optimize_btn.configure(state="disabled", text="Optimizing...")
        
        # Run in thread to not freeze UI
        threading.Thread(target=self.run_optimization, args=(raw_prompt,)).start()

    def run_optimization(self, raw_prompt):
        url = self.url_entry.get().strip()
        model = self.model_option_menu.get()
        
        # Update optimizer config
        self.optimizer = PromptOptimizer(base_url=url)
        
        result = self.optimizer.optimize_prompt(raw_prompt, model)
        
        # Update UI in main thread
        self.after(0, lambda: self.display_results(result, raw_prompt))

    def display_results(self, result: Dict, raw_prompt: str):
        self.optimize_btn.configure(state="normal", text="Optimize Prompt")
        
        if "error" in result:
            self.final_prompt_textbox.delete("0.0", "end")
            self.final_prompt_textbox.insert("0.0", f"Error: {result['error']}")
            return

        elements = result.get("elements", {})
        final = result.get("final_prompt", "")

        # Fill elements
        for key, text in elements.items():
            # normalize key
            normalized_key = key.lower()
            if normalized_key in self.element_widgets:
                self.element_widgets[normalized_key].delete("0.0", "end")
                self.element_widgets[normalized_key].insert("0.0", str(text))
        
        # Fill final prompt
        self.final_prompt_textbox.delete("0.0", "end")
        self.final_prompt_textbox.insert("0.0", final)

        # Save to DB
        try:
            self.db.add_session(raw_prompt, elements, final)
            self.load_history() # Refresh history
        except Exception as e:
            print(f"DB Error: {e}")

    def load_models(self):
        # Fetch models in background
        def fetch():
            models = self.optimizer.get_available_models()
            if models:
                self.after(0, lambda: self.model_option_menu.configure(values=models))
                self.after(0, lambda: self.model_option_menu.set(models[0]))
            else:
                self.after(0, lambda: self.model_option_menu.set("No models found"))
        
        threading.Thread(target=fetch).start()

    def load_history(self):
        # Clear existing
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        sessions = self.db.get_history()
        for s in sessions:
            btn = ctk.CTkButton(
                self.history_frame, 
                text=f"{s.timestamp.strftime('%H:%M')} - {s.raw_prompt[:20]}...", 
                command=lambda sid=s.id: self.load_session(sid),
                fg_color="transparent", 
                border_width=1,
                anchor="w",
                text_color=("gray10", "gray90")
            )
            btn.pack(fill="x", pady=2)

    def load_session(self, session_id):
        session = self.db.get_session(session_id)
        if not session:
            return
        
        self.raw_prompt_textbox.delete("0.0", "end")
        self.raw_prompt_textbox.insert("0.0", session.raw_prompt)
        
        elements = session.to_dict()["structured_elements"]
        for key, text in elements.items():
             normalized_key = key.lower()
             if normalized_key in self.element_widgets:
                self.element_widgets[normalized_key].delete("0.0", "end")
                self.element_widgets[normalized_key].insert("0.0", str(text))
        
        self.final_prompt_textbox.delete("0.0", "end")
        self.final_prompt_textbox.insert("0.0", session.final_prompt)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def on_closing(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
