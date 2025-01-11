import numpy as np

def cell_hog(magnitude, orientation, orientation_start, orientation_end,
             cell_columns, cell_rows, column_index, row_index,
             size_columns, size_rows,
             range_rows_start, range_rows_stop,
             range_columns_start, range_columns_stop):
    """Calculation of the cell's HOG value

    Parameters
    ----------
    magnitude : ndarray
        The gradient magnitudes of the pixels.
    orientation : ndarray
        Lookup table for orientations.
    orientation_start : float
        Orientation range start.
    orientation_end : float
        Orientation range end.
    cell_columns : int
        Pixels per cell (rows).
    cell_rows : int
        Pixels per cell (columns).
    column_index : int
        Block column index.
    row_index : int
        Block row index.
    size_columns : int
        Number of columns.
    size_rows : int
        Number of rows.
    range_rows_start : int
        Start row of cell.
    range_rows_stop : int
        Stop row of cell.
    range_columns_start : int
        Start column of cell.
    range_columns_stop : int
        Stop column of cell

    Returns
    -------
    total : float
        The total HOG value.
    """
    total = 0.0

    for cell_row in range(range_rows_start, range_rows_stop):
        cell_row_index = row_index + cell_row
        if cell_row_index < 0 or cell_row_index >= size_rows:
            continue

        for cell_column in range(range_columns_start, range_columns_stop):
            cell_column_index = column_index + cell_column
            if (cell_column_index < 0 or cell_column_index >= size_columns
                    or orientation[cell_row_index, cell_column_index] >= orientation_start
                    or orientation[cell_row_index, cell_column_index] < orientation_end):
                continue

            total += magnitude[cell_row_index, cell_column_index]

    return total / (cell_rows * cell_columns)

def hog_histograms(gradient_columns, gradient_rows,
                   cell_columns, cell_rows,
                   size_columns, size_rows,
                   number_of_cells_columns, number_of_cells_rows,
                   number_of_orientations,
                   orientation_histogram):
    """Extract Histogram of Oriented Gradients (HOG) for a given image.

    Parameters
    ----------
    gradient_columns : ndarray
        First order image gradients (rows).
    gradient_rows : ndarray
        First order image gradients (columns).
    cell_columns : int
        Pixels per cell (rows).
    cell_rows : int
        Pixels per cell (columns).
    size_columns : int
        Number of columns.
    size_rows : int
        Number of rows.
    number_of_cells_columns : int
        Number of cells (rows).
    number_of_cells_rows : int
        Number of cells (columns).
    number_of_orientations : int
        Number of orientation bins.
    orientation_histogram : ndarray
        The histogram array which is modified in place.
    """
    
    # Compute gradient magnitude
    magnitude = np.hypot(gradient_columns, gradient_rows)
    
    # Compute gradient direction (in degrees)
    orientation = np.degrees(np.arctan2(gradient_rows, gradient_columns)) % 180

    # Initialize the variables for histograms
    r_0 = cell_rows // 2
    c_0 = cell_columns // 2
    cc = cell_rows * number_of_cells_rows
    cr = cell_columns * number_of_cells_columns
    range_rows_stop = (cell_rows + 1) // 2
    range_rows_start = -(cell_rows // 2)
    range_columns_stop = (cell_columns + 1) // 2
    range_columns_start = -(cell_columns // 2)
    number_of_orientations_per_180 = 180.0 / number_of_orientations

    # Iterate over orientations
    for i in range(number_of_orientations):
        # Isolate orientations in this range
        orientation_start = number_of_orientations_per_180 * (i + 1)
        orientation_end = number_of_orientations_per_180 * i
        c = c_0
        r = r_0
        r_i = 0
        c_i = 0

        # Iterate over rows and columns
        while r < cc:
            c_i = 0
            c = c_0
            while c < cr:
                # Calculate and fill histogram
                orientation_histogram[r_i, c_i, i] = cell_hog(
                    magnitude, orientation, orientation_start, orientation_end,
                    cell_columns, cell_rows, c, r, size_columns, size_rows,
                    range_rows_start, range_rows_stop,
                    range_columns_start, range_columns_stop)
                c_i += 1
                c += cell_columns
            r_i += 1
            r += cell_rows