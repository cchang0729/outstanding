import numpy as np
import matplotlib.pyplot as plt

class Kalman():
    #initialize R, Q
    def __init__(self, K=0, P=1, Q=1e-5, R=0.1**2):
        self.est = 0 
        self.K = K
        self.P = P
        self.Q = Q
        self.R = R 

    def getEstimation(self, meas ):
        self.K = (self.P + self.Q) / (self.P + self.Q + self.R)
        self.est = self.est + self.K*(meas - self.est)
        self.P = (1-self.K)*self.P
        return self.est

if __name__ == '__main__':

    plt.rcParams['figure.figsize'] = (10, 8)

# intial parameters
    n_iter = 50
    sz = (n_iter,) # size of array
    x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
    z = np.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)

    Q = 1e-5 # process variance

# allocate space for arrays
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor

    R = 0.1**2 # estimate of measurement variance, change to see effect

# intial guesses
    xhat[0] = 0.0
    P[0] = 1.0

    kal = Kalman()
    
    for k in range(1,n_iter):
        xhat[k] = kal.getEstimation(z[k])

    plt.figure()
    plt.plot(z,'k+',label='noisy measurements')
    plt.plot(xhat,'b-',label='a posteri estimate')
    plt.axhline(x,color='g',label='truth value')
    plt.legend()
    plt.title('Estimate vs. iteration step', fontweight='bold')
    plt.xlabel('Iteration')
    plt.ylabel('Voltage')

    plt.figure()
    valid_iter = range(1,n_iter) # Pminus not valid at step 0
    plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
    plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
    plt.xlabel('Iteration')
    plt.ylabel('$(Voltage)^2$')
    plt.setp(plt.gca(),'ylim',[0,.01])
    plt.show()
