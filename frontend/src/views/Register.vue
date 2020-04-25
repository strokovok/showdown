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
            <div class="input-element">
                <div class="input-title">Повторите пароль:</div>
                <input class="oneline-input" type="password" v-model="password_repeat">
            </div>
            <div class="form-error" v-if="form_error !== null">
                {{form_error}}
            </div>
            <button class="continue-button" @click="register">Зарегистрироваться</button>
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

    const LOGIN_ALREADY_EXISTS = 302;

    export default {
        data() {
            return {
                login: "",
                password: "",
                password_repeat: "",
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
                if (this.password_repeat !== this.password) {
                    this.form_error = "Введённые пароли не совпадают";
                    return;
                }

                axios.post('/api/auth/register', {
                    login: this.login,
                    password: this.password
                }).then(response => {
                    this.$store.dispatch("set_user", response.data);
                    this.$router.push("/");
                }).catch(err => {
                    if (err.response.data.error.code === LOGIN_ALREADY_EXISTS) {
                        this.form_error = "Этот логин уже занят";
                        return;
                    }
                    this.form_error = err.response.data.error.message;
                    console.log(err.response);
                });
            }
        }
    }
</script>