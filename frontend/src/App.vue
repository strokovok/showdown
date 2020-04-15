<template>
    <div id="app">
        <div class="nav-bar">
            <div class="title">Showdown.AI</div>
            <div class="empty-nav"></div>
            <div class="sections">
                <div class="section">Соревнования</div>
                <div class="section">Пользователи</div>
                <div class="section">Рейтинг</div>
                <div class="section">Игры</div>
                <div class="section">Профиль</div>
                <div class="section">Язык</div>
            </div>
        </div>
        <div class="content-panel">

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

    .content-panel {
        margin-top: 50px;
        width: 70%;
        height: 500px;
        background: $col-panel;
        /*box-shadow: 0 0 20px transparentize(black, 0.9);*/
    }

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
    }

    .empty-nav {
        flex-grow: 1;
    }

    .sections {
        display: flex;
        justify-content: center;
        flex-shrink: 0;
        /*flex-grow: 1;*/
    }

    .section {
        font-family: 'Source Sans Pro', sans-serif;
        color: $col-text;
        font-size: 18px;
        margin-left: 60px;
        cursor: pointer;
        padding-bottom: 5px;
        border-bottom: 3px $col-background solid;
        &:hover {
            border-bottom: 2px $col-text solid;
            transform: scale(1.05);
        }
        &:active {
            transform: scale(0.95);
        }
        transition: all .3s ease;
    }
</style>
