#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <fstream>
#include <string>
#include <QFile>
#include <QFileDialog>
#include <QTextStream>
#include <QMessageBox>
#include <quiz.cpp>
#include <QXmlStreamReader>
#include <QtXml>
#include<qlist.h>

using namespace std;
QString fileLocation;
QString name;
QString hint;
QString sensor;
QString value;
qint16 offset;
QList<quiztest> holder;
bool questionAsked= false;
bool solved = true;
int quizPos = 0;
bool lightOn = false;
QString color;


//initialization
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
     ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->lcdHumidity->display(30);
    ui->lcdTmp->display(20);



}

MainWindow::~MainWindow()
{
    delete ui;
}

//Start quiz/ next part of quiz
void MainWindow::on_Start_clicked()
{

   if(holder.length()!=quizPos){
        if(solved == true){
            quiztest current = holder.at(quizPos);
            value = current.getAntwort();
            sensor = current.getFragentyp();
            hint = current.getTip();
            offset = current.getTolleranz();
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\n"+current.getFrage());
            ui->textBrowser->moveCursor(QTextCursor::End);
            solved = false;
            questionAsked = true;
        }else{

           ui->textBrowser->moveCursor(QTextCursor::End);
           ui->textBrowser->textCursor().insertText("\nErst die letzte frage lösen");
           ui->textBrowser->moveCursor(QTextCursor::End);//scrolls the textBrowser to the end
   }
    }else{
       ui->textBrowser->moveCursor(QTextCursor::End);
       ui->textBrowser->textCursor().insertText("\nQuiz ist fertig gg");
       ui->textBrowser->moveCursor(QTextCursor::End);
   }






}

