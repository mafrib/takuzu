# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo al043:
# 99188 Carlos Vaz
# 99268 Mafalda Ribeiro

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board):
        """Inicializa um tabuleiro vazio."""
        self.board = board

    def __len__(self):
        """Devolve a dimensão (N) do tabuleiro N x N"""
        return len(self.board)

    def __str__(self):
        """Retorna representação externa do tabuleiro"""
        return "\n".join("\t".join(map(str, row)) for row in self.board)

    def move_result(self, row: int, col: int, number: int):
        """Devolve o tabuleiro resultante da jogada recebida."""
        newBoard = ()
        for i in range(len(self.board)):
            if i == row:
                newRow = ()
                for j in range(len(self.board)):
                    if j == col:
                        newRow += (number,)
                    else:
                        newRow += (self.board[i][j],)
                newBoard += (newRow,)
            else:
                newBoard += (self.board[i],)

        return Board(newBoard)

    def get_row(self, row: int):
        """Devolve a respetiva linha do tabuleiro"""
        return self.board[row]

    def get_col(self, col: int):
        """Devolve a respetiva coluna do tabuleiro"""
        tup = ()
        for i in range(len(self.board)):
            tup += (self.board[i][col],)

        return tup

    def get_rows(self):
        """Devolve tuplo contendo as linhas do tabuleiro"""
        lines = ()
        for i in range(len(self.board)):
            lines += (self.get_row(i),)
        return lines

    def get_cols(self):
        """Devolve tuplo contendo as colunas do tabuleiro"""
        cols = ()
        for i in range(len(self.board)):
            cols += (self.get_col(i),)
        return cols

    def all_diff(self, tups) -> bool:
        """Devolve True se todos os subtuplos preenchidos forem diferentes uns dos outros."""
        trimmed_tups = ()
        for tup in tups:
            if tup.count(2) == 0:
                trimmed_tups += (tup,)

        return len(set(trimmed_tups)) == len(trimmed_tups)

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            return (self.board[row + 1][col], None)
        elif row == len(self.board) - 1:
            return (None, self.board[row - 1][col])
        else:
            return (self.board[row + 1][col], self.board[row - 1][col])

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.board[row][col + 1])
        elif col == len(self.board) - 1:
            return (self.board[row][col - 1], None)
        else:
            return (self.board[row][col - 1], self.board[row][col + 1])

    def check_equal_adjacent(self, row: int, col: int) -> int:
        """Devolve o número a preencher caso os números adjacentes sejam
        iguais entre si. Caso contrário, devolve 2."""

        adjacent_horizontal = self.adjacent_horizontal_numbers(row, col)
        adjacent_vertical = self.adjacent_vertical_numbers(row, col)
        if (
            adjacent_horizontal[0] == adjacent_horizontal[1] == 1
            or adjacent_vertical[0] == adjacent_vertical[1] == 1
        ):
            return 0
        elif (
            adjacent_horizontal[0] == adjacent_horizontal[1] == 0
            or adjacent_vertical[0] == adjacent_vertical[1] == 0
        ):
            return 1
        else:
            return 2

    def is_valid_adjacent(self, tup: tuple) -> bool:
        """Devolve True se a linha ou coluna não tiver mais do
        que dois números iguais adjacentes."""
        for i in range(2, len(tup)):
            if (tup[i - 2] == tup[i - 1] == tup[i]) and tup[i] != 2:
                return False

        return True

    def is_valid_adjacents(self) -> bool:
        """Devolve True se cada linha e coluna não tiver mais do
        que dois números iguais adjacentes."""
        for row in self.get_rows():
            if not self.is_valid_adjacent(row):
                return False

        for col in self.get_cols():
            if not self.is_valid_adjacent(col):
                return False

        return True

    def is_valid_count(self, tup: tuple) -> bool:
        """Devolve True se o número de zeros e uns da linha ou
        coluna é válido de acordo com as restrições do problema."""
        zeros = tup.count(0)
        ones = tup.count(1)
        return True if abs(zeros - ones) < 2 else False

    def check_counter_row(self, row_number: int) -> int:
        """Devolve o número a preencher caso o número de zeros ou uns
        já tenha chegado ao limite da linha. Caso nenhum tenha
        chegado ao limite, devolve 2."""

        row = self.get_row(row_number)
        limit = np.ceil(len(self.board) / 2)
        if row.count(0) == limit:
            return 1
        elif row.count(1) == limit:
            return 0
        else:
            return 2

    def check_counter_col(self, col_number: int) -> int:
        """Devolve o número a preencher caso o número de zeros ou uns
        já tenha chegado ao limite da coluna. Caso nenhum tenha
        chegado ao limite, devolve 2."""

        col = self.get_col(col_number)
        limit = np.ceil(len(self.board) / 2)
        if col.count(0) == limit:
            return 1
        elif col.count(1) == limit:
            return 0
        else:
            return 2

    def two_adjacents_horizontal(self, row_number: int):
        """Devolve ações a executar caso existam dois números
        iguais seguidos adjacentes na mesma linha"""
        actions = []
        row = self.get_row(row_number)
        for j in range(1, len(self.board)):
            current = self.get_number(row_number, j)
            previous = self.get_number(row_number, j - 1)
            before_adjacency = (
                self.get_number(row_number, j - 2) if j - 2 >= 0 else None
            )
            after_adjacency = (
                self.get_number(row_number, j + 1) if j + 1 < len(self.board) else None
            )

            if before_adjacency == 2:
                if current == previous == 0:
                    actions.append((row_number, j - 2, 1))
                elif current == previous == 1:
                    actions.append((row_number, j - 2, 0))
            if after_adjacency == 2:
                if current == previous == 0:
                    actions.append((row_number, j + 1, 1))
                elif current == previous == 1:
                    actions.append((row_number, j + 1, 0))

        return actions

    def two_adjacents_vertical(self, col_number: int):
        """Devolve ações a executar caso existam dois números
        iguais seguidos adjacentes na mesma coluna"""
        actions = []
        row = self.get_col(col_number)
        for i in range(1, len(self.board)):
            current = self.get_number(i, col_number)
            previous = self.get_number(i - 1, col_number)
            before_adjacency = (
                self.get_number(i - 2, col_number) if i - 2 >= 0 else None
            )
            after_adjacency = (
                self.get_number(i + 1, col_number) if i + 1 < len(self.board) else None
            )

            if before_adjacency == 2:
                if current == previous == 0:
                    actions.append((i - 2, col_number, 1))
                elif current == previous == 1:
                    actions.append((i - 2, col_number, 0))
            if after_adjacency == 2:
                if current == previous == 0:
                    actions.append((i + 1, col_number, 1))
                elif current == previous == 1:
                    actions.append((i + 1, col_number, 0))

        return actions

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        from sys import stdin

        n = int(stdin.readline())
        board = ()

        for i in range(n):
            row = ()
            input_row = tuple(map(int, stdin.readline().split()))
            for j in range(n):
                row += (input_row[j],)
            board += (row,)

        return Board(board)

    def check_only_option(self, tup: tuple, is_row: bool, row_or_col_number: int):
        """Devolve uma lista de ações a executar caso seja
        possível prever incoerências na linha ou coluna dadas."""
        empty_indices = []
        for i in range(len(tup)):
            if tup[i] == 2:
                empty_indices.append(i)

        options = [tup]
        while options[0].count(2) > 0:
            option1 = ()
            option2 = ()
            for i in range(len(options[0])):
                if options[0][i] != 2:
                    option1 += (options[0][i],)
                else:
                    option2 = option1 + (1,) + options[0][i + 1 :]
                    option1 = option1 + (0,) + options[0][i + 1 :]
                    break
            options.pop(0)
            options.append(option1)
            options.append(option2)

        validOptions = []
        for option in options:
            if self.is_valid_count(option) and self.is_valid_adjacent(option):
                validOptions.append(option)

        actions = []
        for i in empty_indices:
            uniques = set()
            for j in range(len(validOptions)):
                uniques.add(validOptions[j][i])
            if len(uniques) == 1:
                if is_row:
                    actions.append((row_or_col_number, i, uniques.pop()))
                else:
                    actions.append((i, row_or_col_number, uniques.pop()))

        return actions

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        actions = []
        for i in range(len(state.board)):
            for j in range(len(state.board)):
                if state.board.get_number(i, j) == 2:
                    number_to_place = state.board.check_equal_adjacent(i, j)
                    if number_to_place != 2:
                        actions.append((i, j, number_to_place))

        for i in range(len(state.board)):
            actions += state.board.two_adjacents_horizontal(i)

            number_to_place = state.board.check_counter_row(i)
            if number_to_place != 2:
                for j in range(len(state.board)):
                    if state.board.get_number(i, j) == 2:
                        actions.append((i, j, number_to_place))

        for j in range(len(state.board)):
            actions += state.board.two_adjacents_vertical(j)

            number_to_place = state.board.check_counter_col(j)
            if number_to_place != 2:
                for i in range(len(state.board)):
                    if state.board.get_number(i, j) == 2:
                        actions.append((i, j, number_to_place))

        if actions == []:
            for i in range(len(state.board)):
                actions += state.board.check_only_option(
                    state.board.get_row(i), True, i
                )
                actions += state.board.check_only_option(
                    state.board.get_col(i), False, i
                )

        if actions == []:
            simulation = []
            for i in range(len(state.board)):
                for j in range(len(state.board)):
                    if state.board.get_number(i, j) == 2:
                        simulation.append((i, j, 0))
                        simulation.append((i, j, 1))
            for s in simulation:
                if self.is_valid_state(self.result(state, s)):
                    actions.append(s)

        return list(set(actions))

    @staticmethod
    def is_valid_state(state: TakuzuState) -> bool:
        """Devolve True se o estado cumprir as seguintes restrições:
        - linhas e colunas diferentes entre si
        - número de zeros e uns válidos
        - restrições de adjacência"""

        rows = state.board.get_rows()
        cols = state.board.get_cols()

        if not state.board.all_diff(rows) or not state.board.all_diff(cols):
            return False

        for row in rows:
            if not state.board.is_valid_count(row):
                return False
        for col in cols:
            if not state.board.is_valid_count(col):
                return False

        for i in range(len(state.board)):
            for j in range(len(state.board)):
                if not state.board.is_valid_adjacents():
                    return False

        return True

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        return TakuzuState(state.board.move_result(action[0], action[1], action[2]))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        for i in range(len(state.board)):
            for j in range(len(state.board)):
                if state.board.get_number(i, j) == 2:
                    return False

        rows = state.board.get_rows()
        cols = state.board.get_cols()

        if not state.board.all_diff(rows) or not state.board.all_diff(cols):
            return False

        # lines = state.board.get_lines()
        # cols = state.board.get_cols()

        # if not state.board.all_diff(lines) or not state.board.all_diff(cols):
        #     return False

        # for line in lines:
        #     if not state.board.is_valid_count(line):
        #         return False
        # for col in cols:
        #     if not state.board.is_valid_count(col):
        #         return False

        # for i in range(len(state.board)):
        #     for j in range(len(state.board)):
        #         if not state.board.is_valid_adjacents():
        #             return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        empty_spaces = 0
        for row in node.state.board.get_rows():
            empty_spaces += row.count(2)

        return empty_spaces

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board)
