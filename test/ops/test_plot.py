"""
Tests for plotting operations
"""

import itertools
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from unittest import TestCase

import numpy as np
import pandas as pd
import xarray as xr

from cate.core.op import OP_REGISTRY
from cate.ops.plot import plot, plot_map, plot_dataframe, FigureRegistry
from cate.util.misc import object_to_qualified_name

_counter = itertools.count()
ON_WIN = sys.platform == 'win32'


@contextmanager
def create_tmp_file(name, ext):
    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, '{}{}.{}'.format(name,
                                                  next(_counter),
                                                  ext))
    try:
        yield path
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError:
            if not ON_WIN:
                raise


@unittest.skipIf(condition=os.environ.get('CATE_DISABLE_PLOT_TESTS', None),
                 reason="skipped if CATE_DISABLE_PLOT_TESTS=1")
class TestPlotMap(TestCase):
    """
    Test plot_map() function
    """

    def test_plot_map(self):
        # Test the nominal functionality. This doesn't check that the plot is what is expected,
        # rather, it simply tests if it seems to have been created
        dataset = xr.Dataset({
            'first': (['lat', 'lon', 'time'], np.random.rand(5, 10, 2)),
            'second': (['lat', 'lon', 'time'], np.random.rand(5, 10, 2)),
            'lat': np.linspace(-89.5, 89.5, 5),
            'lon': np.linspace(-179.5, 179.5, 10),
            'time': pd.date_range('2000-01-01', periods=2)})

        with create_tmp_file('remove_me', 'png') as tmp_file:
            plot_map(dataset, file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))

        # Test if an error is raised when an unsupported format is passed
        with create_tmp_file('remove_me', 'pgm') as tmp_file:
            with self.assertRaises(ValueError):
                plot_map(dataset, file=tmp_file)
            self.assertFalse(os.path.isfile(tmp_file))

        # Test if extents can be used
        with create_tmp_file('remove_me', 'pdf') as tmp_file:
            plot_map(dataset,
                     var='second',
                     region='-40.0, -20.0, 50.0, 60.0',
                     file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))

        # Test time slice selection
        with create_tmp_file('remove_me', 'png') as tmp_file:
            plot_map(dataset, time='2000-01-01', file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))

    def test_plot_map_exceptions(self):
        # Test if the corner cases are detected without creating a plot for it.

        # Test value error is raised when passing an unexpected dataset type
        with create_tmp_file('remove_me', 'jpeg') as tmp_file:
            with self.assertRaises(NotImplementedError):
                plot_map([1, 2, 4], file=tmp_file)
            self.assertFalse(os.path.isfile(tmp_file))

        # Test the extensions bound checking
        dataset = xr.Dataset({
            'first': (['lat', 'lon', 'time'], np.random.rand(2, 4, 1)),
            'lat': np.linspace(-89.5, 89.5, 2),
            'lon': np.linspace(-179.5, 179.5, 4)})

        with self.assertRaises(ValueError):
            region = '-40.0, -95.0, 50.0, 60.0',
            plot_map(dataset, region=region)

        with self.assertRaises(ValueError):
            region = '-40.0, -20.0, 50.0, 95.0',
            plot_map(dataset, region=region)

        with self.assertRaises(ValueError):
            region = '-181.0, -20.0, 50.0, 60.0',
            plot_map(dataset, region=region)

        with self.assertRaises(ValueError):
            region = '-40.0, -20.0, 181.0, 60.0',
            plot_map(dataset, region=region)

        with self.assertRaises(ValueError):
            region = '-40.0, -20.0, 50.0, -25.0',
            plot_map(dataset, region=region)

        with self.assertRaises(ValueError):
            region = '-20.0, -20.0, -25.0, 60.0',
            plot_map(dataset, region=region)

        # Test temporal slice validation
        with self.assertRaises(ValueError):
            plot_map(dataset, time=0)

    def test_registered(self):
        """
        Test nominal execution of the function as a registered operation.
        """
        reg_op = OP_REGISTRY.get_op(object_to_qualified_name(plot_map))
        dataset = xr.Dataset({
            'first': (['lat', 'lon', 'time'], np.random.rand(5, 10, 2)),
            'second': (['lat', 'lon', 'time'], np.random.rand(5, 10, 2)),
            'lat': np.linspace(-89.5, 89.5, 5),
            'lon': np.linspace(-179.5, 179.5, 10),
            'time': pd.date_range('2000-01-01', periods=2)})

        with create_tmp_file('remove_me', 'png') as tmp_file:
            reg_op(ds=dataset, file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))


