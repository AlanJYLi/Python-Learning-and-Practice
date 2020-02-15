from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}
        

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        
        def find_best_numeric(X, y, split_attribute):
            '''
            find the split value (mean or median) with largest IG for a continuous variable
            Inputs:
                X: data containing all attributes
                y: labels
            split_attribute: column index of the attribute to split on
            '''
            if isinstance(np.array(X)[:, split_attribute][0], np.int32) or isinstance(np.array(X)[:, split_attribute][0], np.float64):
                all_values = [val for val in np.array(X)[:, split_attribute]]
            else:
                all_values = [ast.literal_eval(val) for val in np.array(X)[:, split_attribute]]
            median = np.median(all_values)
            mean = np.mean(all_values)
            best_ig = 0
            best_val = 0
            for val in (median, mean):
                y_left = partition_classes(X, y, split_attribute, val)[2]
                y_right = partition_classes(X, y, split_attribute, val)[3]
                if len(y_left)*len(y_right) != 0:
                    ig = information_gain(y, [y_left,y_right])
                    if ig >= best_ig:
                        best_ig = ig
                        best_val = val
                else:
                    continue
            return best_ig, best_val

        def find_best_category(X, y, split_attribute):
             '''
             find the split value with largest IG for a category variable
             Inputs:
                 X: data containing all attributes
                 y: labels
                 split_attribute: column index of the attribute to split on
             '''
             all_values = set(np.array(X)[:, split_attribute]) # get all values in the category variable
             best_ig = 0
             best_val = 0
             for val in all_values:
                 y_left = partition_classes(X, y, split_attribute, val)[2]
                 y_right = partition_classes(X, y, split_attribute, val)[3]
                 if len(y_left)*len(y_right) != 0:
                     ig = information_gain(y, [y_left,y_right])
                     if ig >= best_ig:
                         best_ig = ig
                         best_val = val
                 else:
                     continue
             return best_ig, best_val
    
        def find_best_spliter(X, y):
            '''
            find the best attribute with best value to split the data
            '''
            column_num = -1
            ig_max = 0
            split_value = 0
            for i in range(len(X[0])):
                if isinstance(X[0][i], int) or isinstance(X[0][i], float):
                    ig, value = find_best_numeric(X, y, i)
                else:
                    ig, value = find_best_category(X, y, i)
                if ig > ig_max:
                    ig_max = ig
                    column_num = i
                    split_value = value
            return column_num, split_value, ig_max

        def terminate(node):
            '''
            Determine whether or not a node need to be splited
            return None - need split
            return 1 or 0 - it's should be a leaf
            Rules:
                1. number of data points <= 500 (rule of thumb: size of leaf at least 5% of total sample)
                2. if number of data points >500
                   1) pure
                   2) no more information gain
                   3) the proportion of one class is over 95%
                   4) all points from one class completely overlap with points from another class
            '''
            y = node['response']
            a = y.count(1)  # number of positive response
            b = y.count(0)  # number of negative response
            result = 1 if a>=b else 0
            if len(y) <= 500:  # number of data points <= 500 
                return result
            else:
                if a == 0 or b == 0:  # pure
                    return result
                if node['maxig'] == 0:  # no information gain
                    return result
                if a/(a+b) >= 0.95 or a/(a+b) <= 0.05:  # proportion of one class is over 95%
                    return result
                X = node['data']  # deal with all points from one class completely overlap with points from another class
                X_major = []
                X_minor = []
                for i in range(len(y)):
                    if y[i] != result:
                        X_minor.append(X[i])
                    else:
                        X_major.append(X[i])
                for row in X_minor:
                    if row in X_major:
                        continue
                    else:
                        return None
                return result
            return None
            
        def build_node(X, y, selfid='0', parentid=None):
            '''
            build a node
            '''
            split_attribute, split_val, ig_max = find_best_spliter(X, y)
            node = {'data': X, 'response': y, 
                    'leftbranchid': None, 'rightbranchid': None, 
                    'parentid': parentid, 'selfid': selfid, 
                    'splitcolumn': split_attribute, 'splitvalue': split_val, 
                    'maxig': ig_max, 'classification': None}
            result = terminate(node)
            if result != None:
                node['classification'] = result
            else:
                leftbranchid = selfid+'0'
                rightbranchid = selfid+'1'
                node['leftbranchid'] = leftbranchid
                node['rightbranchid'] = rightbranchid
            return node

        def build_children(node):
            '''
            given a node, build its children if needed
            '''
            if node['classification'] == None:
                X_left, X_right, y_left, y_right = partition_classes(node['data'], node['response'], node['splitcolumn'], node['splitvalue'])
                nodeleft = build_node(X_left, y_left, node['leftbranchid'], node['selfid'])
                noderight = build_node(X_right, y_right, node['rightbranchid'], node['selfid'])
                return nodeleft, noderight
            else:
                return 0,0
        
        def build_tree(node):
            left,right = build_children(node)
            # function in util
            # if node is a leaf, it will return 0,0
            # if node is not a leaf, it will return left child node and right child node
            if left != 0 and right != 0:
                self.tree[left['selfid']] = left
                self.tree[right['selfid']] = right
                build_tree(left)
                build_tree(right)
        
        node = build_node(X, y, selfid='0', parentid=None) # root of the tree
        self.tree[node['selfid']] = node
        build_tree(node)
            
        
    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        def track_down(node_id):
            node = self.tree[node_id]
            if node['classification'] != None:
                return node['classification']
            else:
                value = record[node['splitcolumn']]
                if isinstance(value, int) or isinstance(value, float):
                    if value <= node['splitvalue']:
                        go_to = node['leftbranchid']
                        return track_down(go_to)
                    else:
                        go_to = node['rightbranchid']
                        return track_down(go_to)
                else:
                    if value == node['splitvalue']:
                        go_to = node['leftbranchid']
                        return track_down(go_to)
                    else:
                        go_to = node['rightbranchid']
                        return track_down(go_to)
         
        prediction = track_down('0')
        return prediction