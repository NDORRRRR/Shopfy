// Fungsi untuk membuat slug dari nama produk
function makeSlug(text) {
    return text
        .toLowerCase()
        .replace(/[^\w ]+/g, '')
        .replace(/ +/g, '-');
}

// Auto-generate slug saat mengetik nama produk
document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('id_name');
    const slugInput = document.getElementById('id_slug');
    
    if (nameInput && slugInput) {
        nameInput.addEventListener('keyup', function() {
            slugInput.value = makeSlug(nameInput.value);
        });
    }
});