# Wreckognizer
Wreckognizer is an GUI application that uses data from Kaggle of US Accidents to locate car accidents around a selected location on a map interface. The dataset includes countrywide traffic accident reports of over 7.7 accidents. From a sampled set of records which include coordinates, severity, city, state, and zip code data of each accident, Wreckognizer builds both a K-D tree and a Quad tree using coordinate data. The user can search or manually select a location and a radius area to discover the location and magnitude of surrounding accidents.

The user when entering the area they would like to search, can choose to use either the K-D tree or Quad tree. 

![image](https://github.com/user-attachments/assets/66226f16-e4aa-445e-89b1-e97e5ca5a26d)



Implementation of a Quad Tree and K-D tree that compares the search algorithms of accidents in a specified radius to the user's selected location. The program displays the crashes as clickable dots on the map that can be clicked to see their severity.

This program runs on the dependencies Folium and Flask.

pip install Flask
pip install folium

Run interface.py to start the program. The code has a prebuilt tree, to make running the program quicker, but if you'd like to build the tree from scratch you can uncomment line 11 in init_tree.py.  

To use the program, select a radius for the circle from the slider and select which tree search type you would like to test. You can either search a location/address or just zoom in to some place in the contiguous US. Click a location, and then press the "Submit Radius" button. All crashes in that radius will be shown on screen. The crash circles are clickable and show the latitude, longitude, and severity of the crash.
