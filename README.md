# Questions?!?!?!


Q) Description of code:

Q) parts to be distributed and parallelized? and why?
    1) Fitness evaluation is the sequential part so it should be parallelized O(n),
    2) Population Regeneration because its O(n^2)



Q) What Algorithm enhancement?
    1) eewrote fitness calculation to be more efficient.
    2) kept the best 10% of routes instead of fully regenerating on stagnation.
    
Q) How would u add cars to the problem?
    1) Instead of one route per individual, each individual would represent multiple routes, one for each car.
    2) Instead of a single distance, the fitness function should sum the distances of all cars while balancing the load.

--------------------outputs:-----------------------

### city_distances.csv
sequential part:
Total Distance: -1187.0
Total Time: 19.04 seconds

parallel part:
Total Distance: -1247.0
Total Time: 121.83 seconds

enhanced part:
Total Distance: -1104.0
Total Time: 28.70 seconds

### city_distances_extended.csv

Total Distance: -304713.0
Total Time: 71.2382082939148
