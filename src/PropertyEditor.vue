<template>
    <div class="property-editor">

        <div class="top row">
            <div class="grid" v-for="item in gridInfo.top" @click="edgeClickHandler($event, item)"></div>
        </div>

        <div class="left col">
            <div class="grid" v-for="item in gridInfo.left" @click="edgeClickHandler($event, item)"></div>
        </div>

        <div class="bottom row">
            <div class="grid" v-for="item in gridInfo.bottom" @click="edgeClickHandler($event, item)"></div>
        </div>

        <div class="right col">
            <div class="grid" v-for="item in gridInfo.right" @click="edgeClickHandler($event, item)"></div>
        </div>

        <div class="property">
            <span class="text">grid_value</span>
            <input class="property-input" type="number" step="0.001" @change="gridValueChangeHandler"
                v-model="gridClone.height" :class="{ 'disabled': !gridClone.height }" :disabled="!gridClone.height">
            <span class="text">edge_value</span>
            <input class="property-input" type="number" step="0.001" @change="edgeValueChangeHandler"
                :disabled="!clickedEdge" :class="{ 'disabled': !clickedEdge }" v-model="inputNum">
        </div>

    </div>
</template>

<script setup>
import { onMounted, watch, ref, toRaw, reactive } from 'vue';

const inputNum = ref(null)
const edgeValues = new Map()

let clickedEdgeDom = null
let clickedEdge = null
// gridlayer -- edgeRecoder --> getEdgeBykey
// gridNode -- edges -- keys

const gridClone = ref({})
const gridInfo = reactive({
    top: [],
    left: [],
    bottom: [],
    right: []
})

const props = defineProps({
    grid: {
        type: Object,
        default: {}
    },
    update: {
        type: Function,
        default: () => { }
    },
    getEdge: {
        type: Function,
        default: () => { }
    }
})

const refresh = () => {
    inputNum.value = null
    gridClone.value = null
    edgeValues.clear()
    if (clickedEdgeDom) {
        clickedEdgeDom.classList.remove('clicked')
        clickedEdgeDom = null
    }
    clickedEdge = null
}

watch(props.grid, (v) => {
    refresh()

    parseEdges(v.edges)
    gridClone.value = v
    console.log(gridClone.value)

})
const reset = () => {
    gridInfo.top = []
    gridInfo.bottom = []
    gridInfo.left = []
    gridInfo.right = []
}

const parseEdges = (v) => {
    reset()
    const array = toRaw(v)
    const t = array[0]
    const l = array[1]
    const b = array[2]
    const r = array[3]

    for (let edge of t) {
        gridInfo.top.push(edge)
        edgeValues.set(edge, props.getEdge(edge).height)
    }
    for (let edge of l) {
        gridInfo.left.push(edge)
        edgeValues.set(edge, props.getEdge(edge).height)
    }
    for (let edge of b) {
        gridInfo.bottom.push(edge)
        edgeValues.set(edge, props.getEdge(edge).height)
    }
    for (let edge of r) {
        gridInfo.right.push(edge)
        edgeValues.set(edge, props.getEdge(edge).height)
    }

}

const gridValueChangeHandler = () => {
    if (Number.isNaN(parseFloat(gridClone.value.height))) {
        gridClone.value.height = -9999
    }
}
const edgeValueChangeHandler = () => {

    edgeValues.set(clickedEdge, inputNum.value)

    props.update({
        edgeValues: edgeValues
    })
}



const edgeClickHandler = (event, edge) => {
    if (clickedEdgeDom) {
        clickedEdgeDom.classList.remove('clicked')

    }
    clickedEdgeDom = event.target
    clickedEdgeDom.classList.add('clicked')
    clickedEdge = edge

    inputNum.value = props.getEdge(clickedEdge).height
}


onMounted(() => {
    console.log("property editor mounted")
})

</script>

<style scoped>
div.property-editor {
    /* top: 100px;
    left: 100px; */
    position: absolute;
    width: 150px;
    height: 150px;
    background-color: transparent;
    z-index: 10;
    user-select: none;
    --wwidth: 15px;
    --hheight: 120px;
    --edgeSize: 25px;
    --edgeHeight: 15px;
}

div.property {
    position: absolute;
    left: var(--wwidth);
    top: var(--wwidth);
    width: var(--hheight);
    height: var(--hheight);
    background-color: rgb(64, 101, 120);
    display: grid;
    place-items: center;
}

div.property>.property-input {
    width: 70px;
    height: 20px;
    font-size: 16px;
    background-color: #e6fcff;
    border-radius: 6px;
    border: #e6fcff solid 2px;
    font-family: sans-serif;
    outline: none;
}

div.property>.property-input.disabled {
    cursor: not-allowed;
}

div.property>.property-input:focus {
    outline: none;
    border: rgb(255, 175, 175) solid 2px;
}

.text {
    position: relative;
    font-family: sans-serif;
    font-size: 16px;
    color: whitesmoke;
}


div.top {
    position: absolute;
    top: 0px;
    left: var(--wwidth);
    height: var(--wwidth);
    width: var(--hheight);
    background-color: #d8ffef;
}

div.left {
    position: absolute;
    top: var(--wwidth);
    left: 0;
    height: var(--hheight);
    width: var(--wwidth);
    background-color: #d8ffef;
}

div.right {
    position: absolute;
    top: var(--wwidth);
    /* right: 0; */
    right: 0;
    height: var(--hheight);
    width: var(--wwidth);
    background-color: #d8ffef;

}

div.bottom {
    position: absolute;
    bottom: 0px;
    left: var(--wwidth);
    height: var(--wwidth);
    width: var(--hheight);
    background-color: #d8ffef;
}

div.col {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}

div.row {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
}

div.grid {
    background-color: rgb(250, 226, 215);
    box-shadow: inset 0px 0px 0px 2px rgb(183, 116, 116);
    cursor: pointer;
}

div.row>div.grid {
    height: var(--edgeHeight);
    width: var(--edgeSize);
}

div.col>div.grid {
    height: var(--edgeSize);
    width: var(--edgeHeight);
}

div.grid.clicked {
    background-color: rgb(252, 151, 151);

}


input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>