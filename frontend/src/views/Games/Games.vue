<template>
    <div class="games">
        <card-link v-for="game in games"
                   img="/game.png"
                   :title="game.name"
                   :to="`/games/${game.id}`"
                   :key="game.id"
                   class="game"/>
    </div>
</template>

<style lang="scss" scoped>
    .games {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }

    .game {
        width: 200px;
        height: 200px;
        margin: 10px;
    }
</style>

<script>
    import CardLink from "@/components/CardLink.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_games_list', "");
        },
        computed: {
            games() {
                return this.$store.getters.get_games_list("") || [];
            }
        },
        components: {
            CardLink
        }
    }
</script>
