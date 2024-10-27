from flask import Flask, request, jsonify, send_file
import os
from update_csv.processors.df_process import process_df
from update_csv.utils import make_dir
from update_csv.constant import UPLOAD_FOLDER, OUTPUT_FOLDER

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

make_dir(UPLOAD_FOLDER)
make_dir(OUTPUT_FOLDER)


@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    print(file)
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".csv"):
        input_csv_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_csv_path)

        # Process the CSV
        output_csv_path = process_df(input_csv_path)

        return send_file(output_csv_path, mimetype="text/csv", as_attachment=True)

    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5150, debug=True)
