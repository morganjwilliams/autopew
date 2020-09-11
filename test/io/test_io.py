import unittest
import pathlib
import pandas as pd
import numpy as np
import inspect
from autopew.io import (
    get_filehandler,
    registered_extensions,
    PewIOSpecification,
    PewCSV,
    PewSCANCSV,
)
from pyrolite.util.general import temp_path, remove_tempdir


class TestGetRegisteredExtensions(unittest.TestCase):
    def setUp(self):
        pass

    def test_default(self):
        handlers = registered_extensions()
        # keys should be classes
        self.assertTrue(all([inspect.isclass(k) for k in handlers.keys()]))
        # values should be extensions
        self.assertTrue(all([isinstance(v, str) for v in handlers.values()]))


class TestGetHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_filehandler_from_file(self):
        valid_single_handler = [
            "mylasercoords.scancsv",
            "../mylasercoords.scancsv",
            pathlib.Path("../mylasercoords.scancsv"),
        ]
        for filepath in valid_single_handler:
            with self.subTest(filepath=filepath):
                handler = get_filehandler(filepath=filepath)
                self.assertTrue(issubclass(handler, PewIOSpecification))

        unregistered_filetypes = ["not_a_valid.filextension"]
        for filepath in unregistered_filetypes:
            with self.subTest(filepath=filepath):
                with self.assertRaises(IndexError):
                    handler = get_filehandler(filepath=filepath)

        invalid_filetypes = [".filextension"]
        for filepath in invalid_filetypes:
            with self.subTest(filepath=filepath):
                with self.assertRaises(NotImplementedError):
                    handler = get_filehandler(filepath=filepath)

    def test_get_filehandler_from_name(self):
        valid_names = [
            "PewCSV",
            "PewSCANCSV",
        ]
        for name in valid_names:
            with self.subTest(name=name):
                handler = get_filehandler(name=name)
                self.assertTrue(issubclass(handler, PewIOSpecification))

        invalid_names = ["PewALLTHELASERS"]
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(IndexError):
                    handler = get_filehandler(name=name)


class TestPewIOSpec(unittest.TestCase):
    def test_validate_input(self):
        handler = PewIOSpecification()
        handler.validate_input(pd.DataFrame(columns=["x", "y", "name"]))


class TestPewCSV(unittest.TestCase):
    def setUp(self):
        self.tempdir = temp_path()

    def test_init(self):
        handler = PewCSV()
        self.assertTrue(isinstance(handler, PewIOSpecification))

    def tearDown(self):
        try:
            remove_tempdir(self.fp)
        except:
            pass


class TestPewSCANSCV(unittest.TestCase):
    def setUp(self):
        self.tempdir = temp_path()

    def test_init(self):
        handler = PewSCANCSV()
        self.assertTrue(isinstance(handler, PewIOSpecification))

    def tearDown(self):
        try:
            remove_tempdir(self.fp)
        except:
            pass
