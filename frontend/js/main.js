$(document).ready(function () {
    // Navbar Toggle Functionality
    $(".fa-bars").click(function () {
        $(this).toggleClass("fa-times");
        $(".navbar").toggleClass("nav-toggle");
    });

    // Scroll Event for Header Styling
    $(window).on("scroll load", function () {
        $(".fa-bars").removeClass("fa-times");
        $(".navbar").removeClass("nav-toggle");

        if ($(window).scrollTop() > 30) {
            $("header").addClass("header-active");
        } else {
            $("header").removeClass("header-active");
        }
    });

    // Contact Form Submission
    $("#contactForm").submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form values
        let name = $("#name").val().trim();
        let email = $("#email").val().trim();
        let phone = $("#phone").val().trim();
        let message = $("#message").val().trim();

        // Form validation (Ensure no fields are empty)
        if (!name || !email || !phone || !message) {
            alert("Please fill in all fields before submitting.");
            return;
        }

        let formData = { name, email, phone, message };

        // Send data to backend
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/contact", // Backend API endpoint
            data: JSON.stringify(formData),
            contentType: "application/json",
            success: function (response) {
                alert("Query sent successfully!");
                $("#contactForm")[0].reset(); // Reset form after submission
            },
            error: function (error) {
                alert("Error submitting form. Please try again.");
                console.error("Submission Error:", error);
            },
        });
    });
});
