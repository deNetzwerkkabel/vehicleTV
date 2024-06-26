import json
import os

# Funktion, um HTML-Inhalt zu generieren
def generate_html(data, i):
    # Dynamically build images HTML
    images_html = ''.join([
        f'<div class="carousel-item{" active" if i == 0 else ""}">'
        f'<img src="{img["href"]}" class="d-block w-100" alt="..."></div>'
        for i, img in enumerate(data.get("images", []))  # Use data.get() to handle missing 'images'
    ])

    # Dynamically build price HTML
    price_html = (
        f'<div class="price">{data.get("parsedPrice", {}).get("valueString", "")}€ '
        f'<span class="price-details">{data.get("parsedPrice", {}).get("suffix", {}).get("label", "")}</span></div>'
    )

    # Dynamically build list-group items HTML
    list_group_html = ''.join([
        f'<li class="list-group-item"><div class="row"><div class="col-sm-5"><strong>{label}</strong></div><div class="col">{value}</div></div></li>'
        for label, value in [
            ("Motor", f"{data.get('motor', {}).get('fuel', {}).get('value', '')} | {data.get('motor', {}).get('powerPs', {}).get('value', '')} PS"),
            ("Modelljahr", data.get('modelyear', {}).get('value', '')),
            ("Getriebeart", data.get('gear', {}).get('value', '')),
            ("Kilometerstand", f"{data.get('mileage', {}).get('value', '')} km")
        ]
    ])

    try:
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        @font-face {{
        font-family: font;
        src: url(https://www.volkswagen.de/apps/clientlibs/vwa-ngw18/ngw18-frontend/clientlibs/statics/fonts/vwtext-regular.woff2);
        }}
        @font-face {{
        font-family: font_bold;
        src: url(https://www.volkswagen.de/apps/clientlibs/vwa-ngw18/ngw18-frontend/clientlibs/statics/fonts/vwtext-bold.woff2);
        }}

        body {{
        font-family: font;
        }}

        h1 {{
            font-family: font_bold;
        }}

        .container {{
        display: flex;
        justify-content: space-between;
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        }}

        .left {{
        width: 60%;
        }}

        .right {{
        width: 38%;
        }}

        .right {{
        padding: 20px;
        border: 1px solid rgb(8, 29, 77);
        }}

        .carousel {{
        height: 300px; /* Definierte Höhe */
        }}

        .carousel-item img {{
        height: 100%;
        object-fit: cover;
        }}

        .car-img {{
        width: 100%;
        height: auto;
        }}

        .car-images {{
        display: flex;
        justify-content: space-around;
        padding: 20px;
        }}

        .car-image {{
        width: 100px;
        height: auto;
        }}

        .title {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: font_bold;
        }}

        .subtitle {{
        font-size: 18px;
        margin-bottom: 10px;
        }}

        .price {{
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: font_bold;
        }}

        .price-details {{
        font-size: 14px;
        margin-bottom: 10px;
        }}

        .button {{
        background-color: #007bff;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin-bottom: 10px;
        }}

        .button-secondary {{
        background-color: #ddd;
        color: #000;
        }}

        .info {{
        font-size: 14px;
        margin-bottom: 10px;
        font-family: font;
        }}

        strong {{
            font-family: font_bold;
        }}

        .bg-body-white {{
            background-color: #fff;
        }}

        .list-group .list-group-item {{
            border-color: rgb(8, 29, 77, 0);
        }}

        /* Accent blue color */
        .accent-blue {{
        color: rgb(8, 29, 77);
        }}
        .accent-blue-bg {{
        background-color: rgb(8, 29, 77);
        }}
        .accent-blue-border {{
        border-color: rgb(8, 29, 77);
        }}
        </style>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <meta http-equiv="refresh" content="120; URL=car_{i}.html">
        </head>
        <body class="accent-blue-bg">

        <div class="container p-5 mb-3 bg-body-white rounded-3">
        <div class="left">
            <strong>{data.get("carTypeLabel", "")}</strong>
            <h1>{data.get("model", {}).get("value", "")}</h1>
            <div class="subtitle">{data.get("localCarTitle", {}).get("value", "")}</div>
            <div id="carouselExample" class="carousel slide car-img" data-bs-ride="carousel">
                <div class="carousel-inner">
                {images_html}
                </div>
            </div>
        </div>
        <div class="right accent-blue-border">
            <div class="subtitle">Kaufpreis</div>
            {price_html}
            <hr />
            <div class="">
                <ul class="list-group">
                    {list_group_html}
                </ul>
            </div>
            <hr />
            <div class="info">{data.get("contactData", {}).get("dealerLabel", "")}</div>
            <div class="info">{data.get("contactData", {}).get("dealerStreet", "")}</div>
            <div class="info">{data.get("contactData", {}).get("dealerAddress", "")}</div>
            <br />
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://www.volkswagen.de/de/modelle/verfuegbare-fahrzeuge-suche.html/__app/search/car/{data.get('key', "")}.app">
            <div class="info"><small>Dieses Angebot ist unverbindlich und freibleibend. Irrtümer und Änderungen vorbehalten.</small></div>
        </div>
        </div>

        </body>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        </html>
        '''
        return html_content
    except Exception as e:
        print(f"Es ist ein Fehler aufgetreten: {e}")



# Funktion, um die HTML-Dateien zu generieren
def generate_html_files(json_file, filename):
    with open(json_file, 'r') as f:
        cars = json.load(f)["cars"]

    if not os.path.exists(filename.removesuffix(".json")):
        os.makedirs(filename.removesuffix(".json"))

    print(f"{len(cars)} Autos in der Datei gefunden")
    for i, car in enumerate(cars):
        if i+1 == len(cars):
            l = 1
        else:
            l = i + 2
        html_content = generate_html(car, l)
        with open(f'{filename.removesuffix(".json")}/car_{i+1}.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)



def process_all_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            generate_html_files(file_path, filename)

# Hauptprogramm
if __name__ == "__main__":
    process_all_json_files('cars/')