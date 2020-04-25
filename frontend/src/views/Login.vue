<template>
    <div class="content-panel">
        <div class="input-form">
            <div class="input-element">
                <div class="input-title">Логин:</div>
                <input class="oneline-input" type="text" v-model="login">
            </div>
            <div class="input-element">
                <div class="input-title">Пароль:</div>
                <input class="oneline-input" type="password" v-model="password">
            </div>
            <div class="form-error" v-if="form_error !== null">
                {{form_error}}
            </div>
            <button class="continue-button" @click="register">Войти</button>
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

    const INCORRECT_LOGIN = 301;
    const INCORRECT_PASSWORD = 202;

    export default {
        data() {
            return {
                login: "",
                password: "",
                form_error: null
            }
        },
        methods: {
            register() {
                this.form_error = null;
                if (this.login.length < 1 || this.login.length > 30) {
                    this.form_error = "Длина логина должна быть от 1 до 30";
                    return;
                }
                if (this.password.length < 1 || this.password.length > 30) {
                    this.form_error = "Длина пароля должна быть от 1 до 100";
                    return;
                }

                axios.post('/api/auth/login', {
                    login: this.login,
                    password: this.password
                }).then(response => {
                    this.$store.dispatch("set_user", response.data);
                    this.$router.push("/");
                }).catch(err => {
                    if (err.response.data.error.code === INCORRECT_LOGIN) {
                        this.form_error = "Пользователя с таким логином не существует";
                        return;
                    }
                    if (err.response.data.error.code === INCORRECT_PASSWORD) {
                        this.form_error = "Неправильный пароль";
                        return;
                    }
                    this.form_error = err.response.data.error.message;
                    console.log(err.response);
                });
            }
        }
    }
</script>