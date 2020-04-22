<template>
    <div class="content-panel-container">
        <div class="content-panel">
            Боты: {{game_bots}}
        </div>
    </div>
</template>

<style lang="scss" scoped>
</style>

<script>
    export default {
        mounted() {
            this.$store.dispatch("reload_game_bots", this.$route.params.game_id);
        },
        computed: {
            game_bots() {
                return this.$store.getters.games_bots[this.$route.params.game_id];
            }
        }
    }
</script>
