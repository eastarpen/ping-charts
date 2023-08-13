<template>
    <h1 class="tittle">Ping Charts</h1>
    <radio-com :initModel="judgeLevel" :uid="levelUid" :items="levelItems" :info="levelInfo"
        @option-selected="changeLevel" />
    <radio-com :initModel="min" :uid="minUid" :items="minItems" :info="minInfo" :initSelect="3"
        @option-selected="changeMin" />
    <div style="overflow-x: auto; max-width: 1200px; margin:auto;">
        <table class="content-table" v-if="isTableVisible">
            <thead>
                <tr>
                    <th style="position: sticky; left: 0; background: #009879;"> Name </th>
                    <th> Label </th>
                    <th v-for="(target, index) in targets" :key="index">
                        {{ target }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in rows" :key="index">
                    <td style="position: sticky; left: 0; background: #f3f3f3;">{{ row.name }}</td>
                    <td>{{ row.label }}</td>
                    <td v-for="(chartData, index) in row.chartDataList" :key="index" class="chart">
                        <bar-chart :chartData="chartData" :judgeLevel="judgeLevel" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style>
@import './assets/styles/table.css';
@import './assets/styles/app.css';
</style>

<script>
import axios from 'axios';
import BarChart from './components/BarChart.vue'
import RadioCom from './components/RadioCom.vue'
import { judge_levels } from '@/constants';

export default {
    name: 'App',
    components: {
        BarChart,
        RadioCom
    },
    data() {
        return {
            targets: ["CHINANET", "CHINAUNION", "CHINAMOBLE"],
            rows: {},
            judgeLevel: judge_levels.strict,
            isTableVisible: false,
            levels: judge_levels,
            levelUid: 'level',
            levelInfo: "Select Level",
            levelItems: [
                { value: judge_levels.strict, label: "strict" },
                { value: judge_levels.lenient, label: "lenient" },
                { value: judge_levels.much_lenient, label: "much lenient" },
            ],
            min: 60,
            minUid: 'min',
            minInfo: "Select Time",
            minItems: [
                { value: 5, label: "5min" },
                { value: 30, label: "30min" },
                { value: 60, label: "1h" },
                { value: 1440, label: "1d" },
                { value: 10080, label: "7d" },
                { value: 43200, label: "30d" },
            ],
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        fetchData() {
            this.isTableVisible = false;
            axios.get('./data?min=' + this.min).then(response => {
                this.targets = response.data.targets;
                this.rows = response.data.rows;
                this.isTableVisible = true;
            }).catch(err => {
                console.log(err);
            })
        },
        changeLevel(level) {
            this.judgeLevel = level;
        },
        changeMin(min) {
            this.min = min;
        }

    },
    watch: {
        min() {
            this.fetchData();
        }
    }
}
</script>
