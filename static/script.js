document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const targetInput = document.getElementById("target");
    const scanButton = document.querySelector("button");

    form.addEventListener("submit", function (event) {

        const target = targetInput.value.trim();

        // Check if target is empty
        if (target === "") {
            event.preventDefault();

            alert("Please enter an authorized target IP address or hostname.");
            return;
        }

        // Change button while scan is running
        scanButton.textContent = "Scanning... Please Wait";
        scanButton.disabled = true;
    });

});
