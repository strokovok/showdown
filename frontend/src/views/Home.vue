<template>
    <div class="content-panel">
        <div class="welcome">Добро пожаловать!</div>
        <img class="showdown-img" src="/showdown.png">
        Showdown.AI - это платформа для проведения соревнований по программированию ИИ.<br>
        Здесь участники разрабатывают игровой ИИ и подключают его к системе соревнований, после чего происходит игра. <br>
        Присоединяйтесь к соревнованиям или наблюдайте за играми!
<!--        Наблюдайте за прошедшими соревнованиями и рейтингом игровых ботов.<br>-->
<!--        Или присоединяйтесь к соревнованиям.<br>-->
    </div>
</template>

<style lang="scss" scoped>
    .content-panel {
        align-items: center;
        text-align: center;
        line-height: 1.5em;
    }

    .welcome {
        font-size: 1.1em;
    }

    .showdown-img {
        margin-top: 20px;
        width: 40%;
    }
</style>

<script>
    import VueMarkdown from 'vue-markdown';

    export default {
        components: {
            VueMarkdown
        }
    }
</script>
