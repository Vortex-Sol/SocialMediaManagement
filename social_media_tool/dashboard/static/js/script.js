// Dark mode toggle functionality
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check for saved theme preference or default to dark mode
const currentTheme = localStorage.getItem('theme') || 'dark';

// Apply the saved theme
if (currentTheme === 'light') {
    body.setAttribute('data-theme', 'light');
    themeToggle.classList.add('active');
}

// Toggle theme function
function toggleTheme() {
    const currentTheme = body.getAttribute('data-theme');
    
    if (currentTheme === 'light') {
        body.removeAttribute('data-theme');
        themeToggle.classList.remove('active');
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        themeToggle.classList.add('active');
        localStorage.setItem('theme', 'light');
    }
}

// Add click event listener to toggle
themeToggle.addEventListener('click', toggleTheme);

// File upload functionality
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const cropBtn = document.getElementById('cropBtn');
let cropper = null;
let lastImageURL = null;

// Click to upload
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Handle file upload
function handleFile(file) {
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.createElement('img');
        preview.src = e.target.result;
        preview.className = 'preview-image';
        preview.alt = 'Preview';
        preview.style.maxWidth = '100%';
        preview.style.maxHeight = '100%';
        previewContainer.innerHTML = '';
        previewContainer.appendChild(preview);
        cropBtn.style.display = 'block';
        lastImageURL = e.target.result;
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    };
    reader.readAsDataURL(file);
}

cropBtn.addEventListener('click', () => {
    const img = previewContainer.querySelector('img');
    if (!img) return;
    if (cropper) {
        // If already cropping, get cropped data
        const canvas = cropper.getCroppedCanvas({
            width: 800,
            height: 800,
            imageSmoothingQuality: 'high'
        });
        const croppedDataUrl = canvas.toDataURL();
        cropper.destroy();
        cropper = null;
        img.src = croppedDataUrl;
        lastImageURL = croppedDataUrl;
        cropBtn.textContent = 'Crop Image';
    } else {
        cropper = new Cropper(img, {
            aspectRatio: NaN,
            viewMode: 1,
            autoCropArea: 1,
            movable: true,
            zoomable: true,
            scalable: true,
            rotatable: false,
            background: false,
        });
        cropBtn.textContent = 'Apply Crop';
    }
});

// Character counter for description
const descriptionTextarea = document.getElementById('description');
const charCount = document.getElementById('charCount');

descriptionTextarea.addEventListener('input', () => {
    const count = descriptionTextarea.value.length;
    charCount.textContent = count;
    
    if (count > 2000) {
        charCount.style.color = '#e74c3c';
    } else if (count > 1800) {
        charCount.style.color = '#f39c12';
    } else {
        charCount.style.color = 'var(--text-tertiary)';
    }
});

// Schedule toggle functionality
const enableSchedule = document.getElementById('enableSchedule');
const datePickerContainer = document.getElementById('datePickerContainer');

enableSchedule.addEventListener('change', () => {
    if (enableSchedule.checked) {
        datePickerContainer.classList.add('active');
    } else {
        datePickerContainer.classList.remove('active');
    }
});

// Set minimum date to current date/time
const publicationDate = document.getElementById('publicationDate');
const now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
publicationDate.min = now.toISOString().slice(0, 16);

// Button functionality
const previewBtn = document.getElementById('previewBtn');
const publishBtn = document.getElementById('publishBtn');

previewBtn.addEventListener('click', () => {
    const selectedPlatforms = Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
        .map(cb => cb.value);
    const description = descriptionTextarea.value;
    const isScheduled = enableSchedule.checked;
    const scheduleDate = publicationDate.value;

    if (selectedPlatforms.length === 0) {
        alert('Please select at least one platform');
        return;
    }

    console.log('Preview:', {
        platforms: selectedPlatforms,
        description,
        scheduled: isScheduled,
        publishDate: scheduleDate
    });

    alert('Preview functionality would show a modal with post preview here!');
});

publishBtn.addEventListener('click', () => {
    const selectedPlatforms = Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
        .map(cb => cb.value);
    const description = descriptionTextarea.value;
    const isScheduled = enableSchedule.checked;
    const scheduleDate = publicationDate.value;

    if (selectedPlatforms.length === 0) {
        alert('Please select at least one platform');
        return;
    }

    if (isScheduled && !scheduleDate) {
        alert('Please select a publication date');
        return;
    }

    console.log('Publishing:', {
        platforms: selectedPlatforms,
        description,
        scheduled: isScheduled,
        publishDate: scheduleDate
    });

    const action = isScheduled ? 'scheduled' : 'published';
    alert(`Post ${action} successfully to ${selectedPlatforms.join(', ')}!`);
});

// Additional utility functions
function validateForm() {
    const selectedPlatforms = document.querySelectorAll('input[name="platforms"]:checked');
    const description = descriptionTextarea.value.trim();
    
    return {
        isValid: selectedPlatforms.length > 0 && description.length > 0,
        errors: {
            noPlatforms: selectedPlatforms.length === 0,
            noDescription: description.length === 0
        }
    };
}

function resetForm() {
    // Clear file input and preview
    fileInput.value = '';
    previewContainer.innerHTML = '';
    cropBtn.style.display = 'none'; // Hide crop button on reset
    lastImageURL = null; // Clear last image URL
    
    // Uncheck all platforms
    document.querySelectorAll('input[name="platforms"]').forEach(cb => cb.checked = false);
    
    // Clear description
    descriptionTextarea.value = '';
    charCount.textContent = '0';
    
    // Reset scheduling
    enableSchedule.checked = false;
    datePickerContainer.classList.remove('active');
    publicationDate.value = '';
}

// Export functions for potential use in other modules
window.SocialMediaManager = {
    toggleTheme,
    handleFile,
    validateForm,
    resetForm
};
