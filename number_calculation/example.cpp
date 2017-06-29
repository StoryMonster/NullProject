#include <iostream>
#include "CalculateExpression.hpp"

int main()
{
    std::string expr1("3-2*4 +5");
    std::string expr2("(12-4)*2-3");
    std::string expr3("-34 + 20 * 10");
    std::string expr4("-(12-9)");
    std::string expr5("22");
    std::cout << expr1 << '=' << CalculateExpression::calculateExpression(expr1) << std::endl;
    std::cout << expr2 << '=' << CalculateExpression::calculateExpression(expr2) << std::endl;
    std::cout << expr3 << '=' << CalculateExpression::calculateExpression(expr3) << std::endl;
    std::cout << expr4 << '=' << CalculateExpression::calculateExpression(expr4) << std::endl;
    std::cout << expr5 << '=' << CalculateExpression::calculateExpression(expr5) << std::endl;
}

