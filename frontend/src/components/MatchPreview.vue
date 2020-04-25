<template>
    <div class="content-panels-row">
        <card-link img="/game.png"
                   :title="match.game.name"
                   :to="`/games/${match.game.id}`"
                   class="card"
                   v-if="show_game"/>
        <div class="content-panel match-preview">
            <div class="participant participant-left">
                <router-link :to="`/bots/${left.id}`" class="bot jump-link">
                    <img class="bot-logo" src="/bot.png">
                    <div class="bot-name">{{left.name}}</div>
                </router-link>
                <router-link :to="`/users/${left.owner.id}`" class="user jump-link">
                    <img class="user-logo" src="/user.png">
                    <div class="user-login">{{left.owner.login}}</div>
                </router-link>
            </div>
            <router-link :to="`/matches/${match.id}`" class="jump-link">
                Перейти к матчу
            </router-link>
            <div class="participant participant-right">
                <router-link :to="`/bots/${right.id}`" class="bot jump-link">
                    <div class="bot-name">{{right.name}}</div>
                    <img class="bot-logo" src="/bot.png">
                </router-link>
                <router-link :to="`/users/${right.owner.id}`" class="user jump-link">
                    <div class="user-login">{{right.owner.login}}</div>
                    <img class="user-logo" src="/user.png">
                </router-link>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .card {
        width: 123.5px;
        height: 123.5px;
        font-size: 14px;
    }

    .match-preview {
        flex-direction: row;
        justify-content: space-between;
        flex-grow: 1;
    }

    .participant {
        display: flex;
        flex-direction: column;
    }

    .participant-left {
        align-items: flex-start;
    }

    .participant-right {
        align-items: flex-end;
    }

    .bot {
        display: flex;
        align-items: center;
    }

    .bot-logo {
        width: 50px;
        height: 50px;
    }

    .bot-name {
        margin-left: 10px;
        margin-right: 10px;
    }

    .user {
        margin-top: 10px;
        display: flex;
        align-items: center;
    }

    .user-logo {
        width: 25px;
        height: 25px;
        margin-left: 12.5px;
        margin-right: 12.5px;
    }

    .user-login {
        font-size: 14px;
        margin-left: 10px;
        margin-right: 10px;
    }
</style>

<script>
    import CardLink from "@/components/CardLink.vue";

    export default {
        props: {
            match: Object,
            show_game: { default: false },
            prefer_left_bot_id: { default: null },
            prefer_left_user_id: { default: null }
        },
        computed: {
            participants() {
                let first = this.match.participants[0], second = this.match.participants[1];

                if (this.prefer_left_bot_id === null && this.prefer_left_user_id === null)
                    return [first, second];

                if (this.prefer_left_bot_id !== null && this.prefer_left_bot_id.toString() === first.id.toString())
                    return [first, second];

                if (this.prefer_left_user_id !== null && this.prefer_left_user_id.toString() === first.owner_id.toString())
                    return [first, second];

                return [second, first];
            },
            left() {
                return this.participants[0];
            },
            right() {
                return this.participants[1];
            }
        },
        components: {
            CardLink
        }
    }
</script>