#include <iostream>
using namespace std;

struct State
{
    int explorers;
    int guardians;
    int boat;
    int parent;
};

bool safeState(int explorers, int guardians)
{
    if (explorers < 0 || explorers > 3 || guardians < 0 || guardians > 3)
        return false;

    if (explorers > 0 && guardians > explorers)
        return false;

    int otherExplorers = 3 - explorers;
    int otherGuardians = 3 - guardians;

    if (otherExplorers > 0 && otherGuardians > otherExplorers)
        return false;

    return true;
}

int main()
{
    State list[100];

    int front = 0;
    int back = 0;

    bool visited[4][4][2] = {};

    int explorerMove[5] = {0, 0, 1, 2, 1};
    int guardianMove[5] = {1, 2, 0, 0, 1};

    State start;

    start.explorers = 3;
    start.guardians = 3;
    start.boat = 0;
    start.parent = -1;

    list[back] = start;
    back++;

    visited[3][3][0] = true;

    int goal = -1;

    while (front < back)
    {
        int currentNumber = front;
        State current = list[front];
        front++;

        if (current.explorers == 0 &&
            current.guardians == 0 &&
            current.boat == 1)
        {
            goal = currentNumber;
            break;
        }

        for (int i = 0; i < 5; i++)
        {
            State next = current;

            if (current.boat == 0)
            {
                next.explorers = current.explorers - explorerMove[i];
                next.guardians = current.guardians - guardianMove[i];
                next.boat = 1;
            }
            else
            {
                next.explorers = current.explorers + explorerMove[i];
                next.guardians = current.guardians + guardianMove[i];
                next.boat = 0;
            }

            if (safeState(next.explorers, next.guardians))
            {
                if (visited[next.explorers][next.guardians][next.boat] == false)
                {
                    visited[next.explorers][next.guardians][next.boat] = true;

                    next.parent = currentNumber;

                    list[back] = next;
                    back++;
                }
            }
        }
    }

    if (goal != -1)
    {
        int path[100];
        int count = 0;
        int current = goal;

        while (current != -1)
        {
            path[count] = current;
            count++;
            current = list[current].parent;
        }

        cout << "Optimal solution:" << endl;

        for (int i = count - 1; i >= 0; i--)
        {
            State s = list[path[i]];

            cout << "(" << s.explorers << ", "
                 << s.guardians << ", ";

            if (s.boat == 0)
                cout << "L";
            else
                cout << "R";

            cout << ")" << endl;
        }

        cout << "Number of crossings: " << count - 1 << endl;
    }
    else
    {
        cout << "No solution found." << endl;
    }

    return 0;
}