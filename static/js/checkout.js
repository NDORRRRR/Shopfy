// Validasi form checkout
document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkout-form');
    
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = checkoutForm.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                alert('Mohon lengkapi semua field yang diperlukan.');
            }
        });
    }
});

// Tampilkan ringkasan pesanan saat checkout
function updateOrderSummary() {
    // Implementasi untuk memperbarui ringkasan pesanan secara dinamis
}