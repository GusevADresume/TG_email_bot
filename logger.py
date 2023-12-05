import csv
import datetime


async def logger(error):
    csv = await reader()
    csv.append(f'{error} - {datetime.datetime.now()}')
    await writer(csv)


async def reader():
    with open('logs.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            return (row)


async def writer(error):
    with open('logs.csv', 'w', newline='') as csvfile:
        errorriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        errorriter.writerow(error)
