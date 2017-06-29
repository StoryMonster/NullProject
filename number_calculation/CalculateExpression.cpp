#include "CalculateExpression.hpp"

namespace
{
template<typename T>
class Queue : public std::queue<T>
{
public:	
    T pop_first()
    {
        T res = std::queue<T>::front();
        std::queue<T>::pop();
        return res;
    }
};

class OpQueue : public Queue<char>
{
};

class NumQueue : public Queue<double>
{
};
}

namespace CalculateExpression
{
double calcFromQueues(OpQueue& opQueue, NumQueue& numQueue)
{
    OpQueue newOpQueue;
    NumQueue newNumQueue;
    double temp = numQueue.pop_first();
    while(opQueue.size())
    {
        char op = opQueue.pop_first();
        double num = numQueue.pop_first();
        if(op == '+' || op == '-')
        {
            newOpQueue.push(op);
            newNumQueue.push(temp);
            temp = num;
        }
        else temp = (op == '*') ? (temp * num) : (temp / num);
    }
    newNumQueue.push(temp);
    double res = newNumQueue.pop_first();
    while(newOpQueue.size())
    {
        char op = newOpQueue.pop_first();
        double num = newNumQueue.pop_first();
        res = (op == '+') ? (res + num) : (res - num);
    }
    return res;
}

std::string getExpressionInBracket(const std::string& originExpr)
{
    std::uint8_t lBracketCount = 0, rBracketCount = 0;
    std::uint32_t startIndex = 0, endIndex = originExpr.size() - 1;
    for(std::uint32_t i = 0; i < originExpr.size(); ++i)
    {
        if(originExpr[i] == '(')
        {
            if(0 == lBracketCount)
            {
                startIndex = i;
            }
            ++lBracketCount;
        }
        else if(originExpr[i] == ')')
        {
            ++rBracketCount;
            if(lBracketCount == rBracketCount)
            {
                endIndex = i;
                break;
            }
        }
     }
     return originExpr.substr(startIndex+1, endIndex - startIndex - 1);
}

double parserExpressionAndCalculate(const std::string expr)
{
    OpQueue opQueue;
    NumQueue numQueue;
    if('-' == expr[0]) numQueue.push(0);
    for(std::uint32_t i = 0; i < expr.size(); ++i)
    {
        if(expr[i] == '+' || expr[i] == '-' || expr[i] == '*' || expr[i] == '/')
        {
            opQueue.push(expr[i]);
        }
        else if(expr[i] == '(')
        {
            std::string subExpr = getExpressionInBracket(expr.substr(i, expr.size() - i));
            numQueue.push(parserExpressionAndCalculate(subExpr));
            i += (subExpr.size() + 1);
        }
        else if(expr[i] >= '0' && expr[i] <= '9')
        {
            std::string str;
            for(std::uint32_t j = i; j < expr.size(); ++j)
            {
            	if(j == expr.size() - 1)
            	{
                    str = expr.substr(i, j-i+1);
                    numQueue.push(atof(str.c_str()));
                    i = j;
                    break;
            	}
                else if((expr[j] > '9' || expr[j] < '0') && expr[j] != '.')
                {
                    str = expr.substr(i, j-i);
                    numQueue.push(atof(str.c_str()));
                    i = j-1;
                    break;
                }
            }
        }
        else
        {
            throw std::runtime_error("error expression!");
        }
    }
    return calcFromQueues(opQueue, numQueue);
}

std::string deleteCharactorInString(const std::string& str, const char ch)
{
    std::string res;
    for(const auto& elem : str)
    {
        if(elem != ch)
        {
            res += elem;
        }
    }
    return res;
}

double calculateExpression(const std::string& expr)
{
    try
    {
        return parserExpressionAndCalculate(deleteCharactorInString(expr, ' '));
    }
    catch(std::runtime_error e)
    {
        std::cout << e.what() << std::endl;
    }
}
}