@unittest.skipIf(condition=os.environ.get('CATE_DISABLE_PLOT_TESTS', None),
                 reason="skipped if CATE_DISABLE_PLOT_TESTS=1")
class TestPlot(TestCase):
    """
    Test plot() function
    """

    def test_plot(self):
        # Test plot
        dataset = xr.Dataset({
            'first': np.random.rand(10)})

        with create_tmp_file('remove_me', 'jpg') as tmp_file:
            plot(dataset, 'first', file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))

    def test_registered(self):
        """
        Test nominal execution of the function as a registered operation.
        """
        reg_op = OP_REGISTRY.get_op(object_to_qualified_name(plot))
        # Test plot
        dataset = xr.Dataset({
            'first': np.random.rand(10)})

        with create_tmp_file('remove_me', 'jpg') as tmp_file:
            reg_op(ds=dataset, var='first', file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))


@unittest.skipIf(condition=os.environ.get('CATE_DISABLE_PLOT_TESTS', None),
                 reason="skipped if CATE_DISABLE_PLOT_TESTS=1")
class TestPlotDataFrame(TestCase):
    """
    Test plot_dataframe() function.
    """

    def test_nominal(self):
        """
        Test nominal execution
        """
        data = {'A': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                'B': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
        df = pd.DataFrame(data=data, index=pd.date_range('2000-01-01',
                                                         periods=10))

        with create_tmp_file('remove_me', 'png') as tmp_file:
            plot_dataframe(df, file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))

    def test_registered(self):
        """
        Test the method when run as a registered operation
        """
        reg_op = OP_REGISTRY.get_op(object_to_qualified_name(plot_dataframe))

        data = {'A': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                'B': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
        df = pd.DataFrame(data=data, index=pd.date_range('2000-01-01',
                                                         periods=10))

        with create_tmp_file('remove_me', 'png') as tmp_file:
            reg_op(df=df, file=tmp_file)
            self.assertTrue(os.path.isfile(tmp_file))


class TestFigureRegistry(TestCase):
    class Figure:
        def __repr__(self):
            return "Figure@%s" % id(self)

    def test_it(self):
        registry = FigureRegistry()
        figure1 = TestFigureRegistry.Figure()
        figure2 = TestFigureRegistry.Figure()
        figure3 = TestFigureRegistry.Figure()
        registry.add_entry(5, figure1)
        registry.add_entry(7, figure2)
        registry.add_entry(13, figure3)
        self.assertEqual(registry.figures, [figure1, figure2, figure3])
        registry.remove_entry(13)
        registry.remove_entry(5)
        self.assertEqual(list(registry.figures), [figure2])
        self.assertEqual(list(registry.entries), [(figure2, dict(figure_id=7))])
        self.assertEqual(registry.has_entry(5), False)
        self.assertEqual(registry.has_entry(11), False)
        self.assertEqual(registry.has_entry(13), False)
        self.assertEqual(registry.get_entry(13), None)
        self.assertEqual(registry.has_entry(7), True)
        self.assertEqual(registry.get_entry(7), (figure2, dict(figure_id=7)))

    def test_observer(self):
        registry = FigureRegistry()
        observations = []

        def observer(event, entry):
            observations.append([event, entry])

        registry.add_observer(observer)
        figure1 = TestFigureRegistry.Figure()
        figure2 = TestFigureRegistry.Figure()
        figure3 = TestFigureRegistry.Figure()
        registry.add_entry(13, figure1)
        registry.add_entry(14, figure2)
        registry.add_entry(13, figure3)
        registry.remove_entry(14)
        registry.remove_entry(13)
        registry.remove_entry(13)
        self.assertEqual(observations,
                         [
                             ['entry_added', (figure1, {'figure_id': 13})],
                             ['entry_added', (figure2, {'figure_id': 14})],
                             ['entry_updated', (figure3, {'figure_id': 13})],
                             ['entry_removed', (figure2, {'figure_id': 14})],
                             ['entry_removed', (figure3, {'figure_id': 13})]
                         ])

        observations = []
        registry.remove_observer(observer)
        registry.add_entry(15, TestFigureRegistry.Figure())
        self.assertEqual(observations, [])
