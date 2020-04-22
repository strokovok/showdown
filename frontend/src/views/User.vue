<template>
    <div class="content-panel-container">
        <div class="content-panel short-info-panel" v-if="user !== undefined">
            <img class="user-logo" src="/user.png">
            <div class="short-info">
                <div class="user-name">{{user.login}}</div>
                <div class="user-short-descr">Здесь будет краткая информация.</div>
            </div>
        </div>
        <BotPreview v-for="bot in bots" :bot="bot" :key="bot.id" :show_game="true" :show_user="false"/>
    </div>
</template>

<style lang="scss" scoped>

    .short-info-panel {
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
    }

    .user-logo {
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

    .user-name {
        font-size: 24px;
        font-weight: 600;
    }

    .user-short-descr {
        margin-top: 8px;
        font-size: 18px;
    }
</style>

<script>
    import BotPreview from "@/components/BotPreview.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_user', this.user_id);
            this.$store.dispatch('reload_user_bots', this.user_id);
        },
        computed: {
            user_id() {
                return this.$route.params.user_id;
            },
            user() {
                return this.$store.getters.get_user(this.user_id);
            },
            bots() {
                return this.$store.getters.get_user_bots(this.user_id) || [];
            }
        },
        components: {
            BotPreview
        }
    }
</script>
