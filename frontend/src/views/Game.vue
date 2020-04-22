<template>
    <div class="content-panel-container">
        <div class="content-panel short-info-panel" v-if="game !== undefined">
            <img class="game-logo" src="/game.png">
            <div class="short-info">
                <div class="game-name">{{game.name}}</div>
                <div class="game-short-descr">Здесь будет краткая информация.</div>
            </div>
        </div>
        <div class="subnav">
            <router-link :to="`/games/${game_id}/`" class="navigation-link-exact">Детали</router-link>
            <router-link :to="`/games/${game_id}/matches`" class="navigation-link-exact">Матчи</router-link>
            <router-link :to="`/games/${game_id}/bots`" class="navigation-link-exact">Боты</router-link>
            <router-link :to="`/games/${game_id}/create_bot`" class="navigation-link-exact">Создать бота</router-link>
        </div>
        <router-view/>
    </div>
</template>

<style lang="scss" scoped>
    .subnav {
        width: 98.5%;
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }

    .short-info-panel {
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
    }

    .game-logo {
        width: 100px;
        height: 100px;
        flex-shrink: 0;
    }

    .short-info {
        margin-left: 30px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }

    .game-name {
        font-size: 24px;
        font-weight: 600;
    }

    .game-short-descr {
        margin-top: 8px;
        font-size: 18px;
    }
</style>

<script>
    export default {
        mounted() {
            this.$store.dispatch('reload_game', this.game_id);
        },
        computed: {
            game_id() {
                return this.$route.params.game_id;
            },
            game() {
                return this.$store.getters.get_game(this.game_id);
            }
        }
    }
</script>
