import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import math
from fractions import Fraction as fractions
from streamlit_option_menu import option_menu
from sympy import *
import re


def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    x_values = [a + i * h for i in range(n+1)]
    y_values = [f(x) for x in x_values]
    integral = (h / 2) * (y_values[0] + 2 * sum(y_values[1:n]) + y_values[n])
    return integral

def simpsons_rule(f, a, b, n):
    h = (b - a) / n
    x_values = [a + i * h for i in range(n+1)]
    y_values = [f(x) for x in x_values]

    # Check if the number of intervals is even
    if n % 2 != 0:
        raise ValueError("The number of intervals must be even for Simpson's rule.")

    # Apply Simpson's rule formula
    sum_odd = sum(y_values[1:n:2])
    sum_even = sum(y_values[2:n:2])
    integral = (h / 3) * (y_values[0] + 4 * sum_odd + 2 * sum_even + y_values[n])
    return integral

def eliminate_text_before_slash(string):
    index = string.find('/')
    if index != -1:
        return string[index+1:]
    return string

def split_fraction(text):
    # Remove spaces between operands and their preceding and succeeding operators
    text = re.sub(r'(?<=[+\-*/^])\s*(?=\d)|(?<=\d)\s*(?=[+\-*/^])\s*(?=\d)', '', text)

    # Split the expression by spaces
    tokens = re.split(r'\s+', text)
    tokens = [elem for i, elem in enumerate(tokens) if i % 2 != 1]
    tokens = [eliminate_text_before_slash(elem) for elem in tokens]
    return tokens


# Define an empty DataFrame
df = pd.DataFrame(columns=['Method', 'Function', 'Lower Limit', 'Upper Limit', 'Number of Intervals', 'Result'])

# Perform numerical integration and add the results to the DataFrame
def perform_integration(method, f, a, b, n):
    if method == 'Trapezoidal':
        result = trapezoidal_rule(f, a, b, n)
    elif method == 'Simpson':
        result = simpsons_rule(f, a, b, n)

    df.loc[len(df)] = [method, str(f), a, b, n, result]
    

