 // Function to add a product to the cart
 function addToCart(productId) {
    // Retrieve the existing cart from localStorage or initialize an empty array
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Find the product details from the product list (you can retrieve this data dynamically if needed)
    const product = getProductDetails(productId); // You need to implement this function
    
    if (!product) {
        console.error('Product not found');
        return;
    }

    // Check if the product already exists in the cart
    const existingProduct = cart.find(item => item.id === productId);

    if (existingProduct) {
        // If the product exists, increment the quantity
        existingProduct.quantity += 1;
    } else {
        // If not, add the new product to the cart with quantity 1
        cart.push({ ...product, quantity: 1 });
    }

    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Optionally, update the cart UI
    updateCartUI();
}

// Dummy function to simulate retrieving product details
function getProductDetails(productId) {
    // Replace this with actual product data retrieval logic
    const products = [
        { id: 1, name: "Cartoon Astronaut T-Shirts", price: 2499, image: "img/products/f1.jpg" },
        { id: 2, name: "Cool Hoodie", price: 1999, image: "img/products/f2.jpg" },
        { id: 3, name: "Stylish Cap", price: 999, image: "img/products/f3.jpg" }
    ];
    return products.find(product => product.id === productId);
}

// Function to update the cart UI (example)
function updateCartUI() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartSection = document.querySelector('#cart tbody');
    cartSection.innerHTML = ""; // Clear existing rows

    let total = 0;
    cart.forEach(item => {
        total += item.price * item.quantity;

        const row = `
            <tr>
                <td><i class='bx bx-x-circle' onclick="removeFromCart(${item.id})"></i></td>
                <td><img src="${item.image}" alt="${item.name}"></td>
                <td>${item.name}</td>
                <td>₹${item.price}</td>
                <td><input type="number" value="${item.quantity}" onchange="updateQuantity(${item.id}, this.value)"></td>
                <td>₹${item.price * item.quantity}</td>
            </tr>
        `;
        cartSection.innerHTML += row;
    });

    console.log(`Total Cart Value: ₹${total}`);
}

// Function to remove a product from the cart
function removeFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
}

// Function to update product quantity in the cart
function updateQuantity(productId, quantity) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const product = cart.find(item => item.id === productId);

    if (product) {
        product.quantity = parseInt(quantity, 10);
        if (product.quantity <= 0) {
            removeFromCart(productId);
        } else {
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartUI();
        }
    }
}

// Initialize the cart UI on page load
document.addEventListener('DOMContentLoaded', updateCartUI);