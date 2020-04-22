import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('./views/Home.vue')
        },

        {
            path: '/games',
            name: 'games',
            component: () => import('./views/Games.vue')
        },
        {
            path: '/games/:game_id',
            component: () => import('./views/Game.vue'),
            children: [
                {
                    path: "/",
                    name: "game_details",
                    component: () => import('./views/GameDetails.vue')
                },
                {
                    path: "bots",
                    name: "game_bots",
                    component: () => import('./views/GameBots.vue')
                },
                {
                    path: "matches",
                    name: "game_matches",
                    component: () => import('./views/GameMatches.vue')
                },
                {
                    path: "create_bot",
                    name: "create_bot",
                    component: () => import('./views/GameCreateBot.vue')
                }
            ]
        },

        {
            path: '/users',
            name: 'users',
            component: () => import('./views/Users.vue')
        },
        {
            path: '/users/:user_id',
            name: 'user',
            component: () => import('./views/User.vue'),
        },

        {
            path: '/bots',
            name: 'bots',
            component: () => import('./views/Bots.vue'),
        },
        {
            path: '/bots/:bot_id',
            name: 'bot',
            component: () => import('./views/Bot.vue'),
        },
    ]
})
