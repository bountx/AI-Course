import random

"""
program stosuje heurystykę inspirowaną WalkSAT, 
polegającą na iteracyjnym dopasowywaniu bloków kolorów do opisów rzędów i kolumn

calculate_partial_distribution szuka optymalnego miejsca dla pojedynczego bloku, 
zachłannie minimalizując liczbę błędów względem opisu

almost_walk_sat iteracyjnie poprawia rozwiązanie przez losowe modyfikacje w najbardziej problematycznych miejscach, 
aż do osiągnięcia rozwiązania lub wyczerpania limitu prób
"""


def calculate_partial_distribution(numbers, desc_length, start, end):
    result_start = start
    current = 0
    
    for i in range(start, start + desc_length):
        if numbers[i] == 0:
            current += 1

    for i in range(start + desc_length, end):
        current += numbers[i]

    maximum = current

    for i in range(start, end - desc_length):
        if numbers[i] == 0:
            current -= 1
        else:
            current += 1

        if numbers[i + desc_length] == 0:
            current += 1
        else:
            current -= 1

        if current < maximum:
            result_start = i + 1
            maximum = current
            if current == 0:
                break

    return result_start

def optimal_distribution(row, desc):
    start = 0
    end = len(row)
    left = sum(desc) + len(desc)
    result = 0
    blocks = [0 for i in range(end)]

    for desc_length in desc:
        left -= desc_length + 1
        start = calculate_partial_distribution(row, desc_length, start, end - left)
        for i in range(start, start + desc_length):
            blocks[i] = 1
        start += desc_length + 1
    
    for i in range(end):
        if row[i] != blocks[i]:
            result += 1

    return result

def get_column(image, column):
    return [row[column] for row in image]

def flip_pixel(image, row, column):
    image[row][column] = abs(image[row][column] - 1)

def print_image(image, row_desc, col_desc):
    col_desc_str = "  "
    for val in col_desc:
        col_desc_str += str(val) + ' '
    print(col_desc_str)
    for row in range(len(image)):
        row_str = str(row_desc[row])
        for pixel in image[row]:
            row_str += " ." if pixel == 0 else " #"
        print(row_str)

def column_optimal_distribution(image, col_desc, column):
    return optimal_distribution(get_column(image, column), col_desc[column])

def almost_walk_sat(sizes, row_desc, col_desc):
    limit = 750
    while True:
        bad_columns = []
        bad_rows = []
        image = [[random.randint(0, 1) for _ in range(sizes[1])] for _ in range(sizes[0])]
        
        for i in range(sizes[1]):
            if optimal_distribution(get_column(image, i), col_desc[i]) > 0:
                bad_columns.append(i)
        
        for i in range(sizes[0]):
            if optimal_distribution(image[i], row_desc[i]) > 0:
                bad_rows.append(i)

        for iteration in range(limit):
            high_difference = float("-inf")
            high_ids = []
            filtered_ids = []
            check_row, check_column = 0, 0
            choice = random.randint(0 if bad_columns else 1, 1 if bad_rows else 0)
            
            if choice == 0:
                column = random.choice(bad_columns)
                column_difference = column_optimal_distribution(image, col_desc, column)
                
                for row in range(sizes[0]):
                    row_difference = optimal_distribution(image[row], row_desc[row])
                    difference = column_difference + row_difference
                    flip_pixel(image, row, column)
                    difference -= column_optimal_distribution(image, col_desc, column) + optimal_distribution(image[row], row_desc[row])
                    flip_pixel(image, row, column)
                    
                    if difference >= high_difference:
                        high_difference = difference
                        high_ids.append((row, difference))
                
                for id in high_ids:
                    if id[1] == high_difference:
                        filtered_ids.append(id[0])
                
                check_row = random.choice(filtered_ids)
                check_column = column
                flip_pixel(image, check_row, column)
            
            else:
                row = random.choice(bad_rows)
                row_difference = optimal_distribution(image[row], row_desc[row])
                
                for column in range(sizes[1]):
                    column_difference = column_optimal_distribution(image, col_desc, column)
                    difference = column_difference + row_difference
                    flip_pixel(image, row, column)
                    difference -= column_optimal_distribution(image, col_desc, column) + optimal_distribution(image[row], row_desc[row])
                    flip_pixel(image, row, column)
                    
                    if difference >= high_difference:
                        high_difference = difference
                        high_ids.append((column, difference))
                
                for id in high_ids:
                    if id[1] == high_difference:
                        filtered_ids.append(id[0])
                
                check_row = row
                check_column = random.choice(filtered_ids)
                flip_pixel(image, row, check_column)

            result = optimal_distribution(image[check_row], row_desc[check_row])
            
            if check_row in bad_rows: 
                if result == 0:
                    bad_rows.remove(check_row)
            elif result != 0:
                bad_rows.append(check_row)

            result = column_optimal_distribution(image, col_desc, check_column)
            
            if check_column in bad_columns: 
                if result == 0:
                    bad_columns.remove(check_column)
            elif result != 0:
                bad_columns.append(check_column)

            if len(bad_rows) == 0 and len(bad_columns) == 0:
                return image


with open("zad_input.txt") as file:
    row_desc = []
    col_desc = []
    sizes = file.readline()
    sizes = [int(size) for size in sizes.split()]
    row_desc = [[int(size) for size in file.readline().split()] for i in range(sizes[0])]
    col_desc = [[int(size) for size in file.readline().split()] for i in range(sizes[1])]
    painted_image = almost_walk_sat(sizes, row_desc, col_desc)
    with open("zad_output.txt", 'w') as output_file:
        for row in painted_image:
            row_str = ""
            for pixel in row:
                if pixel == 1:
                    row_str += '#'
                else:
                    row_str += '.'
            row_str += '\n'
            output_file.write(row_str)
