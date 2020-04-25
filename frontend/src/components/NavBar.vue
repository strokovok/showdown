<template>
    <div class="nav-bar">
        <router-link to="/" class="title">Showdown.AI</router-link>
        <div class="empty-nav"></div>
        <div class="sections">
            <router-link to="/games" class="navigation-link-nonexact">Соревнования</router-link>
            <router-link to="/users" class="navigation-link-nonexact">Пользователи</router-link>
            <router-link to="/bots" class="navigation-link-nonexact">Боты</router-link>
            <router-link to="/matches" class="navigation-link-nonexact">Матчи</router-link>

            <router-link to="/register" class="navigation-link-nonexact" v-if="!logged_in">Регистрация</router-link>
            <router-link to="/login" class="navigation-link-nonexact" v-if="!logged_in">Войти</router-link>

            <router-link :to="profile_link" class="navigation-link" v-if="logged_in">Профиль</router-link>
            <div class="navigation-link-nonexact" v-if="logged_in" @click="logout">Выйти</div>
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
        methods: {
            logout() {
                this.$store.dispatch("logout");
            }
        },
        computed: {
            logged_in() {
                return this.$store.getters.cur_user !== null;
            },
            profile_link() {
                let cur_user = this.$store.getters.cur_user;
                if (cur_user === null)
                    return "/";
                return `/users/${cur_user.id}`;
            }
        }
    }
</script>