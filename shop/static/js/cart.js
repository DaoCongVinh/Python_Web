// Delete a cart item and update the cart dynamically
document.addEventListener("click", function (e) {
  if (e.target.closest(".delete-btn")) {
      const button = e.target.closest(".delete-btn");
      const itemId = button.getAttribute("data-item-id");
      deleteCartItem(itemId);
  }
});
function deleteCartItem(itemId) {
  console.log(`Attempting to delete item with ID: ${itemId}`);
  fetch(`/delete_item/${itemId}/`, {
      method: "GET",
      headers: {
          "X-Requested-With": "XMLHttpRequest",
      },
  })
      .then((response) => response.json())
      .then((data) => {
          console.log("Response data:", data);
          if (data.success) {
              const row = document.querySelector(`.delete-btn[data-item-id="${itemId}"]`).closest("tr");
              if (row) row.remove();

              // Update the cart total dynamically
              updateCartTotal(data.cart_total);
          } else {
              alert(data.message);
          }
      })
      .catch((error) => {
          console.error("Error:", error);
      });
}
  
  // Get CSRF token from the cookie
  function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        csrfToken = value;
        break;
      }
    }
    return csrfToken;
  }
  
  // Update the quantity of a cart item and reflect changes dynamically
  function updateQuantity(itemId, newQuantity) {
    const csrfToken = getCSRFToken();

    if (!csrfToken) {
        alert("CSRF token not found. Ensure your cookies are set up properly.");
        return;
    }

    if (newQuantity === 0) {
        // Call the delete function if quantity is 0
        deleteCartItem(itemId);
        return;
    }

    fetch(`/update_quantity/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `quantity=${newQuantity}`,
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                console.log("Update successful", data);
                const row = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`).closest("tr");
                const priceCell = row.querySelector(".price-cell");
                const totalCell = row.querySelector(".total-cell");

                if (priceCell && totalCell) {
                    const price = parseFloat(priceCell.dataset.price);
                    totalCell.innerText = `₫${(price * newQuantity).toLocaleString()}`;
                }

                updateGrandTotal();
            } else {
                console.error("Update failed:", data.message);
                alert(data.message);
            }
        })
        .catch((error) => console.error("Fetch error:", error));
}
  
  // Calculate and update the grand total dynamically
  function updateGrandTotal() {
    let grandTotal = 0;
  
    document.querySelectorAll(".total-cell").forEach((totalCell) => {
      const total = parseFloat(totalCell.innerText.replace(/₫|,/g, "") || 0);
      grandTotal += total;
    });
  
    const grandTotalElement = document.getElementById("total-price");
    if (grandTotalElement) {
      grandTotalElement.innerText = `₫${grandTotal.toLocaleString()}`;
    }
  }

  function updateCartTotal(cartTotal) {
    fetch("/cart/total/")
        .then((response) => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const grandTotalElement = document.querySelector("#subtotal td:nth-child(2)");
                const finalTotalElement = document.querySelector("#subtotal td:nth-child(4)");

                if (grandTotalElement && finalTotalElement) {
                    const cartTotal = data.cart_total;
                    grandTotalElement.innerText = `₫${cartTotal.toLocaleString()}`;
                    finalTotalElement.innerText = `₫${cartTotal.toLocaleString()}`;
                }
            } else {
                console.error("Failed to update cart total:", data.message);
            }
        })
        .catch((error) => console.error("Error updating cart total:", error));
}
  
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".quantity-input").forEach((input) => {
      input.addEventListener("change", () => {
          const itemId = input.dataset.itemId;
          const newQuantity = parseInt(input.value, 10);

          if (newQuantity >= 0) {
              updateQuantity(itemId, newQuantity);
          } else {
              alert("Quantity cannot be negative.");
              input.value = 1;
          }
      });
  });
});
  
    // Attach quantity inputs
    document.querySelectorAll(".quantity-input").forEach((input) => {
      input.addEventListener("change", () => {
        const itemId = input.dataset.itemId;
        const newQuantity = input.value;
        updateQuantity(itemId, newQuantity);
      });
    });


  