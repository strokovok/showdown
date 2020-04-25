<template>
    <div class="content-panel-container">
        <MatchPreview v-for="match in matches"
                      :match="match"
                      :key="match.id"
                      :show_game="show_game"
                      :prefer_left_bot_id="prefer_left_bot_id"
                      :prefer_left_user_id="prefer_left_user_id"/>
    </div>
</template>

<script>
    import MatchPreview from "@/components/MatchPreview.vue";

    export default {
        props: {
            show_game: { default: false },
            prefer_left_bot_id: { default: null },
            prefer_left_user_id: { default: null },
            query: { default: "" }
        },
        mounted() {
            this.$store.dispatch('reload_matches_list', this.query);
        },
        computed: {
            matches() {
                return this.$store.getters.get_matches_list(this.query) || [];
            }
        },
        components: {
            MatchPreview
        }
    }
</script>
