from flask import Flask, request, jsonify, send_file, render_template, after_this_request
import os
import time
from update_csv.processors.df_process import process_df
from update_csv.utils import make_dir
from update_csv.constant import UPLOAD_FOLDER, OUTPUT_FOLDER

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

make_dir(UPLOAD_FOLDER)
make_dir(OUTPUT_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")  # Serve the HTML UI

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".csv"):
        input_csv_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_csv_path)

        # Process the CSV and generate the output file path
        output_csv_path = process_df(input_csv_path)
        output_file_id = os.path.basename(output_csv_path)

        # Define cleanup actions for the uploaded file only
        @after_this_request
        def remove_uploaded_file(response):
            try:
                os.remove(input_csv_path)
                print(f"Uploaded file {input_csv_path} removed.")
            except Exception as e:
                print(f"Error removing uploaded file: {e}")
            return response

        # Return JSON metadata, not the file itself
        return jsonify({"download_url": f"/download_file/{output_file_id}", "file_id": output_file_id})

    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

@app.route("/download_file/<file_id>", methods=["GET"])
def download_file(file_id):
    output_file_path = os.path.join(OUTPUT_FOLDER, file_id)
    if not os.path.exists(output_file_path):
        return jsonify({"error": "File not found"}), 404

    # Define cleanup action to delete the processed file after download
    @after_this_request
    def remove_processed_file(response):
        try:
            time.sleep(1)  # Add a slight delay to ensure download starts
            os.remove(output_file_path)
            print(f"Processed file {output_file_path} removed after download.")
        except Exception as e:
            print(f"Error removing processed file: {e}")
        return response

    return send_file(output_file_path, mimetype="text/csv", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5150, debug=True)
