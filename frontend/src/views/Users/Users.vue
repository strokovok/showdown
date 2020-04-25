<template>
    <div class="users">
        <card-link v-for="user in users"
                   img="/user.png"
                   :title="user.login"
                   :to="`/users/${user.id}`"
                   :key="user.id"
                   class="user"/>
    </div>
</template>

<style lang="scss" scoped>
    .users {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }

    .user {
        width: 200px;
        height: 200px;
        margin: 10px;
    }
</style>

<script>
    import CardLink from "@/components/CardLink.vue";

    export default {
        mounted() {
            this.$store.dispatch('reload_users_list', "");
        },
        computed: {
            users() {
                return this.$store.getters.get_users_list("") || [];
            }
        },
        components: {
            CardLink
        }
    }
</script>
