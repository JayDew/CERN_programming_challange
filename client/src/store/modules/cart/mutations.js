export default {
    addToOrder(state, payload) {
        // Check if the product with the given id already exists in the array
        const productIndex = state.products.findIndex(product => product.plate_id === payload);

        if (productIndex !== -1) {
            // Product exists, increment its quantity by 1
            state.products[productIndex].quantity += 1;
        } else {
            // Product doesn't exist, add it with a quantity of 1
            state.products.push({plate_id: payload, quantity: 1});
        }
    },
    removeFromOrder(state, payload) {
        // Find the index of the element with the specified plate_id
        const index = state.products.findIndex(item => item.plate_id === payload);

        if (index !== -1) {
            // Decrease the quantity
            state.products[index].quantity--;

            // Remove the entry if the quantity is smaller than 1
            if (state.products[index].quantity < 1) {
                state.products.splice(index, 1);
            }
        }
    },
    emptyCart(state) {
        state.products = []
    }
}
