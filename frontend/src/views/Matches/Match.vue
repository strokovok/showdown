<template>
    <div class="content-panel-container">
        <div class="content-panel-container" v-if="match !== undefined">
            <MatchPreview :match="match" :show_game="true"/>
            <div class="content-panel" v-if="game_log !== undefined">
                <div class="vis-container">
                    <transition-group name="game-log" class="game-log" tag="div">
                        <div class="game-log-item" v-for="i in (cur_frame + 1)" :key="i">
                            {{game_log[i - 1]}}
                        </div>
                    </transition-group>
                    <tic-tac-toe :game_log="game_log" :match="match" :cur_frame="cur_frame"/>
                </div>
                <div class="controls">
                    <div class="con-button" @click="on_play">Играть</div>
                    <div class="con-button" @click="on_stop">Стоп</div>
                    <input type="range"
                           min="0" max="100"
                           step="0.0000001"
                           v-model="progress"
                           class="progress-slider"
                           @mousedown="slider_mouse_down = true"
                           @mouseup="slider_mouse_down = false">
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .controls {
        margin-top: 30px;
        width: 100%;
        display: flex;
        align-items: center;
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
        margin-right: 30px;
        user-select: none;
    }

    .progress-slider {
        width: 580px;
        -webkit-appearance: none;
        appearance: none;
        height: 25px;
        background: transparentize($col-active, 0.6);
        outline: none;
        opacity: 0.7;
        -webkit-transition: .2s;
        transition: opacity .2s;
        &:hover {
            opacity: 1;
        }
    }

    .progress-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 25px;
        height: 25px;
        background: $col-active;
        cursor: pointer;
    }

    .progress-slider::-moz-range-thumb {
        width: 25px;
        height: 25px;
        background: $col-active;
        cursor: pointer;
    }

    .vis-container {
        display: flex;
    }

    .game-log {
        margin-right: 50px;
        width: 300px;
        height: 500px;
        overflow-y: scroll;
        background: $col-background;
        border: 1px transparentize($col-text, 0.5) solid;
        overflow-x: hidden;
    }

    .game-log-item {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px transparentize($col-text, 0.5) solid;
        box-sizing: border-box;

        transition: all .3s;
        margin-right: 10px;
    }
    .game-log-enter, .game-log-leave-to {
        opacity: 0;
        transform: translateX(30px);
    }
    .game-log-leave-active {
        opacity: 0;
    }
</style>

<script>
    import MatchPreview from "@/components/MatchPreview";
    import TicTacToe from "@/components/Games/TicTacToe";

    const STEP_SPEED = 0.1;

    export default {
        data() {
            return {
                cur_frame: -1,
                progress: 0,
                slider_mouse_down: false,
                play: true,
            }
        },
        mounted() {
            this.$store.dispatch('reload_match', this.match_id);
            setInterval(this.update_progress, 50);
        },
        methods: {
            on_play() {
                this.play = true;
                if (this.progress >= 100) {
                    this.progress = 0;
                }
            },
            on_stop() {
                this.play = false;
            },
            update_progress() {
                if (this.game_log === undefined)
                    return;
                this.progress = parseFloat(this.progress);
                if (!this.slider_mouse_down && this.play) {
                    let delta = (100 / this.game_log.length) * STEP_SPEED;
                    this.progress += delta;
                    this.progress = Math.min(this.progress, 100);
                }
                let next_frame = Math.floor((this.progress / 100) * this.game_log.length) - 1;
                if (next_frame !== this.cur_frame) {
                    this.cur_frame = next_frame;
                    this.$nextTick(() => {
                        let el = document.getElementsByClassName("game-log")[0];
                        el.scrollTop = el.scrollHeight;
                    })
                }
            }
        },
        computed: {
            match_id() {
                return this.$route.params.match_id;
            },
            match() {
                return this.$store.getters.get_match(this.match_id);
            },
            game_log() {
                if (this.match !== undefined)
                    return this.match.data.game_log;
                return undefined;
            }
        },
        components: {
            MatchPreview,
            TicTacToe
        }
    }
</script>
