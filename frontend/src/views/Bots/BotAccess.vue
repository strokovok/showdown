<template>
    <div class="content-panel-container">
        <div class="content-panel">
            <div class="input-form">
                <div class="input-element">
                    <div class="input-title">Токен доступа:</div>
                    <input class="oneline-input" type="text" v-model="token" readonly>
                </div>
                <div class="form-error" v-if="form_error !== null">
                    {{form_error}}
                </div>
                <button class="continue-button" @click="renew_token">Генерировать токен</button>
            </div>
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

    export default {
        data() {
            return {
                token: "•••••••••••••••",
                form_error: null,
            }
        },
        methods: {
            renew_token() {
                this.form_error = null;
                axios.get(`/api/bots/${this.bot_id}/renew_token`
                ).then(response => {
                    this.token = response.data.access_token;
                }).catch(err => {
                    this.form_error = err.response.data.error.message;
                    console.log(err.response);
                });
            }
        },
        computed: {
            bot_id() {
                return this.$route.params.bot_id;
            }
        }
    }
</script>
