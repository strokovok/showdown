<template>
    <div class="games">
        <router-link class="game" v-for="game in $store.getters.all_games" :to="`/games/${game.id}`">
            <img class="game-logo" src="/game.png">
            <div class="game-title">{{game.name}}</div>
        </router-link>
    </div>
</template>

<style lang="scss" scoped>
    .games {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }

    .game {
        margin: 10px;
        width: 200px;
        height: 200px;
        background: $col-panel;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        &:hover {
            transform: scale(1.1);
            background: mix($col-panel, $col-active, 70%);
        }
        &:active {
            transform: scale(0.9);
        }
        transition: all .3s ease;
        cursor: pointer;
        text-decoration: none;
    }

    .game-logo {
        width: 100px;
        height: 100px;
    }

    .game-title {
        margin-top: 20px;
        font-family: 'Source Sans Pro', sans-serif;
        color: $col-text;
        font-size: 18px;
    }
</style>

<script>
    export default {
        mounted() {
            this.$store.dispatch('reload_all_games');
        }
    }
</script>
