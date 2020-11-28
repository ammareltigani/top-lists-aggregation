import mallows_kendall as mk
import numpy as np
import collections
from collections import Counter

def generateSample(n,k_distribution,theta=None,phi=None,s0=None):
    """This function generates a single sample according
    to Mallows Models adapted to top-k rankings given a parameter of dispersion
    (theta or phi), where the values of k are controlled by k_distribution
        Parameters
        ----------
        n: int
            The number of candidates considered by rankers. Note that
            k <= n, since rankers cannot create preference lists that
            rank more candidates than exist.
        theta: float, optional (if phi given)
            The dispersion parameter theta
        phi: float, optional (if theta given)
            The dispersion parameter phi
        k_distribution: dict [int : int]
            The provided dictionary indicates the quantity of
            lists in the returned sample of each length. A given
            [key : value] entry dictates that value top-key-lists will
            be created in the resulting sample.
        s0: ndarray
            The consensus ranking. The identity ranking by default.
        Returns
        -------
        ndarray
            The top-lists generated
    """
    return np.array([rank[:k] for
        rank in mk.sampling_top_k_rankings(freq, n, k, theta, phi, s0) for
        k, freq in k_distribution])

def generateSamples(n,k_distribution,thetas=None,phis=None,s0=None):
    """Generates one sample for each parameter of dispersion given, i.e.
        for each theta or for each phi
        Parameters
        ----------
        n: int
            The number of candidates considered by rankers. Note that
            k <= n, since rankers cannot create preference lists that
            rank more candidates than exist.
        theta: list of floats, optional (if phi given)
            The dispersion parameter theta
        phi: list of floats, optional (if theta given)
            The dispersion parameter phi
        k_distribution: dict [int : int]
            The provided dictionary indicates the quantity of
            lists in the returned sample of each length. A given
            [key : value] entry dictates that value top-key-lists will
            be created in the resulting sample.
        s0: ndarray
            The consensus ranking. The identity ranking by default.
        Returns
        -------
        ndarray
            List of samples generated
    """
    return np.array([generateSample(n, theta, phi, s0) for
            theta, phi in zip(thetas, phis)])

    def poissonSample(m, lower = 0, upper = float('inf'), lda):
        """Returns m values drawn from a Poisson distribution on lambda for
            which all values are in [lower, upper] through repeated sampling.
            Not guaranteed to terminate.
            Parameters
            ----------
            m: int
                The number of elements in the requested sample
            lower: int
                Lowerbound of the sampled values
            upper: int
                Upperbound of the sampled values.
            lda: float
                The lambda parameter on which the Poisson distribution is
                defined.
        """
        rng = np.random.default_rng()
        # Samples are drawn repeatedly until enough values
        # reside in [lower,upper]
        while true:
            s = rng.poisson(lda, m)
            s = np.where(lower <= s <= upper)
            if len(s) >= n:
                return s[:n]
            # Double the number of values sampled each time to
            # increase the chance that sufficient values lay in [lower,upper]
            m *= 2

    def samplesFromPoisson(m,n,lda,thetas=None,phis=None,s0=None):
    """Generates one sample for each parameter of dispersion given, i.e.
        for each theta or for each phi, and where
        the lengths of rankers' top-lists are sampled a from a Poisson
        Poisson distribution on lda. The trunctation ensures all
        voters rank at least one candidate, and no voter ranks more than n
        candidates. Formally, with m lists, we define one m_i for
        each i in [1,m], where each m_i is randomly sampled from a truncated
        Poisson distribution. Then, we have a top-m_i-list in the sample for
        each m_i.

        Parameters
        ----------
        m: int
            The number of rankings to generate
        n: int
            The number of candidates considered by rankers.
        lda: float
            The parameter on which the Poisson distribution is defined, short
            for lambda.
            If lda is an integer, the median number of candidates
            ranked by voters will be lda.
        theta: list of floats, optional (if phi given)
            The dispersion parameter theta
        phi: list of floats, optional (if theta given)
            The dispersion parameter phi
        s0: ndarray
            The consensus ranking. The identity ranking by default.
        Returns
        -------
        ndarray
            List of samples generated
    """
    k_distribution = Counter(poissonSample(m, 1, n, lda))
    return generateSamples(n,k_distribution,thetas,phis,s0)

    # Main function generates synthetic data-sets using the Mallows-Model
    # and saves the output in CSV format. The data-sets are made for the
    # the following dispersion parameters: theta = 0, theta = .1
    # For each value of theta, two samples are generated, one where all
    # lists rank the top 5 of 10 candidates, and another where top-lists have
    # their lengths sampled from a Poisson distribution.
    # Note: Primarily for testing and debugging.
    if __name__ == '__main__':
        
