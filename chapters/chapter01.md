### Qbits

These are Quantum Bits. They don't have a known value until they are "read" at which point they "collapse". They collapse to either 1 or 0, probabilistically. 

So if I create the same Qbit 1000 times and read it over and over, I will get a mix of zeros and ones. The mix will depend on certain properties of the Qbit which we call amplitudes. They are two numbers, alpha and beta.

The simplest case is with alpha = and beta = in which case the qbit has a 50/50 chance of becoming a 1 or 0. 

#### Here we illustrate a series of experiments where we "read" a single qbit over and over again.

:visualize qubit-grid 20



#### If we were to do many more experiments you see that the count of those that resolve to "1" is about the same as those who resolve to 2.

:visualize single-qubit 500

Assume that we created a Qbit with these amplitudes, abd then collapsed it, how many zeros and how many ones would we get? 

