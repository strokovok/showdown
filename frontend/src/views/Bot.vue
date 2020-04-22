<template>
    <div class="content-panel-container">
        <div class="content-panel short-info-panel" v-if="bot !== undefined">
            <img class="bot-logo" src="/bot.png">
            <div class="short-info">
                <div class="bot-name">{{bot.name}}</div>
                <div class="bot-short-descr">Здесь будет краткая информация.</div>
            </div>
        </div>
        <MatchPreview v-for="match in matches" :match="match" :key="match.id"></MatchPreview>
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
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }

    .bot-name {
        font-size: 24px;
        font-weight: 600;
    }

    .bot-short-descr {
        margin-top: 8px;
        font-size: 18px;
    }
</style>

<script>
    import MatchPreview from "@/components/MatchPreview.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_bot', this.bot_id);
            this.$store.dispatch('reload_bot_matches', this.bot_id);
        },
        computed: {
            bot_id() {
                return this.$route.params.bot_id;
            },
            bot() {
                return this.$store.getters.get_bot(this.bot_id);
            },
            matches() {
                return this.$store.getters.get_bot_matches(this.bot_id) || [];
            }
        },
        components: {
            MatchPreview
        }
    }
</script>
