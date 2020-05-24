<template>
    <div class="content-panel">
        <textarea v-if="edit_view" v-model="source" class="editor"></textarea>
        <vue-markdown style="width: 100%" v-else :source="edit_mode ? source : text" :postrender="do_postrender"></vue-markdown>

        <div class="con-buttons">
            <button class="con-button" v-if="is_editable && !edit_mode" @click="on_edit">Редактировать</button>
            <button class="con-button" v-if="edit_mode && edit_view" @click="edit_view=false">Смотреть</button>
            <button class="con-button" v-if="edit_mode && !edit_view" @click="edit_view=true">Править</button>
            <button class="con-button" v-if="edit_mode" @click="on_save">Сохранить</button>
            <button class="con-button" v-if="edit_mode" @click="on_cancel">Отменить</button>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    @import '../../node_modules/prismjs/themes/prism.css';

    .editor {
        width: calc(100% - 50px);
        height: 400px;

        background: $col-background;
        outline: none;
        padding: 0.4em 0.5em;
        border: 2px transparentize($col-active, 0.7) solid;
        color: $col-text;
        &:focus {
            border-color: $col-active;
        }
        transition: all .3s ease;
        resize: none;
    }

    .con-buttons {
        margin-top: 10px;
        width: 100%;
        display: flex;
        justify-content: center;
    }

    .con-button {
        padding: 0.4em 0.5em;
        border: 2px transparentize($col-active, 0.7) solid;
        background: transparentize($col-active, 0.8);
        &:hover {
            background: transparentize($col-active, 0.5);
        }
        &:active {
            transform: scale(0.95);
        }
        transition: all .3s ease;
        cursor: pointer;
        outline: none;
        color: $col-text;
        margin-left: 10px;
        margin-right: 10px;
        user-select: none;
    }
</style>

<script>
    import VueMarkdown from 'vue-markdown';

    import Prism from 'prismjs';
    import "prismjs/components/prism-python";
    import "prismjs/components/prism-csharp";
    import "prismjs/components/prism-go";
    import "prismjs/components/prism-java";
    import "prismjs/components/prism-c";
    import "prismjs/components/prism-cpp";
    import "prismjs/components/prism-kotlin";
    import "prismjs/components/prism-json";

    export default {
        props: {
            text: { default: "" },
            is_editable: { default: false }
        },
        data() {
            return {
                source: '',
                edit_mode: false,
                edit_view: false,
            }
        },
        methods: {
            on_edit() {
                this.edit_mode = true;
                this.edit_view = true;
                this.source = this.text;
            },
            on_save() {
                this.edit_mode = false;
                this.edit_view = false;
                this.$emit('on-change', this.source);
            },
            on_cancel() {
                this.edit_mode = false;
                this.edit_view = false;
            },
            do_postrender(res) {
                this.$nextTick(() => {
                    Prism.highlightAll();
                });
                return res;
            }
        },
        components: {
            VueMarkdown
        }
    }
</script>
