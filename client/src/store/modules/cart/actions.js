export default {
    async submitOrder(context, payload) {
        const URL_REGISTER = "https://localhost:8443/api/orders"

        const data = {"plates": JSON.parse(JSON.stringify(payload)).products}

        const response = await fetch(URL_REGISTER, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                'Authorization': `Bearer ${context.getters.token}`
            }
        });

        if (response.status === 200) {
            alert('Order submitted');
            // empty cart
            context.commit('emptyCart')
        } else {
            alert('ERROR!');
        }
    }
}