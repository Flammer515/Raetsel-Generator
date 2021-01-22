#include "quiz.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <fstream>
#include <string>
#include <QFile>
#include <QTextStream>
#include <QMessageBox>

using namespace std;
class quiztest
{
private:
    string Frage;
    string Tip;
    string Fragentyp;
    string Antwort;
    int Tolleranz;

public:
    quiztest(){}
    quiztest(string Frage, string Tip,string Fragentyp,string Antwort,int Tolleranz){
        this->Frage = Frage;
        this->Tip = Tip;
        this->Fragentyp = Fragentyp;
        this->Antwort = Antwort;
        this->Tolleranz = Tolleranz;
    }
    QString getFrage(){
        return QString::fromStdString(Frage);
    }
    QString getTip(){
        return QString::fromStdString(Tip);
    }
    QString getFragentyp(){
        return QString::fromStdString(Fragentyp);
    }
    QString getAntwort(){
        return QString::fromStdString(Antwort);
    }
    int getTolleranz(){
        return Tolleranz;
    }

};




quiz::quiz()
{

}
