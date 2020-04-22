<template>
    <div class="content-panels-row">
        <card-link img="/game.png"
                   :title="bot.game.name"
                   :to="`/games/${bot.game.id}`"
                   class="card"
                   v-if="show_game"/>
        <card-link img="/user.png"
                   :title="bot.owner.login"
                   :to="`/users/${bot.owner.id}`"
                   class="card"
                   v-if="show_user"/>
        <router-link :to="`/bots/${bot.id}`" class="content-panel panel-link bot-preview">
            <div :to="`/bots/${bot.id}`" class="bot">
                <img class="bot-logo" src="/bot.png">
                <div class="bot-name">{{bot.name}}</div>
            </div>
            <div class="rank">
                {{bot.rank}}
                <img class="rank-img" src="/rank.png">
            </div>
        </router-link>
    </div>
</template>

<style lang="scss" scoped>
    .card {
        width: 123.5px;
        height: 123.5px;
        font-size: 14px;
    }

    .bot-preview {
        flex-grow: 1;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        &:hover {
            transform: none;
        }
    }

    .bot {
        display: flex;
        align-items: center;
    }

    .bot-logo {
        width: 70px;
        height: 70px;
    }

    .bot-name {
        margin-left: 15px;
    }

    .rank {
        color: $col-active;
        display: flex;
        align-items: center;
    }

    .rank-img {
        margin-bottom: 0.1em;
        margin-left: 0.3em;
        width: 1em;
    }
</style>

<script>
    import CardLink from "@/components/CardLink.vue";

    export default {
        props: {
            bot: Object,
            show_game: Boolean,
            show_user: Boolean
        },
        components: {
            CardLink
        }
    }
</script>