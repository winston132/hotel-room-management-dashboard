document.addEventListener("DOMContentLoaded", function () {
    // Enable Bootstrap Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto calculate booking total price
    const roomSelect = document.getElementById("room_id");
    const checkInInput = document.getElementById("check_in_date");
    const checkOutInput = document.getElementById("check_out_date");
    const totalCalcDisplay = document.getElementById("total_calc_display");

    function calculateTotal() {
        if (!roomSelect || !checkInInput || !checkOutInput || !totalCalcDisplay) return;

        const selectedOption = roomSelect.options[roomSelect.selectedIndex];
        if (!selectedOption || !selectedOption.dataset.price) {
            totalCalcDisplay.textContent = "$0.00";
            return;
        }

        const pricePerNight = parseFloat(selectedOption.dataset.price);
        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);

        if (checkInDate && checkOutDate && checkOutDate > checkInDate) {
            const diffTime = Math.abs(checkOutDate - checkInDate);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            const total = diffDays * pricePerNight;
            totalCalcDisplay.textContent = `$${total.toFixed(2)} (${diffDays} night${diffDays > 1 ? 's' : ''})`;
        } else {
            totalCalcDisplay.textContent = "$0.00";
        }
    }

    if (roomSelect) roomSelect.addEventListener("change", calculateTotal);
    if (checkInInput) checkInInput.addEventListener("change", calculateTotal);
    if (checkOutInput) checkOutInput.addEventListener("change", calculateTotal);
});
