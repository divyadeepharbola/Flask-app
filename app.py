from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load reference data from a file
def load_reference_data():
    with open("reference_data.txt", "r") as f:
        return json.load(f)

reference_data = load_reference_data()

# Function to find minerals by D-spacing
def find_minerals_by_d_spacing(input_d_spacing, tolerance, reference_data):
    result = []
    for mineral, ref_data in reference_data.items():
        for i, ref_peak in enumerate(ref_data["D-SPACING"]):
            if abs(ref_peak - input_d_spacing) <= tolerance:
                hkl = f"{ref_data['H'][i]}{ref_data['K'][i]}{ref_data['L'][i]}"
                intensity = ref_data["Intensity"][i]
                distance = abs(ref_peak - input_d_spacing)
                result.append((mineral, ref_peak, hkl, intensity, distance))
    
    result_sorted = sorted(result, key=lambda x: (-x[3], x[4]))
    return result_sorted

# Function to get all D-spacing values for a mineral
def get_d_spacing_for_mineral(mineral_name, reference_data):
    if mineral_name in reference_data:
        mineral_data = []
        for i, d_spacing in enumerate(reference_data[mineral_name]["D-SPACING"]):
            hkl = f"{reference_data[mineral_name]['H'][i]}{reference_data[mineral_name]['K'][i]}{reference_data[mineral_name]['L'][i]}"
            intensity = reference_data[mineral_name]["Intensity"][i]
            mineral_data.append((d_spacing, hkl, intensity))
        
        # Sort by intensity in descending order (highest intensity first)
        mineral_data_sorted = sorted(mineral_data, key=lambda x: -x[2])
        return mineral_data_sorted
    return None



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "find_minerals":
            d_spacing = float(request.form["d_spacing"])
            tolerance = float(request.form["tolerance"])
            results = find_minerals_by_d_spacing(d_spacing, tolerance, reference_data)
            return render_template("results.html", results=results, mode="find_minerals", d_spacing=d_spacing, tolerance=tolerance)
        elif action == "view_mineral":
            mineral_name = request.form["mineral_name"]
            mineral_data = get_d_spacing_for_mineral(mineral_name, reference_data)
            return render_template("results.html", results=mineral_data, mode="view_mineral", mineral_name=mineral_name)
    return render_template("index.html", minerals=list(reference_data.keys()))

if __name__ == "__main__":
    app.run(debug=True)
