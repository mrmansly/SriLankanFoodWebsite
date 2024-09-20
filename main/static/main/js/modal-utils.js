// Utility javascript functions that are used in modal windows.

export function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "none";
    document.body.classList.remove('no-cursor-change');
}

