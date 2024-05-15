#include <iostream>
#include <vector>
#include <string>
#include <thread>
//#include <mutex>
#include <fstream>
//#include <sys/stat.h>
//#include <direct.h>
//#include <pthread.h>
#include <filesystem>
//#include <chrono>
#include <future>
//#include <math.h>
//#include <conio.h>
//#include <signal.h>
using namespace std;



namespace fs = std::filesystem;

void copyFile(const string& src, const string& dst) {
    ifstream in(src, ios::binary);
    ofstream out(dst, ios::binary);
    out << in.rdbuf();
}

void copyDir(const string& src, const string& dst) {

    std::filesystem::create_directory(dst);
     
    std::vector<std::filesystem::path> files, directories;
    
    for (const auto& entry : std::filesystem::directory_iterator(src)) {
        if (std::filesystem::is_regular_file(entry)) {
            files.push_back(entry.path());
        }
        else if (std::filesystem::is_directory(entry)) {
            directories.push_back(entry.path());
        }
    }
  
    std::vector<std::future<void>> fileFutures, dirFutures;
  
    // Запустить копирование файлов асинхронно
    for (const auto& file : files) {
        string newSrc = src + "\\" + file.filename().string();
        string newDst = dst + "\\" + file.filename().string();
        std::cout << "Copying file " << endl << "From: " << newSrc << endl << "To: " << newDst << endl;
        fileFutures.push_back(async(launch::async, copyFile, newSrc, newDst));
    }
  
    // Запустить копирование директорий асинхронно
    for (const auto& directory : directories) {
        string newSrc = src + "\\" + directory.filename().string();
        string newDst = dst + "\\" + directory.filename().string();
        std::cout << "Copying directory " << endl << "From: " << newSrc << endl << "To: " << newDst << endl;
        dirFutures.push_back(async(launch::async, copyDir, newSrc, newDst));
    }
  
    for (auto& future : fileFutures) {
        future.get();
    }
    for (auto& future : dirFutures) {
        future.get();
    }
}

int main(){

   /* SetConsoleCP(1251);
    SetConsoleOutputCP(1251);*/

    std::cout << "\n\n_________start__________\n\n";
    string src = "C:\\MPP\\ConsoleApplication6\\ConsoleApplication6";
    string dst = "C:\\MPP\\ConsoleApplication6\\ConsoleApplication6-copy";
    
    
    thread t(copyDir, src, dst);
    t.join();

    std::cout << "\n\n_______________end_______________\n\n";

    return 0;
}