import math
import re

class Derivate:
    #https://qcweb.qc.edu.hk/math/Resource/AL/Derivative%20Table.pdf
    
    derivatives_descriptions = {
        "constant"                      : "c'",
        "var to power"                  : "x^n",
        "root of var"                   : "√^x",
        "constant over var"             : "1/x", 
        "constant*var"                  : "(c*u)'",
        "addition of functions"         : "(u+v)'",    
        "subtraction of functions"      : "(u-v)'", 
        "multiplication of functions"   : "(u*v)'", 
        "division of functions"         : "(u/v)'", 
        "function to power"             : "(u^n)'"
    }
    
    derivatives_formulas = {
        "c'"        : 0             ,
        "x^n"       : n * x^(n-1) ,
        "√^x"       : 1/(2*(root(x)))  ,
        "1/x"       : -(1/x^2),
        "c*u"       : c*Derivate._function_derivate(u)
        # "(c*u)'"    : c*u        ,
        #"(u+v)'"    : u' + v'     ,
        #"(u-v)'"    : u' - v'"     ,
        #"(u*v)"     : "u'*v + u*v'" ,
        #"(u/v)"     : "(u'*v - u*v')/(v^2)",
        #"(u^n)'"    : "n * u^(n-1) * u'" """
    }

    @staticmethod
    def get_derivative(node):
        Derivate._determine_category(node)

    def _determine_category(node):
        operands = node.get_operands()[0].get_operands()
        operator = node.get_operands()[0].get_operator()

        for operand in operands:
            print("Operand: ", operand)

    def function_derivative(function)

        

        


class MathExpression:
    feasible_operations = ["^","*","/","+","-"]
    operation_start_index = {}

    def __init__(self,expression,variable):
        
        self.clean_expression=expression.replace(" ", "")
        for operator in self.feasible_operations:
            if operator in self.clean_expression:
                
                self.operation_start_index[operator]=[i for i in range(len(self.clean_expression)) if self.clean_expression.startswith(operator, i)]
                
                for position in self.operation_start_index[operator]:
                    expression_as_list = list(self.clean_expression)
                    
                    left_bracket_start=position-1
                    right_bracket_end=position+2

                    while (True):

                        if expression_as_list[left_bracket_start]=='}':
                            left_bracket_start = self._find_closing_bracket(left_bracket_start, expression_as_list, '}')

                        if expression_as_list[left_bracket_start] in self.feasible_operations:
                            expression_start=left_bracket_start+1
                            expression_as_list.insert(expression_start, '{')
                            self._fix_operation_start_indexes(expression_start, operator)
                            break
                        elif left_bracket_start==0:
                            expression_start=left_bracket_start
                            expression_as_list.insert(expression_start, '{')
                            self._fix_operation_start_indexes(expression_start, operator)
                            break

                        if (left_bracket_start>=0):
                            left_bracket_start=left_bracket_start-1 
                        else:
                             left_bracket_start=0
                    
                    while (True):

                        if expression_as_list[right_bracket_end]=='{':
                            right_bracket_end = self._find_closing_bracket(right_bracket_end, expression_as_list, '{')

                        if right_bracket_end<len(expression_as_list):
                            if expression_as_list[right_bracket_end] in self.feasible_operations:
                                expression_end=right_bracket_end
                                expression_as_list.insert(expression_end, '}') 
                                self._fix_operation_start_indexes(expression_end, operator)
                                break
                            elif right_bracket_end==len(expression_as_list)-1:
                                expression_end=right_bracket_end+1
                                expression_as_list.insert(expression_end, '}')
                                self._fix_operation_start_indexes(expression_end, operator)
                                break
                        else:
                            expression_as_list.append('}')
                            expression_end=len(expression_as_list)-1
                            break

                        if (right_bracket_end<len(expression_as_list)):
                            right_bracket_end=right_bracket_end+1
                        else:
                             right_bracket_end=len(expression_as_list)-1

                    self.clean_expression="".join(expression_as_list)
                    #_extract_expression_node(self.clean_expression,expression_start,expression_end,operator)

        print("Program will read expression as \n   ", self.clean_expression)

    def get_operator_indexes(self):
        print(self.operation_start_index)

    def get_variable_loc_indexes(self):
        print(self.variable_loc_index)

    def _find_closing_bracket(self, current_position, expression_as_list, bracket):
        if bracket=='{':
            match='}'
            range_start=current_position+1
            range_end=len(expression_as_list)
            step=1
        elif bracket=='}':
            match='{'
            range_start=current_position-1
            range_end=-1
            step=-1

        i=range_start
        while(i!=range_end):
            if expression_as_list[i]==match:
                return i+step if i>0 else 0
            elif expression_as_list[i]==bracket:
                i=self._find_closing_bracket(i, expression_as_list, bracket)
            else:
                i+=step

            
        """ for i in range(range_start,range_end,step):
            if expression_as_list[i]==match:
                return i+step
            elif expression_as_list[i]==bracket:
                self._find_closing_bracket(current_position, expression_as_list, bracket) """

    def _fix_operation_start_indexes(self, position, operator):
        for i in range(len(self.operation_start_index[operator])):
            if self.operation_start_index[operator][i]>=position:
                self.operation_start_index[operator][i]+=1

    def _create_operation_tree(self,start_position):
        operands=[]
        operator = None
        expression_end = None
        i=start_position

        while(i<len(self.clean_expression)):
            if self.clean_expression[i]=='{':
                operand, i = self._create_operation_tree(i+1)
                operands.append(operand)
            elif self.clean_expression[i]=='}':
                expression_end=i
                break
            elif self.clean_expression[i] in self.feasible_operations:
                operator = self.clean_expression[i]
            else:
                operands.append(self.clean_expression[i])

            i+=1
        
        return MathOperationNode(operator,operands), expression_end

    def calc_derivative(self):
        operation_tree, i = self._create_operation_tree(0)
        print("Operations will be carried out in the following order: \n")
        for operand in operation_tree.get_operands():
            self._print_operation_order(operand,"")

        Derivate.get_derivative(operation_tree)

        


    def _print_operation_order(self,operation_node,return_string):
        first_term=True
        for operand in operation_node.get_operands():
            if first_term:
                first_term=False
            else:
                return_string+=operation_node.get_operator()
            
            if isinstance(operand, MathOperationNode):
                returned_string=self._print_operation_order(operand,"")
                #print(returned_string+"\n")
                return_string+='('+returned_string+')'
            else:
                return_string+=operand

        print(return_string+"\n")  
        return return_string
            

            


class MathOperationNode:
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def get_operator(self):
        return self.operator

    def get_operands(self):
        return self.operands

    def get_operands_size(self):
        return len(self.operands)

expression = MathExpression("2*x","x")
#expression = MathExpression("3*x^2 + 2*x ","x")
#expression = MathExpression("3*x^2 + 2*x/4","x")
expression.calc_derivative()
""" variable = input("Type the letter of the variable: ")
while (True):
    expression_str = input("Type expression to find the derivative of: ")
    if expression_str.find(variable)>0:
        break
    else:
        print("\nPlease enter your declared variable in the expression") """
    
#expression = MathExpression(expression_str,variable)
#expression.get_operator_indexes()
#expression.get_variable_loc_indexes()