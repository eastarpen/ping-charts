class row:
    def __init__(self, name: str, label: str, chartDataList: list) -> None:
        self.name = name
        self.label = label
        self.chartDataList = chartDataList


class chartData:
    def __init__(self, delay: list, loss: list, time: list) -> None:
        self.delay = delay
        self.loss = loss
        self.time = time

    @staticmethod
    def empty():
        return chartData([0], [0], [0])


class response:
    """
    {
        targets: ['', '', '']
        rows: [
            {
                name: '',
                label: '',
                chartDataList: [{delay: [], time: [], loss: []}, {}, {}]
            }, {} , {}
        ]
    }
    """

    def __init__(self, targets: list, rows: list) -> None:
        self.rows = rows
        self.targets = targets
