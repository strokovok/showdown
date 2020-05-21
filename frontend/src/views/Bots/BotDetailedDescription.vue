<template>
    <div class="content-panel-container">
        <detailed-description
                v-if="bot !== undefined"
                :text="bot.detailed_description"
                :is_editable="is_editable"
                @on-change="on_change"
        />
    </div>
</template>

<script>
    import DetailedDescription from '@/components/DetailedDescription.vue';

    export default {
        computed: {
            bot_id() {
                return this.$route.params.bot_id;
            },
            bot() {
                return this.$store.getters.get_bot(this.bot_id);
            },
            is_editable() {
                let user = this.$store.getters.cur_user;
                if (user === null || this.bot === undefined)
                    return false;
                return user.id === this.bot.owner_id;
            }
        },
        methods: {
            on_change(source) {
                this.$store.dispatch('update_bot', {
                    id: this.bot_id,
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