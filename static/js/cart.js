// Fungsi untuk memperbarui jumlah item di keranjang
function updateCartQuantity(itemId, direction) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.value);
    
    if (direction === 'increase') {
        quantity += 1;
    } else if (direction === 'decrease') {
        if (quantity > 1) {
            quantity -= 1;
        }
    }
    
    quantityElement.value = quantity;
    document.getElementById(`update-form-${itemId}`).submit();
}

// Konfirmasi sebelum menghapus item
function confirmRemove(itemId, productName) {
    if (confirm(`Apakah Anda yakin ingin menghapus ${productName} dari keranjang?`)) {
        document.getElementById(`remove-form-${itemId}`).submit();
    }
}