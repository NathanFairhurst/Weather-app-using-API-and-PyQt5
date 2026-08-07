# Weather App using API

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLabel, QLineEdit, QPushButton,
                             QVBoxLayout)
from PyQt5.QtCore import Qt
from requests import RequestException

''' The three imports for the program are sys, requests and PyQt5. 
Sys lets you access to variables and functions that re close to the Python interpreter and runtime environment.
Requests allows us to get HTTP requests so the Open Weather API can be used and PyQt5 is Python's GUI application. '''

# The constructor of the class that contains all the labels, inputs and buttons for the GUI
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Check Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App") #Changes the title of the app

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

# Sets the layout of the GUI so all elements are placed vertically.

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

# Centers all the elements of the GUI

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

# Each widget has its own name to make it more readable and writeable

        # The style sheet for the GUI
        self.setStyleSheet("""
            QLabel{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
                background-color: rgb(210, 210, 210);
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }    
            QLabel#temperature_label{  
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
                text-overflow: ellipsis;
                }
            QLabel#description_label{
                font-size: 50px;
            }
            """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "6195ecce099d2d04ab3f47f3685a1c49" # API key from Open Weather
        city = self.city_input.text() # Lets the user input the name of a city
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        # With the use of import, the city input and API key, the user can find out the weather of where they're searching

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200: #Code 200 means successful request
                self.display_weather(data)

        #Checks the error codes and will output the error to the user
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP Error:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()


    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"] # The original temp is measured in Kelvin
        temperature_c = temperature_k - 273.15 # Kelvin is changed to Celsius
        weather_id = data["weather"][0]["id"] # Checks the id for the weather
        weather_description = (data["weather"][0]["description"]) # Gets the weather description

        self.temperature_label.setText(f"{temperature_c:.0f}°C") # Prints the temperature
        self.emoji_label.setText(self.get_weather_emoji(weather_id)) # Prints the emoji correlating to the weather
        self.description_label.setText(weather_description) # Prints the short description of the weather

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️" # If the weather id is between 200 and 232 there is a thunderstorm
        elif 300 <= weather_id <= 321:
            return "☁️" # If the weather id is between 300 and 321 it is light rain
        elif 500 <= weather_id <= 531:
            return "🌧️" # If the weather id is between 500 and 531 it is raining
        elif 600 <= weather_id <= 622:
            return "🌨️" # If the weather id is between 600 and 622 it is snowing
        elif 701 <= weather_id <= 741:
            return "🌫️" # If the weather id is between 701 and 741 it is foggy
        elif weather_id == 762:
            return "🌋" # If the weather id is 762, there is a volcano eruption
        elif weather_id == 771:
            return "💨" # If the weather id is 762, there is a squall or strong winds
        elif weather_id == 781:
            return "🌪️" # If the weather id is 781, there is a tornado
        elif weather_id == 800:
            return "☀️" # if the weather id is 800, there are clear skies
        elif 801 <= weather_id <= 804:
            return "☁️" # if the weather id is between 801 and 804 it is cloudy
        else:
            return "" # if there is no id or the id is outside the parameters, it will return an empty string

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

''' if __name__ == "__main__": checks if the user is running the program as a standalone or whether 
 it's being imported. The code will also open the GUI for the weather app. '''