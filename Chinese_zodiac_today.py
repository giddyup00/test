import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import threading

def fetch_horoscope_data(sign, text_widget):
    # Construct the exact URL using the sign name
    url = f"https://www.astrology.com/horoscope/daily-chinese/{sign.lower()}.html"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the specific sign's horoscope page directly
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all paragraph texts
        paragraphs = soup.find_all('p')
        
        # Filter out short UI text and standard boilerplate 
        valid_texts = [
            p.get_text(strip=True) for p in paragraphs 
            if len(p.get_text(strip=True)) > 50 
            and "Chinese astrology" not in p.get_text(strip=True)
            and "More Horoscopes" not in p.get_text(strip=True)
        ]
        
        if valid_texts:
            # The actual daily reading is almost always the longest paragraph on the page
            horoscope_text = max(valid_texts, key=len)
            
            # Use root.after to safely update the GUI from a background thread
            text_widget.after(0, display_result, text_widget, f"Today's Horoscope for {sign}:\n\n{horoscope_text}")
        else:
            text_widget.after(0, display_result, text_widget, f"Horoscope content could not be parsed from:\n{url}")
            
    except requests.exceptions.RequestException as e:
        text_widget.after(0, display_result, text_widget, f"Network error occurred. Please check your connection:\n{e}")
    except Exception as e:
        text_widget.after(0, display_result, text_widget, f"An unexpected error occurred:\n{e}")

def display_result(text_widget, content):
    # Safely update the GUI with the fetched result
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)

def update_horoscope():
    sign = sign_var.get()
    if not sign:
        messagebox.showwarning("Selection Required", "Please select a Chinese Zodiac sign from the dropdown.")
        return
        
    # Set waiting state
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Fetching today's horoscope, please wait...\n")
    result_text.config(state=tk.DISABLED)
    
    # Run the scraping in a separate thread to prevent freezing the GUI
    thread = threading.Thread(target=fetch_horoscope_data, args=(sign, result_text))
    thread.daemon = True
    thread.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Daily Chinese Horoscope")
root.geometry("500x400")
root.configure(bg="#f2f2f2")

# List of Chinese Zodiac Signs
signs = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", 
         "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig"]

frame = tk.Frame(root, padx=20, pady=20, bg="#f2f2f2")
frame.pack(fill=tk.BOTH, expand=True)

# Zodiac Sign Dropdown Field
tk.Label(frame, text="Select your Chinese Zodiac Sign:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor=tk.W, pady=(0, 5))

sign_var = tk.StringVar()
dropdown = ttk.Combobox(frame, textvariable=sign_var, values=signs, state="readonly", font=("Arial", 12))
dropdown.pack(fill=tk.X, pady=(0, 15))

fetch_btn = tk.Button(frame, text="Get Today's Horoscope", command=update_horoscope, font=("Arial", 12, "bold"), bg="#d9534f", fg="white", relief=tk.FLAT)
fetch_btn.pack(fill=tk.X, pady=(0, 15))

# Horoscope Text Area Field
tk.Label(frame, text="Your Horoscope:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor=tk.W, pady=(0, 5))

result_text = tk.Text(frame, wrap=tk.WORD, font=("Georgia", 11), state=tk.DISABLED, height=10, bg="#ffffff", relief=tk.SOLID, borderwidth=1, padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

# Run application
root.mainloop()