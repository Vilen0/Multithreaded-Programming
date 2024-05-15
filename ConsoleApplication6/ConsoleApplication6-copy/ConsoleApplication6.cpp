/*
Реализуйте уникальный алгоритм сортировки sleepsort с асимптотикой O(N) (по процессорному времени).

На стандартный вход программы подается не более 100 строк различной длины.
Вам необходимо вывести эти строки, отсортированные по длине.
Строки одинаковой длины могут выводиться в произвольном порядке.

Для каждой входной строки, создайте поток и передайте ей эту строку в качестве параметра.
Поток должна вызвать sleep(2) или usleep(2) с параметром, пропорциональным длине этой строки.
Затем поток выводит строку в стандартный поток вывода и завершается.
Не следует выбирать коэффициент пропорциональности слишком маленьким, вы рискуете получить некорректную сортировку.
*/





#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <mutex>
using namespace std;

mutex printMutex;

void Print(const string& str) {
    lock_guard<mutex> lock(printMutex);
    cout << str << endl;
}

void sleepSortAndPrint(const string& str) {

    int sleepTime = str.length() * 100-2000; 

    this_thread::sleep_for(chrono::milliseconds(sleepTime));

    Print(str);
}



int main() {
    setlocale(LC_ALL, "Ru");

    ifstream inputFile("input.txt");
    if (!inputFile) {
        cerr << "Ошибка открытия файла" << endl;
        return 1;
    }

    vector<string> strings;

    string input;
    while (getline(inputFile, input)) {
        strings.push_back(input);
    }

    inputFile.close();

    vector<thread> threads;
    for (const auto& str : strings) {
        threads.push_back(thread(sleepSortAndPrint, str));
    }

    for (auto& thread : threads) {
        thread.join();
    }

    return 0;
}
