import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

API_KEY = "58a13c1d3edc8bfc4ca9bad35c341650"

# Mapping weather condition to icon and background
def get_icon_and_bg(weather_main):
    if weather_main == "Clear":
        return "sunny.png", "yellow"  # Yellow
    elif weather_main == "Clouds":
        return "cloudy.png", "sky blue"  # Gray
    elif weather_main == "Rain":
        return "rainy.png", "Light Slate Gray"  # gray
    else:
        return "default.png", "Alice blue"  # Alice blue

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            city_name = data['name']
            temp = data['main']['temp']
            description = data['weather'][0]['description'].title()
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            weather_main = data['weather'][0]['main']

            # Get local icon and background color
            local_icon_file, bg_color = get_icon_and_bg(weather_main)

            # Update background colors
            root.configure(bg=bg_color)
            title.configure(bg=bg_color)
            weather_label.configure(bg=bg_color)
            icon_label.configure(bg=bg_color)

            # Load local image
            try:
                icon_img = Image.open(local_icon_file)
                icon_img = icon_img.resize((80, 80))
                icon_photo = ImageTk.PhotoImage(icon_img)
                icon_label.config(image=icon_photo)
                icon_label.image = icon_photo  # keep reference
            except Exception as img_err:
                icon_label.config(text="(No icon found)")

            # Display weather details
            weather_label.config(
                text=f"{city_name}\n{description}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind: {wind} m/s"
            )
        else:
            messagebox.showerror("API Error", data.get("message", "Error fetching weather data"))

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))


# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="Alice blue")

# Title
title = tk.Label(root, text="🌤️ Weather Forecast", font=("Helvetica", 22, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Entry
city_entry = tk.Entry(root, font=("Helvetica", 14), justify='center')
city_entry.pack(pady=10)
city_entry.focus()

# Button
search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=get_weather)
search_button.pack(pady=5)

# Weather Info
icon_label = tk.Label(root, bg="#f0f0f0")
icon_label.pack()

weather_label = tk.Label(root, font=("Helvetica", 15), justify='center', bg="#f0f0f0")
weather_label.pack(pady=10)

# Start the app
root.mainloop()
