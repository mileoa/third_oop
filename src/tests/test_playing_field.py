import pytest
from src.playing_field import PlayingField


class TestPlayingFieldATD:

    @pytest.fixture
    def field(self):
        return PlayingField(width=8, height=8)

    def test_init(self):
        fileid_width = 8
        fileid_height = 8
        field = PlayingField(width=fileid_width, height=fileid_height)

        field_matrix = field.get_field()

        assert len(field_matrix) == fileid_height
        for row in field_matrix:
            assert len(row) == fileid_width
        assert field.find_combination() == []
        assert field.has_possible_moves()

    def test_top_row_has_empty_cells(self, field):
        matrix_before_delete = self.field.get_field()
        elements_to_delete = [(0, 0), (0, 4), (0, 7)]
        field.delete_elements(elements_to_delete)

        field.fill_top_row()
        matrix_after_delete = self.field.get_field()

        assert field.get_fill_top_row_status() == field.FILL_TOP_ROW_NOT_OK
        for row_i, row in enumerate(matrix_after_delete):
            for element_i, element in enumerate(row):
                if (row_i, element_i) in elements_to_delete:
                    assert element is not None
                    continue
                assert element == matrix_before_delete[row_i][element_i]

    def test_top_row_has_no_empty_cells(self, field):
        field.fill_top_row()
        field_matrix = field.get_field()

        for row in range(field_matrix):
            for cell in range(len(row)):
                assert field_matrix[row][cell] is not None
        assert field.get_fill_top_row_status() == field.FILL_TOP_ROW_ERR_NOT_EMPTY

    def test_shift_elements_down_full_field(self, field):
        matrix_before_shift = field.get_field()
        field.shift_elements_down()
        matrix_after_shift = field.get_field()

        assert field.get_shift_down_status() == field.SHIFT_DOWN_ERR_FULL_FIELD
        assert matrix_before_shift == matrix_after_shift

    def test_shift_elements_down_not_full_field(self, field):
        elements_to_delete = [
            (0, 0),
            (0, 4),
            (0, 7),
            (2, 0),
            (2, 1),
            (7, 4),
            (1, 7),
        ]

        matrix_before_shift = field.get_field()
        field.delete_elements(elements_to_delete)
        field.shift_elements_down()
        matrix_after_shift = field.get_field()

        assert field.get_shift_down_status() == field.SHIFT_DOWN_OK

        # Колонка 0: удалены (0,0) и (2,0), два None всплывают наверх
        for row_i, row_after_shift in enumerate(matrix_after_shift):
            if row_i < 2:
                assert row_after_shift[0] is None
                continue
            assert row_after_shift[1] == matrix_before_shift[row_i][1]

        # Колонка 1: удалена (2,1), один None всплывает наверх
        for row_i, row_after_shift in enumerate(matrix_after_shift):
            if row_i < 1:
                assert row_after_shift[1] is None
                continue
            assert row_after_shift[1] == matrix_before_shift[row_i][0]

        # Колонка 4: удалены (0,4) и (7,4), два None всплывают наверх
        for row_i, row_after_shift in enumerate(matrix_after_shift):
            if row_i < 2:
                assert row_after_shift[4] is None
                continue
            assert row_after_shift[4] == matrix_before_shift[row_i][4]

        # Колонка 7: удалены (0,7) и (1,7), два None всплывают наверх
        for row_i, row_after_shift in enumerate(matrix_after_shift):
            if row_i < 2:
                assert row_after_shift[7] is None
                continue
            assert row_after_shift[1] == matrix_before_shift[row_i][7]

        # Колонки без изменений
        for row_i, row_after_shift in enumerate(matrix_after_shift):
            for cell_i, cell_after_shift in enumerate(row_after_shift):
                if cell_i in (0, 1, 4, 7):
                    continue
                assert cell_after_shift == matrix_before_shift[row_i][cell_i]

    def test_shift_elements_down_empty_field(self, field):
        elements_to_delete = []
        matrix = field.get_field()
        empty_matrix = []
        for row_i in range(len(matrix)):
            empty_matrix_row = []
            for cell_i in range(len(matrix[row_i])):
                elements_to_delete.append((row_i, cell_i))
                empty_matrix_row.append(None)
            empty_matrix.append(empty_matrix_row)

        field.shift_elements_down()
        matrix_after_shift = field.get_field()

        assert field.get_shift_down_status() == field.SHIFT_DOWN_OK
        assert matrix_after_shift == empty_matrix

    @pytest.mark.parametrize(
        "pos1, pos2",
        [
            ((0, 0), (0, 1)),
            ((3, 2), (3, 3)),
            ((0, 0), (1, 0)),
            ((2, 3), (3, 3)),
        ],
    )
    def test_swap_elements_correct(self, field, pos1, pos2):
        matrix_before_swap = field.get_field()
        val1 = matrix_before_swap[pos1[0]][pos1[1]]
        val2 = matrix_before_swap[pos2[0]][pos2[1]]

        field.swap_elements(pos1, pos2)
        matrix_after = field.get_field()

        assert matrix_after[pos1[0]][pos1[1]] == val2
        assert matrix_after[pos2[0]][pos2[1]] == val1
        assert field.get_swap_status() == field.SWAP_ELEMENTS_OK

    @pytest.mark.parametrize(
        "pos1, pos2",
        [
            ((0, 0), (-1, 0)),
            ((0, 0), (0, 100)),
            ((-1, 0), (0, 0)),
            ((0, 100), (0, 0)),
        ],
    )
    def test_swap_elements_out_of_bounds(self, field, pos1, pos2):
        matrix_before = field.get_field()
        field.swap_elements(pos1, pos2)
        matrix_after = field.get_field()

        assert field.get_swap_status() == field.SWAP_ELEMENTS_ERR_OUT_OF_BOUNDS
        assert matrix_before == matrix_after

    @pytest.mark.parametrize(
        "pos1, pos2",
        [
            ((0, 0), (0, 2)),
            ((0, 0), (2, 0)),
            ((5, 5), (4, 4)),
            ((5, 5), (4, 6)),
            ((5, 5), (6, 4)),
            ((5, 5), (6, 6)),
        ],
    )
    def test_swap_elements_not_neighbours(self, field, pos1, pos2):
        matrix_before = field.get_field()
        field.swap_elements(pos1, pos2)
        matrix_after = field.get_field()

        assert field.get_shift_down_status() == field.SHIFT_DOWN_ERR_FULL_FIELD
        assert matrix_before == matrix_after

    @pytest.mark.parametrize(
        "positions",
        [
            [(0, 0)],
            [(0, 0), (0, 1), (0, 2)],
            [(0, 0), (2, 3), (4, 1)],
            [(row, col) for row in range(8) for col in range(8)],
        ],
    )
    def test_delete_elements(self, field, positions):
        matrix_before = field.get_field()
        field.delete_elements(positions)
        matrix_after = field.get_field()

        assert field.get_delete_status() == field.DELETE_ELEMENTS_OK
        for row_i, row in enumerate(matrix_after):
            for col_i, element in enumerate(row):
                if (row_i, col_i) not in positions:
                    assert element == matrix_before[row_i][col_i]
                    continue
                assert matrix_after[row_i][col_i] is None

    @pytest.mark.parametrize(
        "positions",
        [
            # Выход за границы
            [(-1, 0)],
            [(0, 100)],
            [(100, 100)],
        ],
    )
    def test_delete_elements_out_of_bounds(self, field, positions):
        matrix_before = field.get_field()
        field.delete_elements(positions)
        matrix_after = field.get_field()

        assert field.get_delete_status() == field.DELETE_ELEMENTS_ERR_OUT_OF_BOUNDS
        assert matrix_after == matrix_before

    def test_delete_elements_empty_position(self, field):
        # Позиция уже пуста
        field.delete_elements([(0, 0)])
        field.delete_elements([(0, 0)])

        assert field.get_delete_status() == field.DELETE_ELEMENTS_ERR_EMPTY

    def test_has_possible_moves_false(self, field):
        assert field.has_possible_moves()

    def test_has_possible_moves(self, field):
        assert field.has_possible_moves()

    def test_find_combination_no_combination(self, field):
        assert field.find_combination == []

    def test_find_combination(self, field):
        assert field.find_combination == []

    def test_find_special_bonus_affected_elements_column(self, field):
        fileds_to_delete = field.find_special_bonus_affected_elements(
            "column_eliminate", 1, 1
        )
        assert fileds_to_delete == [
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
        ]
        assert (
            field.get_find_special_bonus_affected_elements_status()
            == field.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_OK
        )

    def test_find_special_bonus_affected_elements_row(self, field):
        fileds_to_delete = field.find_special_bonus_affected_elements(
            "row_eliminate", 1, 1
        )
        assert fileds_to_delete == [
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
        ]
        assert (
            field.get_find_special_bonus_affected_elements_status()
            == field.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_OK
        )

    def test_find_special_bonus_affected_elements_by_type(self, field):
        field_matrix = field.get_field()
        type_to_delete = field_matrix[1][1]

        fileds_to_delete = field.find_special_bonus_affected_elements(
            "by_type_eliminate", 1, 1
        )

        for row_i, row in enumerate(field_matrix):
            for column_i, cell in enumerate(row):
                if cell == type_to_delete:
                    assert (row_i, column_i) in fileds_to_delete
                    continue
                assert (row_i, column_i) not in fileds_to_delete

        assert (
            field.get_find_special_bonus_affected_elements_status()
            == field.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_OK
        )

    def test_find_special_bonus_affected_elements_bonus_not_exists(self, field):
        fileds_to_delete = field.find_special_bonus_affected_elements("test", 0, 0)
        assert fileds_to_delete == []
        assert (
            field.get_find_special_bonus_affected_elements_status()
            == field.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_BONUS_NOT_EXIST
        )

    @pytest.mark.parametrize(
        "pos1, pos2",
        [
            ((0, 0), (-1, 0)),
            ((0, 0), (0, 100)),
            ((-1, 0), (0, 0)),
            ((0, 100), (0, 0)),
        ],
    )
    def test_find_special_bonus_affected_elements_out_of_bounds(
        self, field, pos1, pos2
    ):
        fileds_to_delete = field.find_special_bonus_affected_elements(
            "column_eliminate", pos1, pos2
        )
        assert fileds_to_delete == []
        assert (
            field.get_find_special_bonus_affected_elements_status()
            == field.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_OUT_OF_BOUNDS
        )

    def test_get_filed(self, field):
        field_matrix = field.get_field()

        for row in field_matrix:
            assert len(row) == len(field_matrix)
