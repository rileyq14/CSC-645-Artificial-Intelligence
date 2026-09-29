
#include <iostream>
#include <vector>
using namespace std;

extern int location;
extern int configurationScore;
extern vector<int> rooms;

void setup(int start, vector<int> initialRooms);
void suck();
void moveRight();
void moveLeft();
int chooseAction();
bool allClean();
void resetAgent();

int main(){

    int numberOfRooms;

    cout << "Enter the number of rooms: ";
    cin >> numberOfRooms;

    if (numberOfRooms <= 0){

        cout << "Invalid number of rooms." << endl;
        return 1;
    }

    int numberOfRoomStates =
        1 << numberOfRooms;

    int numberOfConfigurations =
        numberOfRoomStates * numberOfRooms;

    int totalScore = 0;

    for (int configuration = 0;
         configuration < numberOfConfigurations;
         configuration++){

        int roomPattern =
            configuration / numberOfRooms;

        int startingRoom =
            configuration % numberOfRooms;

        vector<int> initialRooms(numberOfRooms);

        for (int i = 0; i < numberOfRooms; i++){

            initialRooms[i] =
                (roomPattern >> i) & 1;
        }

        setup(startingRoom, initialRooms);

        resetAgent();

        while (!allClean()){

            int action = chooseAction();

            if (action == 1){

                suck();
            }

            else if (action == 2){

                moveRight();
            }

            else if (action == 3){

                moveLeft();
            }

            else{

                break;
            }
        }

        if (allClean()){

            configurationScore =
                configurationScore + 20;
        }

        cout << "Configuration "
             << configuration + 1
             << " score: "
             << configurationScore
             << endl;
        

        totalScore =
            totalScore + configurationScore;

        configurationScore = 0;
    }

    double averageScore =
        static_cast<double>(totalScore) /
        numberOfConfigurations;

    cout << endl;

    cout << "Number of rooms: "
         << numberOfRooms
         << endl;

    cout << "Number of configurations: "
         << numberOfConfigurations
         << endl;

    cout << "Total score: "
         << totalScore
         << endl;

    cout << "Average score: "
         << averageScore
         << endl;

    cout << "Vacuum Complete"
         << endl;

    return 0;
}
