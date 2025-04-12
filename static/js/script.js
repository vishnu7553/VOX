document.addEventListener('DOMContentLoaded', function() {
    // File input handling
    const fileInput = document.getElementById('file-input');
    const fileName = document.querySelector('.file-name');
    const analyzeButton = document.querySelector('.analyze-button');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileName.textContent = this.files[0].name;
                analyzeButton.disabled = false;
            } else {
                fileName.textContent = 'No file selected';
                analyzeButton.disabled = true;
            }
        });
    }
    
    // Form submission handling
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const file = fileInput.files[0];
            if (!file) {
                e.preventDefault();
                return;
            }
            
            // You could add file validation here
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                e.preventDefault();
                alert('File size exceeds 10MB limit');
                return;
            }
            
            // Show loading state
            analyzeButton.disabled = true;
            analyzeButton.innerHTML = 'Analyzing... <div class="spinner"></div>';
        });
    }
});
