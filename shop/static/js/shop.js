 // Function to add a product to the cart
 function addToCart(productId) {
    // Define the URL for adding a product to the cart
    const url = "/cart/add/";

    // Prepare the data payload
    const data = {
        product_id: productId
    };

    // Make an AJAX POST request
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") // Django's CSRF token
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Failed to add product to cart");
        }
    })
    .then(data => {
        // Notify the user of success
        alert(`Product ${data.product_name} has been added to the cart!`);
    })
    .catch(error => {
        console.error(error);
        alert("An error occurred while adding the product to the cart.");
    });
}

// Helper function to get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
