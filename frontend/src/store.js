import Vue from 'vue';
import Vuex from 'vuex';

const axios = require('axios');


Vue.use(Vuex);


export default new Vuex.Store({
    state: {
        all_games: [],
        games_short: {},
        games_details: {},
        games_matches: {},
        games_bots: {}
    },
    getters: {
        all_games: state => state.all_games,
        games_short: state => state.games_short,
        games_details: state => state.games_details,
        games_matches: state => state.games_matches,
        games_bots: state => state.games_bots,
    },
    mutations: {
        set_all_games(state, all_games) {
            state.all_games = all_games;
            for (let game of all_games) {
                Vue.set(state.games_short, game.id, game);
            }
        },
        set_game_details(state, game) {
            Vue.set(state.games_details, game.id, game);
            Vue.set(state.games_short, game.id, game);
        },
        set_game_matches(state, game) {
            Vue.set(state.games_matches, game.id, game);
            Vue.set(state.games_short, game.id, game);
        },
        set_game_bots(state, game) {
            Vue.set(state.games_bots, game.id, game);
            Vue.set(state.games_short, game.id, game);
        }
    },
    actions: {
        reload_all_games(context) {
            axios.get('/api/games').then(response => {
                context.commit('set_all_games', response.data.games);
            }).catch(err => {
                console.log(err);
            });
        },
        reload_game_details(context, game_id) {
            axios.get(`/api/games/${game_id}`).then(response => {
                context.commit('set_game_details', response.data);
            }).catch(err => {
                console.log(err);
            });
        },
        reload_game_matches(context, game_id) {
            axios.get(`/api/games/${game_id}/matches`).then(response => {
                context.commit('set_game_matches', response.data);
            }).catch(err => {
                console.log(err);
            });
        },
        reload_game_bots(context, game_id) {
            axios.get(`/api/games/${game_id}/bots`).then(response => {
                context.commit('set_game_bots', response.data);
            }).catch(err => {
                console.log(err);
            });
        },
    }
})
