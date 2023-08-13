<template>
    <div class="radio-container">
        <div class="tabs">
            <label class="tab info"> {{ info }} </label>
            <div v-for="(item, index) in items" :key="index">
                <input type="radio" :id="uid + index" :value="item.value" v-model="model">
                <label class="tab" :for="uid + index" @click="changeSelect(index)"> {{ item.label }}</label>
            </div>
            <span class="glider" :style="`--radio-index: ${select};`"></span>
        </div>
    </div>
</template>

<script>

export default {
    props: {
        uid: String,
        info: String,
        initModel: Number,
        initSelect: Number,
        items: Array,
    },
    data() {
        return {
            model: this.initModel,
            select: this.initSelect ? this.initSelect : 1,
        }
    },
    watch: {
        model(newVal) {
            this.$emit('option-selected', newVal);
        }
    },
    methods: {
        changeSelect(index) {
            this.select = index + 1;
        }
    }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap");


*,
*:after,
*:before {
    box-sizing: border-box;
}

.radio-container {
    font-family: "Inter", sans-serif;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    margin: 5px;
}

.tabs {
    display: flex;
    position: relative;
    background-color: #bcebd0;
    box-shadow: 0 0 1px 0 rgba(#185ee0, 0.15), 0 6px 12px 0 rgba(#185ee0, 0.15);
    padding: 0.75rem;
    border-radius: 49px;

    * {
        z-index: 2;
    }
}


input[type="radio"] {
    display: none;
}

.tab {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 34px;
    width: 150px;
    font-size: 1.25rem;
    font-weight: 500;
    border-radius: 49px;
    cursor: pointer;
    transition: color 0.15s ease-in;
}

.info {
    width: 150px;
    font-weight: bold;
    border-radius: 0;
    border-right: 2px solid white;
    border: left;
}

.glider {
    position: absolute;
    display: flex;
    height: 34px;
    width: 150px;
    background-color: rgba(140, 242, 138, 0.3);
    z-index: 1;
    border-radius: 99px;
    transition: 0.15s ease-out;
    transform: translateX(calc(100% * var(--radio-index)));
}

@media (max-width: 700px) {
    .tabs {
        transform: scale(0.6);
    }
}
</style>
