#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdin = open('input.txt')
def input_data():
    """
    Получаем граф от пользователя
    Возвращаем: 
                сам граф
                таблицу родителей
                названия узлов начала и конца пути
    """

    # сам граф
    graph = {}
    # Таблица родителей, где ключ - имя дочернего узла
    parents = {}

    # Получаем данные от пользователя
    # Названия начального и конечного узлов (через пробел)
    start, finish = input().split()

    while True:
        try:
            node, child, cost = input().split()
        except EOFError:             # если достигли конца файла или ввода
            break                    # завершаем бесконечный цикл
        else:
            # Если ввод от пользователя не закончен, то
            # Проверяем есть ли такой узел УЖЕ в графе
            if node in graph:
                # Если есть, то добавляем новое ребро
                graph[node][child] = float(cost)
            else:
                # Узла такого нет, создаём новый и добавляем потомков
                graph[node] = {child: float(cost)}
            
            # Добавляем дочерний узел в таблицу родителей
            parents[child] = None

    return (graph, parents, start, finish)


def find_lowest_cost_node(costs, processed=[]):
    """
    Находим узел с наименьшей стоимостью
    costs - таблица стоимостей
    processed - список уже обработанных узлов
    """

    lowest_cost = float('inf')
    lowest_cost_node = None

    for node in costs:
        # Получаем стоимость узла
        curent_cost = costs[node]
        # Если есть узел с меньшей стоимостью, и он не был обработан
        if curent_cost < lowest_cost and node not in processed:
            # Он назначается новым узлом с наименьшей стоимостью
            lowest_cost = curent_cost
            lowest_cost_node = node

    return lowest_cost_node


def main():
    graph, parents, start, finish = input_data()

    # Таблица стоимостей
    costs = {}
    # Для всех узлов из таблицы parents неизвестны длины путей
    # Поэтому по умолчанию для каждого ставим наибольшую стоимость
    for node in parents:
        costs[node] = float('inf')

    # После того как весь граф получен, добавим, что
    # У потомков начального узла есть только один родитель - он сам
    for child in graph[start]:
        # Назначаем родителя для узла
        parents[child] = start
        # Добавляем его в таблицу стоимостей
        costs[child] = graph[start][child]

    # У конечного узла нет потомков
    graph[finish] = {}

    # Создаем список обработанных узлов графа
    processed = []

    # Тело алгоритма Дейкстры

    # Пока есть необработанные узлы
    while True:
        # Находим узел с наименьшей соимостью
        node = find_lowest_cost_node(costs, processed)

        # если все узлы обработаны, то выходим из цикла
        if node is None:
            break

        # Стоимость, чтобы добраться до текущего узла
        cost = costs[node]
        # Таблица с потомками текущего узла
        childs = graph[node]

        # Обходим всех потомков текущего узла
        for child in childs:
            # Вычисляем расстояние до них
            new_cost = cost + childs[child]
            # Если расстояние до потомка меньше его табличного значения
            if costs[child] > new_cost:
                # Назначаем ему меньшую стоимость
                costs[child] = new_cost
                # Делаем родителем узла child узел node
                # Так как от узла node до child наименьшее расстояние
                parents[child] = node
        processed.append(node)
    
    # Теперь мы получили две важные таблицы
    # Таблицу стоимостей и таблицу родителей
    
    # В таблице costs храниться кратчайшее расстояние от узла start к узлу finish
    res_cost = costs[finish]
    
    # Найдём кратчайший путь по узлам через таблицу parents
    res_path = []
    next_node = finish
    while True:
        res_path.append(next_node)

        if next_node == start:
            # Если дошли до начального узла то выходим из цикла
            break
        else:
            # Берём следующий родительский узел
            next_node = parents[next_node]
    

    # Печатаем результирующую стоимость
    print(res_cost)
    # Печатаем весь путь от начала до конца
    for node in res_path[::-1]:
        print(node) 

if __name__ == "__main__":
    main()