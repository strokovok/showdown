<template>
    <div class="content-panel-container">
        <div class="content-panel short-info-panel" v-if="bot !== undefined">
            <img class="bot-logo" src="/bot.png">
            <div class="short-info">
                <div class="info-section">
                    <div class="bot-name">{{bot.name}}</div>
                    <div class="bot-short-descr">Здесь будет краткая информация.</div>
                </div>
                <div class="info-section-right">
                    <router-link :to="`/users/${bot.owner.id}`" class="user jump-link">
                        <div class="user-login">{{bot.owner.login}}</div>
                        <img class="user-logo" src="/user.png">
                    </router-link>
                    <div class="rank">
                        {{bot.rank}}
                        <img class="rank-img" src="/rank.png">
                    </div>
                </div>
            </div>
        </div>
        <div class="subnav">
            <router-link :to="`/bots/${bot_id}/`" class="navigation-link-exact">Детали</router-link>
            <router-link :to="`/bots/${bot_id}/matches`" class="navigation-link-exact">Матчи</router-link>
        </div>
        <router-view/>
    </div>
</template>

<style lang="scss" scoped>
    .short-info-panel {
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
    }

    .bot-logo {
        width: 100px;
        height: 100px;
        flex-shrink: 0;
    }

    .short-info {
        margin-left: 30px;
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .info-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }

    .info-section-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .bot-name {
        font-size: 24px;
        font-weight: 600;
    }

    .bot-short-descr {
        margin-top: 8px;
        font-size: 18px;
    }

    .rank {
        margin-top: 30px;
        color: $col-active;
        display: flex;
        align-items: center;
    }

    .rank-img {
        margin-bottom: 0.1em;
        margin-left: 0.3em;
        width: 1em;
    }

    .user {
        display: flex;
        align-items: center;
    }

    .user-logo {
        width: 30px;
        height: 30px;
        margin-left: 10px;
    }

    .user-login {
        font-size: 16px;
    }
</style>

<script>
    export default {
        mounted() {
            this.$store.dispatch('reload_bot', this.bot_id);
        },
        computed: {
            bot_id() {
                return this.$route.params.bot_id;
            },
            bot() {
                return this.$store.getters.get_bot(this.bot_id);
            }
        }
    }
</script>
