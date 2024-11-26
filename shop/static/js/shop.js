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

// // Dummy function to simulate retrieving product details
// function getProductDetails(productId) {
//     // Replace this with actual product data retrieval logic
//     const products = [
//         { id: 1, name: "Cartoon Astronaut T-Shirts", price: 2499, image: "img/products/f1.jpg" },
//         { id: 2, name: "Cool Hoodie", price: 1999, image: "img/products/f2.jpg" },
//         { id: 3, name: "Stylish Cap", price: 999, image: "img/products/f3.jpg" }
//     ];
//     return products.find(product => product.id === productId);
// }

// // Function to update the cart UI (example)
// function updateCartUI() {
//     const cart = JSON.parse(localStorage.getItem('cart')) || [];
//     const cartSection = document.querySelector('#cart tbody');
//     cartSection.innerHTML = ""; // Clear existing rows

//     let total = 0;
//     cart.forEach(item => {
//         total += item.price * item.quantity;

//         const row = `
//             <tr>
//                 <td><i class='bx bx-x-circle' onclick="removeFromCart(${item.id})"></i></td>
//                 <td><img src="${item.image}" alt="${item.name}"></td>
//                 <td>${item.name}</td>
//                 <td>₹${item.price}</td>
//                 <td><input type="number" value="${item.quantity}" onchange="updateQuantity(${item.id}, this.value)"></td>
//                 <td>₹${item.price * item.quantity}</td>
//             </tr>
//         `;
//         cartSection.innerHTML += row;
//     });

//     console.log(`Total Cart Value: ₹${total}`);
// }

// // Function to remove a product from the cart
// function removeFromCart(productId) {
//     let cart = JSON.parse(localStorage.getItem('cart')) || [];
//     cart = cart.filter(item => item.id !== productId);
//     localStorage.setItem('cart', JSON.stringify(cart));
//     updateCartUI();
// }

// // Function to update product quantity in the cart
// function updateQuantity(productId, quantity) {
//     let cart = JSON.parse(localStorage.getItem('cart')) || [];
//     const product = cart.find(item => item.id === productId);

//     if (product) {
//         product.quantity = parseInt(quantity, 10);
//         if (product.quantity <= 0) {
//             removeFromCart(productId);
//         } else {
//             localStorage.setItem('cart', JSON.stringify(cart));
//             updateCartUI();
//         }
//     }
// }
