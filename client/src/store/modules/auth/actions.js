export default {
    async login(context, payload) {
        const URL_REGISTER = "https://localhost:8443/api/users/login"
        const response = await fetch(URL_REGISTER, {
            method: 'POST',
            body: JSON.stringify({
                email: payload.email,
                password: payload.password
            }),
            headers: {"Content-Type": "application/json; charset=utf-8"}
        });
        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Authentication failed. Please try again.')
            alert(error)
        }
        // save token
        context.commit('setUser', {
            token: responseData.access_token
        })
    },
    async signup(context, payload) {
        const URL_REGISTER = "https://localhost:8443/api/users/register"
        const response = await fetch(URL_REGISTER, {
            method: 'POST',
            body: JSON.stringify({
                email: payload.email,
                password: payload.password,
                username: payload.username
            }),
            headers: {"Content-Type": "application/json; charset=utf-8"}
        });
        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Account already exists!')
            alert(error)
        } else {
            alert('Account created!')
        }
    }
};