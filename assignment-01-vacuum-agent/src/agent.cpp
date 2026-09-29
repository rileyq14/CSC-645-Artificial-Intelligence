
#include <vector>
using namespace std;

extern int location;
extern vector<int> rooms;

int direction;

void resetAgent(){

    direction = 1;
}

bool allClean(){

    for (int room : rooms){

        if (room == 1){

            return false;
        }
    }

    return true;
}

int chooseAction(){

    if (allClean()){

        return 0;
    }

    if (rooms[location] == 1){

        return 1;
    }

    if (direction == 1){

        if (location < static_cast<int>(rooms.size()) - 1){

            return 2;
        }

        direction = -1;

        if (location > 0){

            return 3;
        }
    }

    else{

        if (location > 0){

            return 3;
        }

        direction = 1;

        if (location < static_cast<int>(rooms.size()) - 1){

            return 2;
        }
    }

    return 0;
}
