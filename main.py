from PyPDF2 import PdfReader
from gtts import gTTS
from tkinter import *
from tkinter import filedialog
import webbrowser

# Constants
BG_COLOR = "#39B5E0"
DEFAULT_SAVE_PATH = "C:/"
DEFAULT_FILE_PATH = "C:/"

class PDFToAudioConverter:
    def __init__(self, window):
        self.window = window
        self.save_path_directory = DEFAULT_SAVE_PATH
        self.file_path = DEFAULT_FILE_PATH
        self.setup_ui()

    def get_audio(self):
        try:
            reader = PdfReader(self.file_path)
            number_of_pages = len(reader.pages)
            all_pages_texts = []
            
            for i in range(number_of_pages):
                page = reader.pages[i]
                page_texts = page.extract_text()
                all_pages_texts.append(page_texts)
            
            all_texts = " ".join(all_pages_texts)
            
            if not all_texts.strip():
                self.title.config(text="Error: No text found in PDF", fg="red")
                return
                
            tts = gTTS(all_texts)
            tts.save(self.save_path_directory)
            self.title.config(text="Done! PDF converted to audio", fg="green")
            webbrowser.open(self.save_path_directory)
            
        except Exception as e:
            self.title.config(text=f"Error: {str(e)}", fg="red")

    def get_save_path(self):
        self.save_path_directory = filedialog.asksaveasfilename(
            title="Save As",
            initialfile="mypdf-audio.mp3",
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3")]
        )
        self.save_path_entry.delete(0, END)
        self.save_path_entry.insert(0, self.save_path_directory)

    def get_pdf(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Your PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        self.directory_entry.delete(0, END)
        self.directory_entry.insert(0, self.file_path)

    def setup_ui(self):
        self.window.minsize(500, 250)
        self.window.config(bg=BG_COLOR, pady=10, padx=10)
        self.window.title("PDF to Audio Converter")

        # Title
        self.title = Label(
            text="Convert PDF to Audio File",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg=BG_COLOR
        )
        self.title.grid(column=0, row=0, columnspan=3, pady=20)

        # PDF Selection
        browser_label = Label(
            text="PDF File:",
            font=("Arial", 10, "bold"),
            bg=BG_COLOR
        )
        browser_label.grid(column=0, row=1, sticky="e")

        self.directory_entry = Entry(width=40, font=("Arial", 10))
        self.directory_entry.grid(column=1, row=1, padx=10)

        browser_btn = Button(
            text="Browse",
            width=15,
            command=self.get_pdf,
            bg=BG_COLOR
        )
        browser_btn.grid(column=2, row=1, padx=5)

        # Save Location
        save_path_label = Label(
            text="Save As:",
            font=("Arial", 10, "bold"),
            bg=BG_COLOR
        )
        save_path_label.grid(column=0, row=2, sticky="e")

        self.save_path_entry = Entry(width=40, font=("Arial", 10))
        self.save_path_entry.grid(column=1, row=2, padx=10, pady=10)

        save_path_browser = Button(
            text="Choose Location",
            width=15,
            command=self.get_save_path,
            bg="green",
            fg="white"
        )
        save_path_browser.grid(column=2, row=2, padx=5)

        # Generate Button
        generate_audio = Button(
            text="Convert to Audio",
            bg="red",
            fg="white",
            command=self.get_audio,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        )
        generate_audio.grid(column=1, row=3, pady=20)

if __name__ == "__main__":
    window = Tk()
    app = PDFToAudioConverter(window)
    window.mainloop()