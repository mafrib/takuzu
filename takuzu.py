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

    def __init__(self, n):
        """Inicializa um tabuleiro vazio."""
        self.board = np.full((n, n), 2)

    def __len__(self):
        """Devolve a dimensão (N) do tabuleiro N x N"""
        return len(self.board)

    def __str__(self):
        """Retorna representação externa do tabuleiro"""
        return "\n".join("\t".join(map(str, row)) for row in self.board)

    def update(self, row: int, col: int, number: int):
        """Atualiza o valor de uma posição no tabuleiro."""
        self.board[row, col] = number

    def copy(self):
        """Devolve uma cópia profunda do tabuleiro"""
        newBoard = Board(len(self.board))
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                newBoard.update(i, j, self.get_number(i, j))
        return newBoard

    def get_row(self, row: int):
        """Devolve tuplo contendo a respetiva linha do tabuleiro"""
        return tuple(self.board[row])

    def get_col(self, col: int):
        """Devolve tuplo contendo a respetiva coluna do tabuleiro"""
        return tuple(self.board[:, col])

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
        """Devolve True se todos os subtuplos forem diferentes uns dos outros."""
        if len(set(tups)) == len(self.board):
            return True
        return False

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= len(self.board) or col < 0 or col >= len(self.board):
            return None
        return self.board[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            return (self.board[row + 1, col], None)
        elif row == len(self.board) - 1:
            return (None, self.board[row - 1, col])
        else:
            return (self.board[row + 1, col], self.board[row - 1, col])

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.board[row, col + 1])
        elif col == len(self.board) - 1:
            return (self.board[row, col - 1], None)
        else:
            return (self.board[row, col - 1], self.board[row, col + 1])

    def check_equal_adjacent(self, row: int, col: int) -> int:
        """Devolve o número a preencher caso os números adjacentes sejam
        iguais entre si. Caso contrário, devolve 2."""

        adjacent_horizontal = self.adjacent_horizontal_numbers(row, col)
        adjacent_vertical = self.adjacent_vertical_numbers(row, col)
        if (
            adjacent_horizontal[0] == adjacent_horizontal[1] == 1
            or adjacent_vertical[0] == adjacent_vertical[1] == 1
        ):
            print("adjacent_horizontal:", adjacent_horizontal)
            print("adjacent_vertical:", adjacent_vertical)
            return 0
        elif (
            adjacent_horizontal[0] == adjacent_horizontal[1] == 0
            or adjacent_vertical[0] == adjacent_vertical[1] == 0
        ):
            return 1
        else:
            return 2

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

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        # TODO voltar a mudar para a submissão
        from sys import stdin

        n = int(stdin.readline())
        board = Board(n)

        for i in range(n):
            line = tuple(map(int, stdin.readline().split()))
            for j in range(n):
                board.update(i, j, line[j])

        return board

        # # TODO remover; só para testes locais
        # import fileinput
        # read = list(fileinput.input("./tests/input_T01"))
        # n = int(read[0])
        # read = read[1:]
        # board = Board(n)

        # for i in range(n):
        #     line = tuple(map(int, read[i].split()))
        #     for j in range(n):
        #         board.update(i, j, line[j])

        # return board

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
            number_to_place = state.board.check_counter_row(i)
            if number_to_place != 2:
                for j in range(len(state.board)):
                    if state.board.get_number(i, j) == 2:
                        actions.append((i, j, number_to_place))

        for j in range(len(state.board)):
            number_to_place = state.board.check_counter_col(j)
            if number_to_place != 2:
                for i in range(len(state.board)):
                    if state.board.get_number(i, j) == 2:
                        actions.append((i, j, number_to_place))

        return list(set(actions))

    @staticmethod
    def is_valid_state(state: TakuzuState) -> bool:
        """Devolve True se o estado cumprir as seguintes restrições:
        - linhas e colunas diferentes entre si
        - número de zeros e uns válidos
        - restrições de adjacência"""

        lines = state.board.get_rows()
        cols = state.board.get_cols()

        if not state.board.all_diff(lines) or not state.board.all_diff(cols):
            return False

        for line in lines:
            if not state.board.is_valid_count(line):
                return False
        for col in cols:
            if not state.board.is_valid_count(col):
                return False

        for i in range(len(state.board)):
            for j in range(len(state.board)):
                if not state.board.is_valid_adjacent():
                    return False

        return True

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        newState = TakuzuState(state.board.copy())
        newState.board.update(action[0], action[1], action[2])
        return newState


    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        for i in range(len(state.board)):
            for j in range(len(state.board)):
                if state.board.get_number(i, j) == 2:
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
        #         if not state.board.is_valid_adjacent():
        #             return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

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