#   Main function
def main():
    st.write("Numerical Integration")

    tab1, tab2= st.tabs(["Pre-defined", "User-defined"])
    with tab1:
        tab3, tab4= st.tabs(["Trapezoidal", "Simpson"])
        with tab3:
            st.title("Numerical Integration with Simpson's Rule")

            # Function input
            st.subheader("Function to Integrate: tanh(x)")
            function_input = 'math.tanh(x)'
            
            # Limits of integration
            st.subheader("Limits of Integration")
            lower_limit = st.number_input(" Lower Limit", value=0.0)
            upper_limit = st.number_input(" Upper Limit", value=1.0)

            # Number of trapezoids
            st.subheader("Number of Trapezoids")
            num_trapezoids = st.number_input("Enter the number of trapezoids", value=100, step=1)

            # Calculate the approximate integral
            try:
                lambda_function = eval("lambda x: " + function_input)
                perform_integration('Trapezoidal', lambda_function, lower_limit, upper_limit, num_trapezoids)
                st.subheader("Approximate Integral")
                st.write(df['Result'].iloc[-1])
            except Exception as e:
                st.subheader("Error")
                st.write(str(e))

        with tab4:
            st.title("Numerical Integration with Simpson's Rule")

            # Function input
            st.subheader("Function to Integrate: math.tanh(x)")
            function_input = 'math.tanh(x)'
            
            # Limits of integration
            st.subheader("Limits of Integration")
            lower_limit = st.number_input(" Lower Limit ", value=0.0)
            upper_limit = st.number_input(" Upper Limit ", value=1.0)

            # Number of intervals
            st.subheader("Number of Intervals")
            num_intervals = st.number_input("Enter the number of intervals", value=100, step=1)

            # Calculate the approximate integral
            try:
                lambda_function = eval("lambda x: " + function_input)
                perform_integration('Simpson', lambda_function, lower_limit, upper_limit, num_intervals)
                st.subheader("Approximate Integral")
                st.write(df['Result'].iloc[-1])
            except Exception as e:
                st.subheader("Error")
                st.write(str(e))
            

    with tab2:
        tab5, tab6= st.tabs(["Trapezoidal", "Simpson"])
        with tab5:
            st.title("Numerical Integration with Trapezoidal Rule")

            # Function input
            st.subheader("Function to Integrate")
            function_input = st.text_input("Enter a function (e.g., x ** 2, math.tanh(x))", value="x ** 2")
            function_input = function_input.replace("e", "math.e")
            function_input = function_input.replace("pi", "math.pi")
            function_input = function_input.replace("^", "**")
       
            # Limits of integration
            st.subheader("Limits of Integration")
            lower_limit = st.number_input("Lower Limit", value=0.0)
            upper_limit = st.number_input("Upper Limit", value=1.0)

            a = lower_limit
            b = upper_limit
            # Checks to see if it is in quotient form then splits it if so 
            if('/' in function_input):
                denoms = split_fraction(function_input)

                x = symbols('x')
                e = symbols('e')
                pi = symbols('pi')
                a = lower_limit
                b = upper_limit
                print(math.pi)

                results = []
                ctr = 0

                for fnb in denoms:
                    if fnb:
                        fnb = fnb.replace("math.","")
                        fbsym = sympify(fnb)

                    fbsyme = fbsym.subs(e, math.e)
                    fbsympi = fbsyme.subs(pi, math.pi)

                    equation = Eq(fbsympi, 0)   
                    roots = solve((equation, x >= a, x <= b), x)
                    results.append(roots)

                results = [x for x in results if x != False]

                if(len(results) > 0):
                    st.write("There is an/are element/s inside [a,b] where the function is undefined. ")  
                    st.write("C: ", results)
                else:
                    st.write("No roots.")

                    # Number of trapezoids
                    st.subheader("Number of Trapezoids")
                    num_trapezoids = st.number_input("Enter the number of trapezoids ", value=100, step=1)

                    # Calculate the approximate integral
                    try:
                        lambda_function = eval("lambda x: " + function_input)
                        perform_integration('Trapezoidal', lambda_function, lower_limit, upper_limit, num_trapezoids)
                        st.subheader("Approximate Integral")
                        st.write(df['Result'].iloc[-1])
                    except Exception as e:
                        st.subheader("Error")
                        st.write(str(e))
            else:
                # Number of trapezoids
                st.subheader("Number of Trapezoids")
                num_trapezoids = st.number_input("Enter the number of trapezoids  ", value=100, step=1)

                # Calculate the approximate integral
                try:
                    lambda_function = eval("lambda x: " + function_input)
                    perform_integration('Trapezoidal', lambda_function, lower_limit, upper_limit, num_trapezoids)
                    st.subheader("Approximate Integral")
                    st.write(df['Result'].iloc[-1])
                except Exception as e:
                    st.subheader("Error")
                    st.write(str(e))

        with tab6:
            st.subheader("Function to Integrate ")
            function_input = st.text_input("Enter a function (e.g., x ** 2, math.tanh(x)) ", value="x ** 2")
            function_input = function_input.replace("e", "math.e")
            function_input = function_input.replace("pi", "math.pi")

            # Limits of integration
            st.subheader("Limits of Integration ")
            lower_limit = st.number_input("Lower Limit ", value=0.0)
            upper_limit = st.number_input("Upper Limit ", value=1.0)

            a = lower_limit
            b = upper_limit
            # Checks to see if it is in quotient form then splits it if so 
            if('/' in function_input):
                denoms = split_fraction(function_input)

                x = symbols('x')
                e = symbols('e')
                pi = symbols('pi')
                a = lower_limit
                b = upper_limit
                print(math.pi)

                results = []
                ctr = 0

                for fnb in denoms:
                    if fnb:
                        fnb = fnb.replace("math.","")
                        fbsym = sympify(fnb)

                    fbsyme = fbsym.subs(e, math.e)
                    fbsympi = fbsyme.subs(pi, math.pi)

                    equation = Eq(fbsympi, 0)   
                    roots = solve((equation, x >= a, x <= b), x)
                    results.append(roots)

                results = [x for x in results if x != False]

                if(len(results) > 0):
                    st.write("There is an/are element/s inside [a,b] where the function is undefined. ")  
                    st.write("C: ", results)
                else:
                    st.write("No roots.")
                # Number of intervals
                st.subheader("Number of Intervals")
                num_intervals = st.number_input("Enter the number of intervals ", value=100, step=1)

                # Calculate the approximate integral
                try:
                    lambda_function = eval("lambda x: " + function_input)
                    perform_integration('Simpson', lambda_function, lower_limit, upper_limit, num_intervals)
                    st.subheader("Approximate Integral")
                    st.write(df['Result'].iloc[-1])
                except Exception as e:
                    st.subheader("Error")
                    st.write(str(e))
            else:
                # Number of intervals
                st.subheader("Number of Intervals")
                num_intervals = st.number_input("Enter the number of intervals ", value=100, step=1)

                # Calculate the approximate integral
                try:
                    lambda_function = eval("lambda x: " + function_input)
                    perform_integration('Simpson', lambda_function, lower_limit, upper_limit, num_intervals)
                    st.subheader("Approximate Integral")
                    st.write(df['Result'].iloc[-1])
                except Exception as e:
                    st.subheader("Error")
                    st.write(str(e))

    

if __name__ == "__main__":
    main()
