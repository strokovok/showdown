<template>
    <div class="content-panel-container">
        <div class="content-panel">
            Здесь будет детальная информация об игре.
        </div>
    </div>
</template>

<style lang="scss" scoped>
</style>

<script>
    export default {
        mounted() {
            this.$store.dispatch("reload_game_details", this.$route.params.game_id);
        },
        computed: {
            game_details() {
                return this.$store.getters.games_details[this.$route.params.game_id];
            }
        }
    }
</script>
