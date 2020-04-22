<template>
    <div class="content-panel-container">
        <BotPreview v-for="bot in $store.getters.all_bots" :bot="bot" :key="bot.id" :show_game="true" :show_user="true"/>
    </div>
</template>

<style lang="scss" scoped>

</style>

<script>
    import BotPreview from "@/components/BotPreview.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_all_bots');
        },
        components: {
            BotPreview
        }
    }
</script>
