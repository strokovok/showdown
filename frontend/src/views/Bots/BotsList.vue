<template>
    <div class="content-panel-container">
        <BotPreview v-for="bot in bots" :bot="bot" :key="bot.id" :show_game="show_game" :show_user="show_user"/>
    </div>
</template>

<script>
    import BotPreview from "@/components/BotPreview.vue";

    export default {
        props: {
            show_game: { default: false },
            show_user: { default: false },
            query: { default: "" }
        },
        mounted() {
            this.$store.dispatch('reload_bots_list', this.query);
        },
        computed: {
            bots() {
                return this.$store.getters.get_bots_list(this.query) || [];
            }
        },
        components: {
            BotPreview
        }
    }
</script>
