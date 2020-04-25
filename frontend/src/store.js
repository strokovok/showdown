import Vue from 'vue';
import Vuex from 'vuex';

const axios = require('axios');


Vue.use(Vuex);


export default new Vuex.Store({
    state: {
        games_lists: {},
        games: {},

        users_lists: {},
        users: {},

        bots_lists: {},
        bots: {},

        matches_lists: {},
        matches: {},
    },
    getters: {
        get_games_list: state => query => state.games_lists[query],
        get_game: state => id => state.games[id],

        get_users_list: state => query => state.users_lists[query],
        get_user: state => id => state.users[id],

        get_bots_list: state => query => state.bots_lists[query],
        get_bot: state => id => state.bots[id],

        get_matches_list: state => query => state.matches_lists[query],
        get_match: state => id => state.match[id],
    },
    mutations: {
        set_games_list: (state, { query, list }) => Vue.set(state.games_lists, query, list),
        set_game: (state, { id, game }) => Vue.set(state.games, id, game),

        set_users_list: (state, { query, list }) => Vue.set(state.users_lists, query, list),
        set_user: (state, { id, user }) => Vue.set(state.users, id, user),

        set_bots_list: (state, { query, list }) => Vue.set(state.bots_lists, query, list),
        set_bot: (state, { id, bot }) => Vue.set(state.bots, id, bot),

        set_matches_list: (state, { query, list }) => Vue.set(state.matches_lists, query, list),
        set_match: (state, { id, match }) => Vue.set(state.matches, id, match),
    },
    actions: {
        reload_games_list(context, query) {
            axios.get(`/api/games${query}`).then(response => {
                context.commit('set_games_list', { 'query': query, list: response.data.games });
            }).catch(err => console.log(err));
        },
        reload_game(context, id) {
            axios.get(`/api/games/${id}`).then(response => {
                context.commit('set_game', { 'id': id, game: response.data });
            }).catch(err => console.log(err));
        },

        reload_users_list(context, query) {
            axios.get(`/api/users${query}`).then(response => {
                context.commit('set_users_list', { 'query': query, list: response.data.users });
            }).catch(err => console.log(err));
        },
        reload_user(context, id) {
            axios.get(`/api/users/${id}`).then(response => {
                context.commit('set_user', { 'id': id, user: response.data });
            }).catch(err => console.log(err));
        },

        reload_bots_list(context, query) {
            axios.get(`/api/bots${query}`).then(response => {
                context.commit('set_bots_list', { 'query': query, list: response.data.bots });
            }).catch(err => console.log(err));
        },
        reload_bot(context, id) {
            axios.get(`/api/bots/${id}`).then(response => {
                context.commit('set_bot', { 'id': id, bot: response.data });
            }).catch(err => console.log(err));
        },

        reload_matches_list(context, query) {
            axios.get(`/api/matches${query}`).then(response => {
                context.commit('set_matches_list', { 'query': query, list: response.data.matches });
            }).catch(err => console.log(err));
        },
        reload_match(context, id) {
            axios.get(`/api/matches/${id}`).then(response => {
                context.commit('set_match', { 'id': id, match: response.data });
            }).catch(err => console.log(err));
        },
    }
})
