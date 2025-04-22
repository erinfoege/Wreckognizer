from flask import Flask, request, render_template_string
import gui
import webbrowser
import json
import pandas as pd
from kdTree import insert_rec, bfs_search, dfs_search
from quadTree import insert_quad, quad_search
from init_tree import build_trees


kd_root, quad_root = build_trees()

site = Flask(__name__)

@site.route("/")
def map():
    with open("radius_picker_map.html") as f:
        return render_template_string(f.read())

print(kd_root.point)
@site.route("/log", methods=["POST"])
def log():
    data = request.json
    lat = data["lat"]
    lon = data["lon"]
    radius = float(data["radius"])
    search_type = data["search_type"]

    center = (lat, lon)

    if search_type == "kd_dfs":
        results = dfs_search(kd_root, center, radius)
    elif search_type == "quad":
        results = quad_search(quad_root, center, radius)
    else:
        return {"crashes": []}

    # makes results look like what the frontend expects
    formatted = []
    for crash in results:
        formatted.append({
            "lat": float(crash.point[0]),
            "lon": float(crash.point[1]),
            "severity": int(crash.data["Severity"])
        })

    return {"crashes": formatted}

if __name__ == "__main__":
    gui.make_gui()

    webbrowser.open_new("http://127.0.0.1:5000/")
    site.run()
