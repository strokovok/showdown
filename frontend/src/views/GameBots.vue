<template>
    <div class="content-panel-container">
        <BotPreview v-for="bot in bots" :bot="bot" :key="bot.id" :show_game="false" :show_user="true"/>
    </div>
</template>

<style lang="scss" scoped>
</style>

<script>
    import BotPreview from "@/components/BotPreview.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_game_bots', this.game_id);
        },
        computed: {
            game_id() {
                return this.$route.params.game_id;
            },
            bots() {
                return this.$store.getters.get_game_bots(this.game_id) || [];
            }
        },
        components: {
            BotPreview
        }
    }
</script>
