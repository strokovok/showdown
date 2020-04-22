import Vue from 'vue';
import Vuex from 'vuex';

const axios = require('axios');


Vue.use(Vuex);


export default new Vuex.Store({
    state: {
        all_games: [],
        games: {},
        games_matches: {},
        games_bots: {},

        all_users: [],
        users: {},
        users_bots: {},

        all_bots: [],
        bots: {},
        bots_matches: {},
    },
    getters: {
        all_games: state => state.all_games,
        get_game: state => id => state.games[id],
        get_game_matches: state => id => state.games_matches[id],
        get_game_bots: state => id => state.games_bots[id],

        all_users: state => state.all_users,
        get_user: state => id => state.users[id],
        get_user_bots: state => id => state.users_bots[id],

        all_bots: state => state.all_bots,
        get_bot: state => id => state.bots[id],
        get_bot_matches: state => id => state.bots_matches[id],
    },
    mutations: {
        set_all_games(state, all_games) {
            state.all_games = all_games;
        },
        set_game(state, { id, game }) {
            Vue.set(state.games, id, game);
        },
        set_game_matches(state, { id, matches }) {
            Vue.set(state.games_matches, id, matches);
        },
        set_game_bots(state, { id, bots }) {
            Vue.set(state.games_bots, id, bots);
        },

        set_all_users(state, all_users) {
            state.all_users = all_users;
        },
        set_user(state, { id, user }) {
            Vue.set(state.users, id, user);
        },
        set_user_bots(state, { id, bots }) {
            Vue.set(state.users_bots, id, bots);
        },

        set_all_bots(state, all_bots) {
            state.all_bots = all_bots;
        },
        set_bot(state, { id, bot }) {
            Vue.set(state.bots, id, bot);
        },
        set_bot_matches(state, { id, matches }) {
            Vue.set(state.bots_matches, id, matches);
        },
    },
    actions: {
        reload_all_games(context) {
            axios.get('/api/games').then(response => {
                context.commit('set_all_games', response.data.games);
            }).catch(err => console.log(err));
        },
        reload_game(context, id) {
            axios.get(`/api/games/${id}`).then(response => {
                context.commit('set_game', { id: id, game: response.data });
            }).catch(err => console.log(err));
        },
        reload_game_matches(context, id) {
            axios.get(`/api/matches?game_id=${id}`).then(response => {
                context.commit('set_game_matches', { id: id, matches: response.data.matches });
            }).catch(err => console.log(err));
        },
        reload_game_bots(context, id) {
            axios.get(`/api/bots?game_id=${id}`).then(response => {
                context.commit('set_game_bots', {id: id, bots: response.data.bots });
            }).catch(err => console.log(err));
        },

        reload_all_users(context) {
            axios.get('/api/users').then(response => {
                context.commit('set_all_users', response.data.users);
            }).catch(err => console.log(err));
        },
        reload_user(context, id) {
            axios.get(`/api/users/${id}`).then(response => {
                context.commit('set_user', { id: id, user: response.data });
            }).catch(err => console.log(err));
        },
        reload_user_bots(context, id) {
            axios.get(`/api/bots?owner_id=${id}`).then(response => {
                context.commit('set_user_bots', {id: id, bots: response.data.bots });
            }).catch(err => console.log(err));
        },

        reload_all_bots(context) {
            axios.get('/api/bots').then(response => {
                context.commit('set_all_bots', response.data.bots);
            }).catch(err => console.log(err));
        },
        reload_bot(context, id) {
            axios.get(`/api/bots/${id}`).then(response => {
                context.commit('set_bot', { id: id, bot: response.data });
            }).catch(err => console.log(err));
        },
        reload_bot_matches(context, id) {
            axios.get(`/api/matches?bot_id=${id}`).then(response => {
                context.commit('set_bot_matches', {id: id, matches: response.data.matches });
            }).catch(err => console.log(err));
        },
    }
})
