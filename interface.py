from flask import Flask, request, render_template_string
import gui
import webbrowser
import json

site = Flask(__name__)

crash_examples = [
    [42.58544425738491, -104.87548828125001, 3],
    [29.650763783036968, -82.32433319091797, 1],
    [40.712776, -74.005974, 2],
    [34.052235, -118.243683, 1]
]

@site.route("/")
def map():
    with open("radius_picker_map.html") as f:
        return render_template_string(f.read())

@site.route("/log", methods=["POST"])
def log():
    data = request.json
    print(f"lat: {data['lat']} lon {data['lon']} radius: {data['radius']} search_type: {data['search_type']}")
    
    return {
        "crashes": [{
                "lat": crash[0],
                "lon": crash[1],
                "severity": crash[2]}
            for crash in crash_examples ]
    }


if __name__ == "__main__":
    gui.make_gui()
    webbrowser.open_new("http://127.0.0.1:5000/")

    site.run(debug=False)