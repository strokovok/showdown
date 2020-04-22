<template>
    <div class="content-panel-container">
        <MatchPreview v-for="match in matches" :match="match" :key="match.id"></MatchPreview>
    </div>
</template>

<style lang="scss" scoped>

</style>

<script>
    import MatchPreview from "@/components/MatchPreview.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_game_matches', this.game_id);
        },
        computed: {
            game_id() {
                return this.$route.params.game_id;
            },
            matches() {
                return this.$store.getters.get_game_matches(this.game_id) || [];
            }
        },
        components: {
            MatchPreview
        }
    }
</script>
