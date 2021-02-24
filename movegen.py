#
#  Knight visualizer
#  A pygame project that shows you graphically how many moves it takes a knight to move to a specific square on the chess board.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

def square_dist(start_pos, target_pos, rows, cols):
    dcol = [2, 2, -2, -2, 1, 1, -1, -1]
    drow = [1, -1, 1, -1, 2, -2, 2, -2]

    queue = [(*start_pos, 0)]

    visited = [[False for _ in range(cols)] for _ in range(rows)]

    visited[start_pos[0]][start_pos[1]] = True

    while len(queue) > 0:
        pos = queue.pop(0)
        if pos[0] == target_pos[0] and pos[1] == target_pos[1]:
            return pos[2]

        for i in range(8):
            col = pos[1] + drow[i]
            row = pos[0] + dcol[i]
            if 0 <= row < rows and 0 <= col < cols and not visited[row][col]:
                visited[row][col] = True
                queue.append((row, col, pos[2] + 1))
