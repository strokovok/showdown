<template>
    <div id="app">
        <!--<div class="title">Showdown.AI</div>-->
        <div class="title">Showdown.AI</div>
        <div class="sections">
            <div class="section">Соревнования</div>
            <div class="section">Пользователи</div>
            <div class="section">Рейтинг</div>
            <div class="section">Игры</div>
            <div class="section">Профиль</div>
            <div class="section">Язык</div>
        </div>
        <!--<div id="nav">-->
            <!--<router-link to="/">Home</router-link>-->
            <!--|-->
            <!--<router-link to="/about">About</router-link>-->
        <!--</div>-->
        <!--<router-view/>-->
    </div>
</template>

<style lang="scss">
    #app {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .title {
        color: $col-header;
        font-family: 'Oxygen', sans-serif;
        font-size: 34px;
        margin-top: 30px;
        cursor: pointer;
        transition: all .5s ease;
        &:hover {
            letter-spacing: 0.1em;
        }
        &:active {
            transition: all .3s ease;
            letter-spacing: 0.02em;
        }
        user-select: none;
    }

    .sections {
        margin-top: 30px;
        display: flex;
    }

    .section {
        color: $col-header;
        font-family: "Source Sans Pro", sans-serif;
        display: flex;
        font-size: 20px;
        margin-left: 20px;
        margin-right: 20px;
        padding: 0.3em 0.5em;
        transition: all .3s ease;
        cursor: pointer;
        &:hover {
            background: $col-panel;
            transform: scale(1.15);
        }
        &:active {
            background: transparentize($col-panel, 0.5);
            transform: scale(1.05);
        }
        user-select: none;
    }
</style>
