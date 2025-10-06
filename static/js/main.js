document.addEventListener("DOMContentLoaded", function () {
    console.log("Gym Routine App cargada 🚀");

    // Toggle mostrar/ocultar contraseñas
    document.querySelectorAll(".toggle-password").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const targetSelector = this.getAttribute("data-target");
            const input = document.querySelector(targetSelector);
            const icon = this.querySelector("i");

            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            } else {
                input.type = "password";
                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }
        });
    });


    // Modal de confirmación (delete)
    const confirmDeleteModal = document.getElementById("confirmDeleteModal");
    if (confirmDeleteModal) {
        confirmDeleteModal.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;
            const url = button.getAttribute("data-bs-url");
            const name = button.getAttribute("data-bs-name");
            const form = document.getElementById("confirmDeleteForm");
            form.action = url;
            document.getElementById("confirmDeleteName").textContent = name;
        });
    }
});
