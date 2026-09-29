
#include <vector>
using namespace std;

int location;
int configurationScore;

vector<int> rooms;

void setup(int start, vector<int> initialRooms){

    location = start;
    rooms = initialRooms;
    configurationScore = 0;
}

void suck(){

    if (rooms[location] == 1){

        rooms[location] = 0;
        configurationScore = configurationScore + 20;
    }

    else{

        configurationScore = configurationScore - 20;
    }
}

void moveRight(){

    if (location < static_cast<int>(rooms.size()) - 1){

        location++;
        configurationScore++;
    }

    else{

        configurationScore--;
    }
}

void moveLeft(){

    if (location > 0){

        location--;
        configurationScore++;
    }

    else{

        configurationScore--;
    }
}
