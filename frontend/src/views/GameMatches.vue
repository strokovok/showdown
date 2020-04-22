<template>
    <div class="content-panel-container">
        <MatchPreview v-for="match in matches" :match="match"></MatchPreview>
    </div>
</template>

<style lang="scss" scoped>

</style>

<script>
    import MatchPreview from "@/components/MatchPreview";

    export default {
        mounted() {
            this.$store.dispatch("reload_game_matches", this.$route.params.game_id);
        },
        computed: {
            game() {
                return this.$store.getters.games_matches[this.$route.params.game_id];
            },
            matches() {
                if (this.game === undefined)
                    return [];
                return this.game.matches;
            }
        },
        components: {
            MatchPreview
        }
    }
</script>
