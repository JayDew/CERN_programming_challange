import {createStore} from 'vuex';
import authModule from './modules/auth/index.js'
import cartModule from './modules/cart/index.js'
import menuModule from './modules/menu/index.js'


const store = createStore({
    modules: {
        auth: authModule,
        cart: cartModule,
        menu: menuModule
    }
})

export default store;

