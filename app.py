# Import models
from flask import Flask, request, render_template, flash
import requests
import datetime
import pytz
import wikipedia
import timezonefinder
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Define a function to get the city information
def get_city_info(city, country):
    # Use the geocode.xyz API to get the latitude and longitude of the city
    url = f"https://geocode.xyz/{city},{country}?json=1&auth=1884576044251515556x21704"
    response = requests.get(url)
    # Check the status code of the response
    if response.status_code == 200:
        # Extract the data from the response
        data = response.json()
        lat = data["latt"]
        long = data["longt"]
        # Use the timezonefinder module to get the timezone of the city
        tf = timezonefinder.TimezoneFinder()
        timezone = tf.timezone_at(lng=float(long), lat=float(lat))
        # Use the pytz and datetime modules to get the current time of the city
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        current_time = now.strftime("%H:%M:%S")
        # Append the current time of the city to a message variable
        
        message = f"زمان دقیق {city}  برابر است با  {current_time}"
        #message = f"The current time in {city}, {country} is {current_time}."

        # Flash the message with category "time"
        flash(message, "time")
        wikipedia.set_lang("fa")
        try:
            # Get the summary of the city
            summary = wikipedia.summary(city)
            # Append some information about the city to the message variable
            message = f"این مطالب مربوط به شهر {city} است:\n"
            message += summary + "\n"
            # Flash the message with category "summary"
            flash(message, "summary")
            # Get the list of tourist attractions in the city
            page = wikipedia.page(city)
            attractions = page.categories 
            # Filter out the categories that contain "Tourist attractions in ..."
            attractions = [a for a in attractions if a.startswith("Tourist attractions in ")]
            # Append some tourist attractions in the city to the message variable
            message = f"پیشنهاد میکنم که حتما به شهر{city} یه سری بزنید !!!:\n"
            message += "\n".join(attractions) + "\n"
            # Flash the message with category "attractions"
            flash(message, "attractions")

# Get the image urls of the city from Wikipedia
            image_urls = page.images[:5]
            # Flash the image urls with category "image"
            for image_url in image_urls:
                flash(image_url, "image")
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle the case when the city name is ambiguous
            # Append an error message to the message variable
            message = f"ببخشید ولی من نتونستم شهری به این اسم پیدا کنم!مطمئن شو که اسم شهر درست باشه!"
            # Flash the message with category "error"
            flash(message, "error")
        except wikipedia.exceptions.PageError as e:
            # Handle the case when the city name is not found on Wikipedia
            # Append an error message to the message variable
            message = f"ببخشید ولی من نتونستم شهری به این اسم پیدا کنم!مطمئن شو که اسم شهر درست باشه!"
            # Flash the message with category "error"
            flash(message, "error")
    else:
        # Handle the case when the response is not successful
        # Append an error message to the message variable
        message = f"ببخشید ولی من از سرور پاسخی دریافت نمیکنم . میتونی بعدا باز امتحان کنی؟"
        # Flash the message with category "error"
        flash(message, "error")

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        # Get the user input from the form
        country = request.form["Country"]
        city = request.form["City"]
        # Call the function with the user input
        get_city_info(city, country)
        # Return a message to confirm that the function was executed and pass no parameters to render_template 
        return render_template("index.html")

if __name__ == "__main__":
    app.run(port=4444, debug=True)