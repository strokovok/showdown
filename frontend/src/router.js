import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);


export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        { path: '/', component: () => import('./views/Home.vue') },

        { path: '/games', component: () => import('./views/Games/Games.vue') },
        { path: '/games/:game_id', component: () => import('./views/Games/Game.vue'),
            children: [
                { path: "/", component: () => import('./views/Games/GameDetailedDescription.vue') },
                { path: "bots", component: () => import('./views/Bots/BotsList.vue'),
                    props: (route) => ({
                        show_user: true,
                        query: `?game_id=${route.params.game_id}`
                    })
                },
                { path: "matches", component: () => import('./views/Matches/MatchesList.vue'),
                    props: (route) => ({
                        query: `?game_id=${route.params.game_id}`
                    })
                },
                { path: "create_bot", component: () => import('./views/Games/GameCreateBot.vue') }
            ]
        },

        { path: '/users', component: () => import('./views/Users/Users.vue') },
        { path: '/users/:user_id', component: () => import('./views/Users/User.vue'),
            children: [
                { path: "/", component: () => import('./views/Users/UserDetailedDescription.vue') },
                { path: "bots", component: () => import('./views/Bots/BotsList.vue'),
                    props: (route) => ({
                        show_game: true,
                        query: `?owner_id=${route.params.user_id}`
                    })
                },
                { path: "matches", component: () => import('./views/Matches/MatchesList.vue'),
                    props: (route) => ({
                        show_game: true,
                        prefer_left_user_id: route.params.user_id,
                        query: `?user_id=${route.params.user_id}`
                    })
                }
            ]
        },

        { path: '/bots', component: () => import('./views/Bots/BotsList.vue'),
            props: {
                show_user: true,
                show_game: true
            }
        },
        { path: '/bots/:bot_id', component: () => import('./views/Bots/Bot.vue'),
            children: [
                { path: "/", component: () => import('./views/Bots/BotDetailedDescription.vue') },
                { path: "matches", component: () => import('./views/Matches/MatchesList.vue'),
                    props: (route) => ({
                        prefer_left_bot_id: route.params.bot_id,
                        query: `?bot_id=${route.params.bot_id}`
                    })
                },
                { path: "access", component: () => import('./views/Bots/BotAccess.vue') },
            ]
        },

        { path: '/matches', component: () => import('./views/Matches/MatchesList.vue'),
            props: {
                show_game: true
            }
        },
        { path: '/matches/:match_id', component: () => import('./views/Matches/Match.vue') },

        { path: '/register', component: () => import('./views/Register.vue')},
        { path: '/login', component: () => import('./views/Login.vue')},

    ]
})
