import folium
from folium.plugins import Geocoder

crash_examples = [
    [42.58544425738491, -104.87548828125001, 3],
    [29.650763783036968, -82.32433319091797, 1],
    [40.712776, -74.005974, 2],
    [34.052235, -118.243683, 1]
]

def make_gui():
    # makes the map and center it at the center of the US
    map_center = [39.8283, -98.5795]
    m = folium.Map(location=map_center, zoom_start=6)

    # adds search bar
    Geocoder(collapsed=False, add_marker=True).add_to(m)

    custom_html = f"""
    <style>
        #submitBtn {{
            padding: 1vw 2vw;
            font-size: 1.2vw;
            background-color: #ff80aa;
            color: white;
            border: none;
            border-radius: 1vw;
            transition: background-color 0.25s;
            cursor: pointer;
        }}
        #submitBtn:hover {{
            background-color: #f8c8d8;
        }}
        #submitBtn:disabled {{
            background-color: gray;
            color: #aaaaa;
            cursor: not-allowed;
            opacity: 0.6;
        }}
        #radius-picker {{
            position: fixed;
            top: 1.5vh;
            left: 4vw;
            z-index: 1000;
            box-shadow: 0 .63vw 1vw;
            border-radius: 0.6vw;
            padding: 1.2vw;
            background-color: white;
        }}
    </style>

    <div id="radius-picker">
        <label>Radius (miles): <span id="radiusValue">10</span></label><br>
        <input type="range" id="radius_slider" min="1" max="100" value="10" step="1"
        oninput="document.getElementById('radiusValue').innerText = this.value;"/><br><br>

        <!-- buttons -->
        <label>Select Search Type:</label><br>
        <input type="radio" name="searchType" value="kd_dfs" checked> K-D Tree DFS<br>
        <input type="radio" name="searchType" value="quad"> Quad Tree Search<br><br>

        <button id="submitBtn" disabled>Submit Radius</button>
    </div>

    <script>
        let storedLat = null;
        let storedLng = null;
        let storedRadius = null;
        let circle = null;
        let crashSquares = [];

        function addClickCircle(map) {{
            map.on('click', function(e) {{
                let radius = document.getElementById("radius_slider").value;
                let miles = radius * 1609;

                storedLat = e.latlng.lat;
                storedLng = e.latlng.lng;
                storedRadius = radius;

                if (circle) {{
                    map.removeLayer(circle);
                }}

                circle = L.circle(e.latlng, {{
                    radius: miles,
                    color: 'purple',
                    fillColor: '#a020f0',
                    fillOpacity: 0.25
                }}).addTo(map).bindPopup("Radius: " + radius + " miles");

                document.getElementById("submitBtn").disabled = false;
            }});
        }}

        document.addEventListener("DOMContentLoaded", function() {{
            var map = window.{m.get_name()};
            addClickCircle(map);

            document.getElementById("submitBtn").addEventListener("click", function() {{
                if (storedRadius !== null) {{
                    let selectedType = document.querySelector('input[name="searchType"]:checked').value;

                    fetch("/log", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{
                            lat: storedLat,
                            lon: storedLng,
                            radius: storedRadius,
                            search_type: selectedType
                        }})
                    }})
                    .then(res => res.json())
                    .then(data => {{
                        // removes old squares
                        crashSquares.forEach(rect => map.removeLayer(rect));
                        crashSquares = [];

                        data.crashes.forEach(crash => {{
                            let size = 0.05;
                            let bounds = [
                                [crash.lat - size/2, crash.lon - size/2],
                                [crash.lat + size/2, crash.lon + size/2]
                            ];

                            // change the colors
                            let color = {{
                                1: "#00cc00",
                                2: "#ffcc00",
                                3: "#ff0000",
                                4: "#800000"
                            }}[crash.severity];

                            let rect = L.rectangle(bounds, {{
                                color: color,
                                weight: 1,
                                fillOpacity: 0.8
                            }}).addTo(map).bindPopup(`Severity: ${{crash.severity}}<br>Lat: ${{crash.lat.toFixed(4)}}<br>Lon: ${{crash.lon.toFixed(4)}}`);

                            crashSquares.push(rect);
                        }});
                    }});
                }}
            }});
        }});
    </script>
    """

    m.get_root().html.add_child(folium.Element(custom_html))
    m.save("radius_picker_map.html")
