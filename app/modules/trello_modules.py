from trello import TrelloClient
from openpyxl import load_workbook
from copy import copy
import ipdb

blessId = '5bff57cb3b4c0b21262eabc6'
owenId = '5bff594d317049461251056e'

members = [blessId, owenId]

key = 'd19356dd8fdeb53226fc5e3fd4f3ab1b'
secret = 'b8f25dfe09f13a2ab3318ed14692a1d8f8aad9a1db4c5183021ae9aa5b77fa23'


def findInAllBoards(client, nameList, id):
    li = []
    boards = client.list_boards()
    for board in boards:
        for lis in board.list_lists():
            if lis.name in nameList:
                for card in lis.list_cards():
                    if id in card.member_id:
                        item = [
                            board.name,
                            '#{}'.format(card.short_id),
                            card.name
                        ]
                        li.append(item)
    return li


def getAllItems(lists):
    client = TrelloClient(api_key=key, api_secret=secret)
    dones = []
    for memberId in members:
        done = findInAllBoards(client, lists, memberId)
        dones.append(done)
    return dones


def putInXlsx(wb, items, row):
    for i in range(len(members)):
        ws = wb.worksheets[i]
        done = items[i]
        cell = copy(ws.cell(row=row, column=1))
        for item in done:
            print(item)
            ws.insert_rows(row)
            for i in range(1, 6):
                ws.cell(row=row, column=i).font = copy(cell.font)
                ws.cell(row=row, column=i).border = copy(cell.border)
                ws.cell(row=row, column=i).fill = copy(cell.fill)
                ws.cell(row=row, column=i).number_format = copy(cell.number_format)
                ws.cell(row=row, column=i).protection = copy(cell.protection)
                # ws.cell(row=10, column=i).alignment = copy(cell.alignment)
            for i in range(1, 4):
                ws.cell(row=row, column=i).value = item[i - 1]
    return wb


def run():
    dones = getAllItems(['已上傳待複驗', '複驗完成'])
    inProgress = getAllItems(['進行中'])

    filepath = "./report.xlsx"
    wb = load_workbook(filepath)

    wb = putInXlsx(wb, dones, 10)
    wb = putInXlsx(wb, inProgress, 5)

    wb.save(filename="./工作週報_Frontend_2019.xlsx")

    print('done')


if __name__ == '__main__':
    run()
