// Utility javascript functions that are used as part of the image-preview-modal.html

function openModal(imageSrc, title, description) {
    const modal = document.getElementById("imagePreviewModal");
    const modalImg = document.getElementById("previewImage");
    const modalTitle = document.getElementById("previewImageTitle");
    const modalDescription = document.getElementById("previewImageDescription");

    modal.style.display = "block";
    modalImg.src = imageSrc;
    modalTitle.textContent = title;
    modalDescription.textContent = description;
}

function closeModal() {
    const modal = document.getElementById("imagePreviewModal");
    modal.style.display = "none";
}

