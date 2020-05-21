<template>
    <div class="content-panel-container">
        <detailed-description
                v-if="game !== undefined"
                :text="game.detailed_description"
        />
    </div>
</template>

<script>
    import DetailedDescription from '@/components/DetailedDescription.vue';

    export default {
        computed: {
            game_id() {
                return this.$route.params.game_id;
            },
            game() {
                return this.$store.getters.get_game(this.game_id);
            }
        },
        components: {
            DetailedDescription
        }
    }
</script>