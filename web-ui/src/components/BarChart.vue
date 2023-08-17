<template>
    <Bar height="26" :data="data" :options="options" />
    <span v-if="averageDelay"> {{ averageDelay }}ms</span>
</template>

<script>

import { max_ping_value, judge_levels, strict_level, lenient_level, much_lenient_level } from '@/constants';

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    components: { Bar },
    props: {
        chartData: {
            type: Object,
            required: true
        },
        judgeLevel: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            options: {
                categoryPercentage: 1.0,
                barPercentage: 1.0,
                scales: {
                    x: { display: false },
                    y: { display: false, max: max_ping_value, min: 0, ticks: { stepSize: 50 } }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: true }
                },
                animation: true,
            },
            data: this.generageData(),
            averageDelay: ((delays) => {
                let aver = delays.reduce((a, b) => a + b, 0) / delays.length
                return aver ? aver.toFixed(2) : 0;
            })(this.chartData.delay),
        }
    },
    watch: {
        judgeLevel: {
            immediate: true,
            handler() {
                this.data = this.generageData();
            }
        }
    },
    methods: {
        timeConverter(UNIX_timestamp) {
            let time = new Date(UNIX_timestamp * 1000);
            let year = time.getFullYear();
            let month = String(time.getMonth() + 1).padStart(2, '0');
            let date = String(time.getDate()).padStart(2, '0');
            let hours = String(time.getHours()).padStart(2, '0');
            let minutes = String(time.getMinutes()).padStart(2, '0');
            let seconds = String(time.getSeconds()).padStart(2, '0');

            return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
        },
        getLabels() {
            let labels = [];
            for (let i = 0; i < this.chartData.time.length; i++) {
                let time = this.timeConverter(this.chartData.time[i]);
                let loss = this.chartData.loss[i];
                let delay = this.chartData.delay[i];
                const s = `${time} delay: ${delay.toFixed(2)}ms loss: ${loss.toFixed(2)}`;
                labels.push(s);
            }
            return labels;
        },
        generageData() {
            return {
                labels: this.getLabels(),
                datasets: [{
                    data: this.chartData.delay,
                    backgroundColor: function (context) {
                        var loss = this.chartData.loss[context.dataIndex];
                        var level;
                        switch (this.judgeLevel) {
                            case judge_levels.strict: level = strict_level; break;
                            case judge_levels.lenient: level = lenient_level; break;
                            case judge_levels.much_lenient: level = much_lenient_level; break;
                        }
                        return loss <= level.green ? 'green'
                            : loss <= level.yellow ? 'orange'
                                : 'red'
                    }.bind(this)
                }]
            }
        }
    }
};
</script>