//file dialog/ loading the data from xml file
void MainWindow::on_chooseFile_clicked()
{
    fileLocation = QFileDialog::getOpenFileName(this,tr("Open File"),"C://","All files(*.*)");
    QString Name;
    QString description;
    QString difficulty;
    QString steps;
    QDomDocument xmlBom;
    QFile f(fileLocation);
    if (!f.open(QIODevice::ReadOnly ))
    {
        // Error while loading file
        std::cerr << "Error while loading file" << std::endl;

    }
    xmlBom.setContent(&f);


    QDomElement root =xmlBom.documentElement();
    QString Type = root.tagName();

    QDomElement Raetsel=root.firstChild().toElement();
    //extracting information about the quiz

        if(Raetsel.tagName()=="Raetsel"){
            QDomElement Child=Raetsel.firstChild().toElement();


            while(!Child.isNull()){
                if(Child.tagName()=="name") Name = Child.firstChild().toText().data();
                if(Child.tagName()=="description") description = Child.firstChild().toText().data();
                if(Child.tagName()=="difficulty") difficulty = Child.firstChild().toText().data();
                if(Child.tagName()=="steps") steps = Child.firstChild().toText().data();

                Child = Child.nextSibling().toElement();
            }
        }
         //Display extracted data
        ui->QuizName->setText(description);
        ui->difficulty->setText(difficulty);
        ui->Steps->setText(steps);








     root =xmlBom.documentElement();
     Type = root.tagName();
    //extracting the quiz steps
    QDomElement Steps=root.firstChild().toElement();
    //repeats until there are no more steps to read
    while(!Steps.isNull()){
        qDebug()<< Steps.lineNumber();
        if(Steps.tagName()=="Steps"){
            QDomElement Child=Steps.firstChild().toElement();
            while(!Child.isNull()){
                QDomElement GrandChild = Child.firstChild().toElement();
                while(!GrandChild.isNull()){
                    qDebug()<< GrandChild.lineNumber();
                    if(GrandChild.tagName()=="name") Name = GrandChild.firstChild().toText().data();
                    if(GrandChild.tagName()=="hint") hint = GrandChild.firstChild().toText().data();
                    if(GrandChild.tagName()=="sensor") sensor = GrandChild.firstChild().toText().data();
                    if(GrandChild.tagName()=="exactvalue") value = GrandChild.firstChild().toText().data();
                    if(GrandChild.tagName()=="max_range") offset = GrandChild.firstChild().toText().data().toInt();

                    GrandChild = GrandChild.nextSibling().toElement();
            }


                //add the new quiz step to the holder
                holder.append(quiztest(Name.toStdString(),hint.toStdString(),sensor.toStdString(),value.toStdString(),offset));


                Child = Child.nextSibling().toElement();
            }
        }



        Steps = Steps.nextSibling().toElement();
    }
f.close();
}
//checks if answer is right
void MainWindow::on_submit_clicked()
{
    //matching the quiztype
    if(sensor =="keyboard"){
        //comparing the given answer with the expected answer
        if(ui->eingabe->text()==value){
            solved = true;
            qDebug()<<"war Richtig";
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nWar Richtig");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }
    if(sensor =="temp"){
        if(ui->lcdTmp->value()>= (value.toInt()-offset) && ui->lcdTmp->value()<= (value.toInt()+offset)){
            solved = true;
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nWar Richtig");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }
    if(sensor =="humidity"){
        if(ui->lcdHumidity->value() >= (value.toInt()-offset) && ui->lcdHumidity->value()<= (value.toInt()+offset)){
            solved = true;
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nWar Richtig");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }
    if(sensor =="light"){
        bool tmp;
        if(value == "true"){
            tmp = true;
        }else{
            tmp = false;
        }
        if(lightOn==tmp){
        solved = true;
        ui->textBrowser->moveCursor(QTextCursor::End);
        ui->textBrowser->textCursor().insertText("\nWar Richtig");
        ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }
    if(sensor =="color"){
        if(color==value ){
        solved = true;
        ui->textBrowser->moveCursor(QTextCursor::End);
        ui->textBrowser->textCursor().insertText("\nWar Richtig");
        ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }
    if(sensor =="gyro"){//if gyro x = value and y = offset
        if(ui->lcdGradX->value()==value.toInt()&ui->lcdGradY->value()==offset){
            solved = true;
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nWar Richtig");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }else{
            ui->textBrowser->moveCursor(QTextCursor::End);
            ui->textBrowser->textCursor().insertText("\nFalsch versuchen sie es erneut");
            ui->textBrowser->moveCursor(QTextCursor::End);
        }
    }



    if(solved){
        questionAsked=false;
        quizPos +=1;
    }
}
void MainWindow::on_pushButton_clicked()// if question was asked display the hint
{
    if(questionAsked){
        ui->textBrowser->moveCursor(QTextCursor::End);
        ui->textBrowser->textCursor().insertText("\n"+hint);
        ui->textBrowser->moveCursor(QTextCursor::End);
    }

}


//ui interaction with the displays( tmp, humidity...
void MainWindow::on_btn_tmp_up_clicked()
{

    ui->lcdTmp->display(ui->lcdTmp->value()+1);
}

void MainWindow::on_btn_tmp_down_clicked()
{
    ui->lcdTmp->display(ui->lcdTmp->value()-1);
}

void MainWindow::on_btnhummidity_up_clicked()
{
    ui->lcdHumidity->display(ui->lcdHumidity->value()+1);
}

void MainWindow::on_btnhumidity_down_clicked()
{
    ui->lcdHumidity->display(ui->lcdHumidity->value()-1);
}









void MainWindow::on_btnXup_clicked()
{

    ui->lcdGradX->display(ui->lcdGradX->value()+90);
    if(ui->lcdGradX->value()>=360){
        ui->lcdGradX->display(ui->lcdGradX->value()-360);
    }
}
void MainWindow::on_btnXdown_clicked()
{
    ui->lcdGradX->display(ui->lcdGradX->value()-90);
    if(ui->lcdGradX->value()<0){
        ui->lcdGradX->display(ui->lcdGradX->value()+360);}
}
void MainWindow::on_btnYdown_clicked()
{
    ui->lcdGradY->display(ui->lcdGradY->value()-90);
    if(ui->lcdGradY->value()<0){
        ui->lcdGradY->display(ui->lcdGradY->value()+360);}
}

void MainWindow::on_btnYup_clicked()
{
    ui->lcdGradY->display(ui->lcdGradY->value()+90);
    if(ui->lcdGradY->value()>=360){
        ui->lcdGradY->display(ui->lcdGradY->value()-360);}
}

void MainWindow::on_btnLichtAn_clicked()
{
    if(!lightOn){

        ui->btnLichtAn->setText("Licht aus");
        ui->LichtAnzeigen->setText("Licht: An");
        lightOn = true;
    }else{
        ui->btnLichtAn->setText("Licht an");
        ui->LichtAnzeigen->setText("Licht: Aus");
        lightOn = false;
    }

}



void MainWindow::on_farbenAuswahl_activated(int index)
{
    color = ui->farbenAuswahl->itemText(index);
    qDebug()<<color;
}


