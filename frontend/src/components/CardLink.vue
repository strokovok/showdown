<template>
    <router-link class="content-panel panel-link card-link" :to="to">
        <img class="logo" :src="img">
        <div class="title">{{title}}</div>
    </router-link>
</template>

<style lang="scss" scoped>
    .card-link {
        width: unset;
        justify-content: center;
    }

    .logo {
        width: 65%;
        height: 65%;
    }

    .title {
        margin-top: 1em;
        text-align: center;
    }
</style>

<script>
    export default {
        props: {
            img: String,
            title: String,
            to: String
        }
    }
</script>