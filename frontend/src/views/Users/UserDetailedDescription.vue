<template>
    <div class="content-panel-container">
        <detailed-description
                v-if="user !== undefined"
                :text="user.detailed_description"
                :is_editable="is_editable"
                @on-change="on_change"
        />
    </div>
</template>

<script>
    import DetailedDescription from '@/components/DetailedDescription.vue';

    export default {
        computed: {
            user_id() {
                return this.$route.params.user_id;
            },
            user() {
                return this.$store.getters.get_user(this.user_id);
            },
            is_editable() {
                let cur_user = this.$store.getters.cur_user;
                if (cur_user === null || this.user === undefined)
                    return false;
                return cur_user.id === this.user.id;
            }
        },
        methods: {
            on_change(source) {
                this.$store.dispatch('update_user', {
                    id: this.user_id,
                    data: {
                        detailed_description: source
                    }
                });
            }
        },
        components: {
            DetailedDescription
        }
    }
</script>