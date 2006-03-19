import numpy as N
import numpy.linalg as L
import scipy
import enthought.traits as traits
import utils, regression

class Contrast(traits.HasTraits):
    """
    This class is used to construct contrast matrices in regression models.
    They are specified by terms in a formula, not contrast matrices. See
    the formula module.

    Here \'term\', T,  is a linear combination of columns of the design
    matrix D, generated by \'formula\'. The getmatrix method constructs
    a contrast matrix C so that

    colspan(dot(D, C)) = colspan(dot(D, dot(pinv(D), T)))

    where pinv(D) is the generalized inverse of D. Further, the matrix

    Tnew = dot(C, D)

    is full rank. The rank attribute is the rank of

    dot(D, dot(pinv(D), T))

    In a regression model, the contrast tests that E(dot(Tnew, Y)) = 0
    for each column of Tnew.

    """

    matrix = traits.Any()
    rank = traits.Int()
    name = traits.Str()

    def __init__(self, term, formula, name='', **keywords):
        self.term = term
        self.formula = formula
        if name is '':
            self.name = str(term)
        else:
            self.name = name

    def __str__(self):
        return '<contrast:%s>' % `{'term':str(self.term), 'formula':str(self.formula)}`

    def getmatrix(self, evaldesign=True, **keywords):
        """
        Construct a contrast matrix to test self.term in self.formula.
        """

        T = N.transpose(N.array(self.term(**keywords)))

        T = utils.clean0(T)
        q = T.shape[1]

        if evaldesign:
            self.D = self.formula.design(**keywords)
            self.pinv = L.generalized_inverse(self.D)

        self.matrix = regression.contrastfromcols(T, self.D)
        try:
            self.rank = self.matrix.shape[1]
        except:
            self.rank = 1
