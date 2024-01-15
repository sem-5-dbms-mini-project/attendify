function handleFileChange() {
    // Assuming there are only two file inputs, you can customize this function
    // based on your needs if you have more file inputs
    var fileInput1 = document.getElementById('dropzone-file1');
    var fileInput2 = document.getElementById('dropzone-file2');
    
    // Check if any of the file inputs have files selected
    if (fileInput1.files.length > 0 || fileInput2.files.length > 0) {
      // Submit the form
      document.getElementById('fileUpload').submit();
    }
}