<template>
    <div class="nav-bar">
        <router-link to="/" class="title">Showdown.AI</router-link>
        <div class="empty-nav"></div>
        <div class="sections">
            <router-link to="/games" class="navigation-link-nonexact">Соревнования</router-link>
            <router-link to="/users" class="navigation-link-nonexact">Пользователи</router-link>
            <router-link to="/bots" class="navigation-link-nonexact">Боты</router-link>
            <router-link to="/profile" class="navigation-link-nonexact">Профиль</router-link>
            <router-link to="/logout" class="navigation-link-nonexact">Выйти</router-link>
<!--            <div class="navigation-link-nonexact">Язык</div>-->
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .nav-bar {
        width: 69%;
        margin-top: 30px;
        display: flex;
        align-items: flex-end;
    }

    .title {
        font-family: 'Oxygen', sans-serif;
        color: $col-text;
        font-size: 34px;
        font-weight: 700;
        flex-shrink: 0;
        &:hover {
            transform: scale(1.05);
        }
        &:active {
            transform: scale(0.95);
        }
        transition: all .3s ease;
        cursor: pointer;
        text-decoration: none;
    }

    .empty-nav {
        flex-grow: 1;
    }

    .sections {
        display: flex;
        flex-shrink: 0;
    }
</style>

<script>
    export default {

    }
</script>