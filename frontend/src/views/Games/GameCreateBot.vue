<template>
    <div class="content-panel-container">
        <div class="content-panel" v-if="logged_in">
            <div class="input-form">
                <div class="input-element">
                    <div class="input-title">Название бота:</div>
                    <input class="oneline-input" type="text" v-model="name">
                </div>
                <div class="form-error" v-if="form_error !== null">
                    {{form_error}}
                </div>
                <button class="continue-button" @click="create_bot">Создать</button>
            </div>
        </div>
        <div class="content-panel" v-else>
            Войдите или зарегистрируйтесь чтобы создавать ботов.
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .input-form {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .input-element {
        display: flex;
        align-items: center;
        margin-top: 20px;
        &:first-child {
            margin-top: 0;
        }
    }

    .input-title {
        margin-right: 1em;
    }

    .form-error {
        margin-top: 40px;
        width: 100%;
        text-align: center;
        color: $col-danger;
    }
</style>

<script>
    const axios = require('axios');

    const BOT_NAME_ALREADY_EXISTS = 502;

    export default {
        data() {
            return {
                name: "",
                form_error: null,
            }
        },
        methods: {
            create_bot() {
                this.form_error = null;
                if (this.name.length < 1 || this.name.length > 30) {
                    this.form_error = "Длина имени бота должна быть от 1 до 30";
                    return;
                }
                axios.post('/api/bots/create', {
                    name: this.name,
                    game_id: parseInt(this.$route.params.game_id)
                }).then(response => {
                    let bot_id = response.data.bot.id;
                    this.$router.push("/bots/" + bot_id);
                }).catch(err => {
                    if (err.response.data.error.code === BOT_NAME_ALREADY_EXISTS) {
                        this.form_error = "Бот с таким именем уже существует";
                        return;
                    }
                    this.form_error = err.response.data.error.message;
                    console.log(err.response);
                });
            }
        },
        computed: {
            logged_in() {
                return this.$store.getters.cur_user !== null;
            }
        }
    }
</script>
