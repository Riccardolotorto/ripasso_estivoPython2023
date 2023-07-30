from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import contextily as ctx
import os
import matplotlib.pyplot as plt

quartieri = gpd.read_file("Quartieri/NIL_WM.dbf")
quartieri3857 = quartieri.to_crs(3857)
fontanelle = gpd.read_file("Fontanelle/Fontanelle_OSM_ODbL.dbf")
fontanelle3857 = fontanelle.to_crs(3857)

@app.route('/')
def home():
    q = list(quartieri3857.NIL)
    q.sort()
    return render_template("home.html", lista = q)


@app.route('/quartiereSelezionato', methods = ["GET"])
def quartiereSelezionato():
    quartiere = request.args.get("quartiereScelto")
    scelto = quartieri3857[quartieri3857.NIL == quartiere]
    ax = scelto.plot(figsize = (12, 6), edgecolor = "k", facecolor = "none", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("risultato.html", immagine = file_name)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)