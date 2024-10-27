function uploadFile(event) {
  event.preventDefault();

  // Show the loading spinner and hide the download button and error alert
  document.getElementById("loadingSpinner").style.display = "block";
  document.getElementById("downloadButton").style.display = "none";
  document.getElementById("errorAlert").style.display = "none";

  // Disable the submit button to prevent multiple submissions
  document.getElementById("submitButton").disabled = true;

  // Prepare the form data
  const formData = new FormData(document.getElementById("uploadForm"));

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to process file");
      }
      return response.blob();
    })
    .then((blob) => {
      // Hide the loading spinner
      document.getElementById("loadingSpinner").style.display = "none";

      // Show the download button
      document.getElementById("downloadButton").style.display = "block";

      // Create a download link for the processed CSV
      const url = window.URL.createObjectURL(blob);
      const downloadLink = document.getElementById("downloadLink");
      downloadLink.href = url;
      downloadLink.download = "processed_file.csv"; // Set the filename
    })
    .catch((error) => {
      document.getElementById("loadingSpinner").style.display = "none";
      document.getElementById("errorAlert").style.display = "block";
      document.getElementById("errorAlert").textContent = error.message;
    })
    .finally(() => {
      // Enable the submit button again
      document.getElementById("submitButton").disabled = false;
    });
}
