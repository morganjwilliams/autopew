import logging
import itertools
from autopew.transform import (
    affine_from_AB,
    transform_from_affine,
    inverse_affine_transform,
)


class CoordinateTransform(object):

    library = []

    def __init__(self, source, dest, *args, **kwargs):
        self.forward = None
        self.reverse = None
        self.source = source
        self.dest = dest
        # todo: methods for dealing with maximum dimensionality of the transform
        # if you create a 3D-3D transform you can keep all dims, but dims will be lost
        # for 3D-2D, and any subsequent transforms.
        self._register()

        if not (self.dest, self.source) in self._links:
            self._invert  # register inverse

        self._iter_library()

    @property
    def _links(self):
        return set(
            zip([i.source for i in self.library], [i.dest for i in self.library])
        )

    @property
    def _domains(self):
        return set([i.dest for i in self.library] + [i.source for i in self.library])

    def _register(self):
        """
        Register the Coordinate Transform in the Transform Library
        """
        if self not in self.library:
            self.library.append(self)
        else:
            logger.warning("Transform Already Exists in Library")

    def _iter_library(self):
        """
        Calibrate all relevant transforms between available sources and destination
        coordinate systems.
        """
        logger.debug("Iterating over transform library.")
        # identify all coordinate reference systems
        crs = self._domains
        present = set([(c.source, c.dest) for c in self.library])
        possible = itertools.product(crs, repeat=2)
        for a, b in possible:
            if (a != b) and ((a, b) not in present):
                print("Need to add ({}, {})".format(a, b))
                pass

    @property
    def _invert(self):
        logger.debug("Creating inverse for {}".format(str(self)))
        self.inverse = CoordinateTransform(self.dest, self.source)
        self.inverse.inverse = self
        self.inverse.forward, self.inverse.reverse = self.reverse, self.forward
        return self.inverse

    def calibrate(self, sourcepoints, destpoints):
        logger.debug("Calibrating {}".format(str(self)))
        self.affine = affine_from_AB(pixelpoints, transformpoints)
        self.forward = affine_transform(self.affine)
        self.reverse = inverse_affine_transform(self.affine)
        self.inverse.forward, self.inverse.reverse, self.inverse.affine = (
            self.reverse,
            self.forward,
            np.linalg.inv(self.affine),
        )

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return (self.source == other.source) and (self.dest == other.dest)
        else:
            return False

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.source, self.dest)

    def __str__(self):
        return "{} from {} to {}".format(
            self.__class__.__name__, self.source, self.dest
        )
