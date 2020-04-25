<template>
    <div id="app">
        <nav-bar/>
        <div class="content-container">
            <router-view/>
        </div>
    </div>
</template>

<style lang="scss">
    #app {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .content-container {
        margin-top: 50px;
        width: 70%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>

<script>
    import NavBar from '@/components/NavBar.vue';

    export default {
        mounted() {
            this.$store.dispatch('reload_auth');
        },
        components: {
            NavBar
        }
    }
</script>