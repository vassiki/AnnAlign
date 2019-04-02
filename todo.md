[ ] Return annotation vector that is same length as movie
[ ] Write tests for annotation function
[ ] Modify function to return labels of the dimension, not just 1's and 0's
[ ] - Function to take two annotation vectors (should be of the same length), check the amount of overall overlap. If the agreement is below a certain    level, just take the dominant annotation vector
    - If it is above the level, average the feature vectors (cosine similarity?) within a tolerance window. 
    - For every row in the resultant vector, take max correlations and decide whether to put 0 or 1   
